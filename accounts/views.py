from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Q
from .models import CustomUser
from .forms import StudentRegisterForm, EmployerRegisterForm, StudentProfileForm, EmployerProfileForm, LoginForm
from opportunities.models import Opportunity, Application
from events.models import Event
from networking.models import Connection
from grades.models import Grade
from .ai_utils import parse_transcript_with_gemini


def home(request):
    if request.user.is_authenticated:
        if request.user.is_employer:
            return redirect('corporate_dashboard')
        return redirect('campus_dashboard')
    stats = {
        'students': CustomUser.objects.filter(portal_type='student', is_active=True).count(),
        'employers': CustomUser.objects.filter(portal_type='employer', is_active=True).count(),
        'opportunities': Opportunity.objects.filter(status='active').count(),
        'applications': Application.objects.count(),
    }
    featured_employers = CustomUser.objects.filter(
        portal_type='employer', is_active=True, is_verified=True
    ).exclude(company_name='').order_by('?')[:8]
    recent_opportunities = Opportunity.objects.filter(status='active').order_by('-created_at')[:4]
    return render(request, 'home.html', {'stats': stats, 'featured_employers': featured_employers,
                                          'recent_opportunities': recent_opportunities})


def register_view(request):
    portal = request.GET.get('portal', 'student')
    if request.method == 'POST':
        portal = request.POST.get('portal_type', 'student')
        if portal == 'employer':
            form = EmployerRegisterForm(request.POST, request.FILES)
        else:
            form = StudentRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, f"Welcome to GradPulse, {user.display_name}!")
            if user.is_employer:
                return redirect('corporate_dashboard')
            return redirect('campus_dashboard')
    else:
        if portal == 'employer':
            form = EmployerRegisterForm()
        else:
            form = StudentRegisterForm()
    return render(request, 'auth/register.html', {'form': form, 'portal': portal})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.display_name}!")
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            if user.is_employer:
                return redirect('corporate_dashboard')
            return redirect('campus_dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm(request)
    return render(request, 'auth/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('login')


# ─── Student / Campus Views ───────────────────────────────────────────────────

@login_required
def campus_dashboard(request):
    if not request.user.is_student:
        return redirect('corporate_dashboard')
    user = request.user
    my_applications = Application.objects.filter(student=user).select_related('opportunity').order_by('-applied_at')[:5]
    upcoming_events = Event.objects.filter(date__gt=__import__('django.utils.timezone', fromlist=['now']).now()).order_by('date')[:3]
    active_opportunities = Opportunity.objects.filter(status='active').order_by('-created_at')[:6]
    connections_count = Connection.objects.filter(
        Q(from_user=user, status='accepted') | Q(to_user=user, status='accepted')
    ).count()
    return render(request, 'campus/dashboard.html', {
        'user': user,
        'my_applications': my_applications,
        'upcoming_events': upcoming_events,
        'active_opportunities': active_opportunities,
        'connections_count': connections_count,
        'applications_count': my_applications.count(),
    })


@login_required
def campus_profile(request):
    if not request.user.is_student:
        return redirect('corporate_dashboard')
    if request.method == 'POST':
        form = StudentProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('campus_profile')
    else:
        form = StudentProfileForm(instance=request.user)
    return render(request, 'campus/profile.html', {'form': form})


@login_required
def transcript_upload(request):
    if not request.user.is_student:
        return redirect('home')
        
    if request.method == 'POST' and request.FILES.get('transcript'):
        pdf_file = request.FILES['transcript']
        
        # 1. Call Gemini to parse
        messages.info(request, "AI is analyzing your transcript, please wait...")
        data = parse_transcript_with_gemini(pdf_file)
        
        if isinstance(data, dict) and "error" in data:
            messages.error(request, f"AI Parsing failed: {data['error']}")
            return redirect('campus_dashboard')
            
        # 2. Save grades
        count = 0
        for item in data:
            try:
                # Basic cleaning of data from AI
                unit_name = item.get('course_name') or item.get('unit_name')
                grade_val = item.get('grade')
                semester = item.get('semester', '')
                year_str = str(item.get('year', ''))
                year = int(year_str) if year_str.isdigit() else None
                
                if unit_name and grade_val:
                    Grade.objects.create(
                        student=request.user,
                        unit_name=unit_name,
                        grade=grade_val,
                        semester=semester,
                        year=year
                    )
                    count += 1
            except Exception as e:
                print(f"Error saving grade: {e}")
                continue
                
        if count > 0:
            messages.success(request, f"Successfully extracted {count} grades using AI!")
        else:
            messages.warning(request, "AI couldn't find any grades in that PDF.")
            
        return redirect('campus_dashboard')
        
    return render(request, 'campus/transcript_upload.html')


# ─── Employer / Corporate Views ───────────────────────────────────────────────

@login_required
def corporate_dashboard(request):
    if not (request.user.is_employer or request.user.is_superuser):
        return redirect('campus_dashboard')
    user = request.user
    if user.is_superuser:
        my_listings = Opportunity.objects.all().annotate(
            app_count=Count('applications')
        ).order_by('-created_at')
        recent_applications = Application.objects.all().select_related('student', 'opportunity').order_by('-applied_at')[:10]
        total_apps = Application.objects.count()
        shortlisted = Application.objects.filter(status='shortlisted').count()
        hired = Application.objects.filter(status='hired').count()
    else:
        my_listings = Opportunity.objects.filter(company=user).annotate(
            app_count=Count('applications')
        ).order_by('-created_at')
        recent_applications = Application.objects.filter(
            opportunity__company=user
        ).select_related('student', 'opportunity').order_by('-applied_at')[:10]
        total_apps = Application.objects.filter(opportunity__company=user).count()
        shortlisted = Application.objects.filter(opportunity__company=user, status='shortlisted').count()
        hired = Application.objects.filter(opportunity__company=user, status='hired').count()
    
    stats = {
        'active_listings': my_listings.filter(status='active').count(),
        'total_applications': total_apps,
        'shortlisted': shortlisted,
        'hired': hired,
    }
    return render(request, 'corporate/dashboard.html', {
        'user': user,
        'my_listings': my_listings[:5],
        'recent_applications': recent_applications,
        'stats': stats,
    })


@login_required
def corporate_profile(request):
    if not request.user.is_employer:
        return redirect('campus_dashboard')
    if request.method == 'POST':
        form = EmployerProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Company profile updated successfully!')
            return redirect('corporate_profile')
    else:
        form = EmployerProfileForm(instance=request.user)
    return render(request, 'corporate/profile.html', {'form': form})


@login_required
def talent_search(request):
    if not request.user.is_employer:
        return redirect('campus_dashboard')
    qs = CustomUser.objects.filter(portal_type='student', is_active=True)
    institution = request.GET.get('institution')
    course = request.GET.get('course')
    skills = request.GET.get('skills')
    otw = request.GET.get('open_to_work')
    if institution:
        qs = qs.filter(institution__icontains=institution)
    if course:
        qs = qs.filter(course__icontains=course)
    if skills:
        qs = qs.filter(skills__icontains=skills)
    if otw:
        qs = qs.filter(open_to_work=True)
    return render(request, 'corporate/talent.html', {'students': qs, 'filters': request.GET})


@login_required
def corporate_applications(request):
    if not request.user.is_employer:
        return redirect('campus_dashboard')
    apps = Application.objects.filter(
        opportunity__company=request.user
    ).select_related('student', 'opportunity').order_by('-applied_at')
    status_filter = request.GET.get('status')
    opp_filter = request.GET.get('opportunity')
    if status_filter:
        apps = apps.filter(status=status_filter)
    if opp_filter:
        apps = apps.filter(opportunity_id=opp_filter)
    opportunities = Opportunity.objects.filter(company=request.user)
    return render(request, 'corporate/applications.html', {
        'applications': apps,
        'opportunities': opportunities,
        'filters': request.GET,
    })


@login_required
def update_application_status(request, pk):
    app = get_object_or_404(Application, pk=pk, opportunity__company=request.user)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in [s[0] for s in Application.STATUS_CHOICES]:
            app.status = new_status
            app.save()
            messages.success(request, f'Application status updated to {new_status}.')
    return redirect('corporate_applications')


@login_required
def student_profile_public(request, pk):
    if not request.user.is_employer:
        return redirect('campus_dashboard')
    student = get_object_or_404(CustomUser, pk=pk, portal_type='student')
    return render(request, 'corporate/student_profile_view.html', {'student': student})
