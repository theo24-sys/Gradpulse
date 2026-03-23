from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Q
from .models import CustomUser, UniSmartResource, UniSmartCourseCart, UniSmartMasterCourse
from .forms import StudentRegisterForm, EmployerRegisterForm, UniSmartRegisterForm, StudentProfileForm, EmployerProfileForm, LoginForm
from opportunities.models import Opportunity, Application
from events.models import Event
from networking.models import Connection
from grades.models import Grade
from .ai_utils import (
    parse_transcript_with_gemini, unismart_career_chat, 
    get_mentor_recommendation, calculate_kcse_clusters, 
    get_academic_guidance, extract_courses_from_pdf,
    extract_courses_from_text
)
from scraping.utils import get_items_for_student


def home(request):
    if request.user.is_authenticated:
        if request.user.is_employer:
            return redirect('corporate_dashboard')
        if request.user.is_unismart:
            return redirect('unismart_dashboard')
        return redirect('campus_dashboard')
    stats = {
        'students': CustomUser.objects.filter(portal_type='student', is_active=True).count(),
        'unismart': CustomUser.objects.filter(portal_type='unismart', is_active=True).count(),
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


def unismart_role_selection(request):
    return render(request, 'auth/unismart_roles.html')


@login_required
def unismart_dashboard(request):
    if not request.user.is_unismart:
        return redirect('home')
    
    # Fetch resources relevant to the student's category
    resources = UniSmartResource.objects.filter(
        category=request.user.student_category,
        is_active=True
    ).order_by('-uploaded_at')
    
    # Get a random mentor recommendation for and initial "connection" hint
    mentor = get_mentor_recommendation(request.user.target_career)
    
    return render(request, 'unismart/dashboard.html', {
        'user': request.user,
        'resources': resources,
        'mentor': mentor
    })


@login_required
def unismart_chat(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        if not message:
            return render(request, 'unismart/chat_response.html', {'response': "Please enter a message."})
        
        user_context = f"Category: {request.user.get_student_category_display()}, Grade: {request.user.grade_level}, Interest: {request.user.target_career}"
        ai_response = unismart_career_chat(message, user_context)
        
        # Check if query implies a course to recommend a mentor
        mentor = get_mentor_recommendation(message)
        
        return render(request, 'unismart/chat_response.html', {
            'response': ai_response,
            'mentor': mentor
        })
    return redirect('unismart_dashboard')


@login_required
def unismart_helb_guide(request):
    return render(request, 'unismart/helb_guide.html')


@login_required
def unismart_kcse_entry(request):
    grades = ['A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-', 'D+', 'D', 'D-', 'E']
    return render(request, 'unismart/kcse_results.html', {'grades_list': grades})


@login_required
def unismart_save_kcse(request):
    if request.method == 'POST':
        results = {}
        for key in ['ENG', 'KISW', 'MATH', 'BIO', 'PHYS', 'CHEM']:
            val = request.POST.get(key)
            if val:
                results[key] = val
        
        # Capture optional subjects
        h1_key = request.POST.get('H1_KEY')
        h1_val = request.POST.get('H1_VAL')
        if h1_key and h1_val:
            results[h1_key] = h1_val
            
        e1_key = request.POST.get('E1_KEY')
        e1_val = request.POST.get('E1_VAL')
        if e1_key and e1_val:
            results[e1_key] = e1_val
            
        request.user.kcse_results = results
        
        # Calculate clusters using AI
        analysis = calculate_kcse_clusters(results)
        request.user.cluster_points = analysis.get('clusters', {})
        request.user.save()
        
        return render(request, 'unismart/kcse_analysis_partial.html', {
            'analysis': analysis
        })
    return redirect('unismart_dashboard')


@login_required
def unismart_manage_cart(request):
    cart_items = request.user.course_basket.all()
    return render(request, 'unismart/course_cart.html', {'cart_items': cart_items})


@login_required
def unismart_extract_courses(request, resource_id):
    if not request.user.is_unismart:
        return redirect('home')
    
    resource = get_object_or_404(UniSmartResource, id=resource_id)
    if not resource.file:
        return render(request, 'unismart/extract_result_partial.html', {'error': 'No file found'})

    # Determine if it's TVET or Degree based on title
    level = 'tvet' if 'tvet' in resource.title.lower() else 'degree'
    
    courses_data = extract_courses_from_pdf(resource.file, level=level)
    
    count = 0
    for item in courses_data:
        try:
            name = item.get('course_name')
            code = item.get('course_code')
            if name and code:
                UniSmartMasterCourse.objects.update_or_create(
                    code=code,
                    defaults={
                        'name': name,
                        'institution': item.get('institution', ''),
                        'cluster_group': item.get('cluster_group', ''),
                        'min_points': item.get('min_points'),
                        'level': level
                    }
                )
                count += 1
        except Exception as e:
            print(f"Error saving master course: {e}")
            
    return render(request, 'unismart/extract_result_partial.html', {
        'count': count,
        'title': resource.title
    })


@login_required
def unismart_course_browser(request):
    level = request.GET.get('level', 'degree')
    query = request.GET.get('q', '')
    cluster_filter = request.GET.get('cluster', '')
    active_category = request.GET.get('category', 'all')
    
    courses = UniSmartMasterCourse.objects.filter(level=level)
    
    # Category to Cluster ID mapping
    category_map = {
        'business': [1, 2, 10],
        'arts': [3, 11, 14, 17, 18, 20, 8, 12], # Added 8 (Agribusiness) and 12 (Natural Resources) to relevant groups
        'science': [4, 5, 6, 7, 9, 15, 16],
        'health': [13],
        'education': [19],
    }
    
    # Get all cluster stats for counts
    cluster_stats = UniSmartMasterCourse.objects.filter(level=level).values('cluster_group').annotate(count=Count('id')).order_by('cluster_group')
    
    # Filter by category if requested
    if active_category != 'all' and active_category in category_map:
        cluster_ids = category_map[active_category]
        # Match "Cluster X:" pattern
        query_filter = Q()
        for cid in cluster_ids:
            query_filter |= Q(cluster_group__startswith=f"Cluster {cid}:")
        courses = courses.filter(query_filter)

    if cluster_filter:
        courses = courses.filter(cluster_group=cluster_filter)
        
    if query:
        courses = courses.filter(
            Q(name__icontains=query) | Q(code__icontains=query) | Q(institution__icontains=query)
        )
    
    # Order by cluster group for regrouping in template
    courses = courses.order_by('cluster_group', 'name')
    
    total_courses = UniSmartMasterCourse.objects.filter(level=level).count()
    
    return render(request, 'unismart/course_browser.html', {
        'courses': courses,
        'level': level,
        'query': query,
        'cluster_filter': cluster_filter,
        'cluster_stats': cluster_stats,
        'active_category': active_category,
        'total_courses': total_courses,
    })


@login_required
def unismart_bulk_extract(request):
    if not request.user.is_unismart:
        return redirect('home')
        
    if request.method == 'POST':
        text = request.POST.get('bulk_text', '')
        level = request.POST.get('level', 'degree')
        
        courses_data = extract_courses_from_text(text, level=level)
        
        count = 0
        for item in courses_data:
            try:
                name = item.get('course_name')
                code = item.get('course_code')
                if name and code:
                    UniSmartMasterCourse.objects.update_or_create(
                        code=code,
                        defaults={
                            'name': name,
                            'institution': item.get('institution', ''),
                            'cluster_group': item.get('cluster_group', ''),
                            'min_points': item.get('min_points'),
                            'level': level
                        }
                    )
                    count += 1
            except Exception as e:
                print(f"Error saving bulk course: {e}")
        
        if count > 0:
            messages.success(request, f"Successfully extracted {count} new courses!")
        else:
            messages.warning(request, "AI couldn't find any courses in the text you pasted.")
            
    return redirect('unismart_course_browser')


@login_required
def unismart_add_to_cart(request):
    if request.method == 'POST':
        course_name = request.POST.get('course_name')
        institution = request.POST.get('institution', '')
        course_code = request.POST.get('course_code', '')
        
        if course_name:
            UniSmartCourseCart.objects.create(
                student=request.user,
                course_name=course_name,
                institution=institution,
                course_code=course_code
            )
            return render(request, 'unismart/cart_added_partial.html', {'course_name': course_name})
    return render(request, 'unismart/cart_added_partial.html', {'error': 'Failed to add'})


@login_required
def unismart_remove_from_cart(request, item_id):
    if request.method == 'POST':
        item = get_object_or_404(UniSmartCourseCart, id=item_id, student=request.user)
        item.delete()
        return render(request, 'unismart/cart_removed_partial.html')
    return redirect('unismart_manage_cart')


def register_view(request):
    portal = request.GET.get('portal', 'student')
    category = request.GET.get('category', '')
    
    if request.method == 'POST':
        if portal == 'employer':
            form = EmployerRegisterForm(request.POST, request.FILES)
        elif portal == 'unismart':
            form = UniSmartRegisterForm(request.POST, request.FILES)
        else:
            form = StudentRegisterForm(request.POST, request.FILES)
        
        # DEBUG BYPASS: Allow registration without reCAPTCHA if ?bypass=true is in URL (and DEBUG is on)
        if settings.DEBUG and request.GET.get('bypass') == 'true':
            if 'captcha' in form.fields:
                form.fields['captcha'].required = False
        
        if form.is_valid():
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, f"Welcome to GradPulse, {user.display_name}!")
            if user.is_employer:
                return redirect('corporate_dashboard')
            if user.is_unismart:
                return redirect('unismart_dashboard')
            return redirect('campus_dashboard')
    else:
        if portal == 'employer':
            form = EmployerRegisterForm()
        elif portal == 'unismart':
            form = UniSmartRegisterForm(initial={'student_category': category})
        else:
            form = StudentRegisterForm()
    return render(request, 'auth/register.html', {'form': form, 'portal': portal})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        
        # DEBUG BYPASS: Allow login without reCAPTCHA if ?bypass=true is in URL (and DEBUG is on)
        if settings.DEBUG and request.GET.get('bypass') == 'true':
            if 'captcha' in form.fields:
                form.fields['captcha'].required = False
        
        if form.is_valid():
            user = form.get_user()
            import sys
            print(f"DEBUG AUTH: User {user.username} (ID: {user.id}) matched. is_active={user.is_active}", file=sys.stderr)
            login(request, user)
            messages.success(request, f"Welcome back, {user.display_name}!")
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            if user.is_employer:
                return redirect('corporate_dashboard')
            return redirect('campus_dashboard')
        else:
            # Better error reporting: show specific form errors (like CAPTCHA failure)
            import sys
            print(f"DEBUG AUTH FAIL: Form invalid for input {request.POST.get('username')}. Errors: {form.errors.as_text()}", file=sys.stderr)
            for field, errors in form.errors.items():
                for error in errors:
                    if field == '__all__':
                        messages.error(request, error)
                    else:
                        messages.error(request, f"{field.capitalize()}: {error}")
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
    
    # NEW: Fetch live discoveries from the 34 scrapers
    discovered_items = get_items_for_student(student=user, limit=6)
    
    # AI Academic Guidance (sample or cached)
    academic_tip = get_academic_guidance(user.course or "General Studies")
    
    return render(request, 'campus/dashboard.html', {
        'user': user,
        'my_applications': my_applications,
        'upcoming_events': upcoming_events,
        'active_opportunities': active_opportunities,
        'discovered_items': discovered_items,
        'connections_count': connections_count,
        'applications_count': my_applications.count(),
        'academic_tip': academic_tip,
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
            return redirect('grades')
            
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
