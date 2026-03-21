from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import OpportunityForm, ApplicationForm
from notifications.models import Notification


def opportunity_list(request):
    qs = Opportunity.objects.filter(status='active').select_related('company')
    type_f = request.GET.get('type')
    sector_f = request.GET.get('sector')
    loc_f = request.GET.get('location')
    q = request.GET.get('q')
    if type_f:
        qs = qs.filter(type=type_f)
    if sector_f:
        qs = qs.filter(sector=sector_f)
    if loc_f:
        qs = qs.filter(location__icontains=loc_f)
    if q:
        qs = qs.filter(title__icontains=q)
    return render(request, 'opportunities/list.html', {
        'opportunities': qs,
        'filters': request.GET,
        'types': Opportunity.TYPE_CHOICES,
        'sectors': Opportunity.SECTOR_CHOICES,
    })


def opportunity_detail(request, pk):
    opp = get_object_or_404(Opportunity, pk=pk)
    opp.views_count += 1
    opp.save(update_fields=['views_count'])
    applied = False
    if request.user.is_authenticated and request.user.is_student:
        applied = Application.objects.filter(student=request.user, opportunity=opp).exists()
    form = ApplicationForm()
    return render(request, 'opportunities/detail.html', {'opportunity': opp, 'applied': applied, 'form': form})


@login_required
def apply_opportunity(request, pk):
    if not request.user.is_student:
        messages.error(request, 'Only students can apply for opportunities.')
        return redirect('opportunity_list')
    opp = get_object_or_404(Opportunity, pk=pk, status='active')
    if Application.objects.filter(student=request.user, opportunity=opp).exists():
        messages.warning(request, 'You have already applied for this opportunity.')
        return redirect('opportunity_detail', pk=pk)
    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            app = form.save(commit=False)
            app.student = request.user
            app.opportunity = opp
            app.save()
            messages.success(request, f'Application submitted for "{opp.title}"!')
            return redirect('campus_dashboard')
    return redirect('opportunity_detail', pk=pk)


@login_required
def post_opportunity(request):
    if not (request.user.is_employer or request.user.is_superuser):
        messages.error(request, 'Only employers or administrators can post opportunities.')
        return redirect('campus_dashboard')
    if request.method == 'POST':
        form = OpportunityForm(request.POST)
        if form.is_valid():
            opp = form.save(commit=False)
            opp.company = request.user
            opp.save()
            messages.success(request, f'Opportunity "{opp.title}" posted successfully!')
            return redirect('corporate_dashboard')
    else:
        form = OpportunityForm()
    return render(request, 'opportunities/post.html', {'form': form})


@login_required
def edit_opportunity(request, pk):
    if request.user.is_superuser:
        opp = get_object_or_404(Opportunity, pk=pk)
    else:
        opp = get_object_or_404(Opportunity, pk=pk, company=request.user)
    if request.method == 'POST':
        form = OpportunityForm(request.POST, instance=opp)
        if form.is_valid():
            form.save()
            messages.success(request, 'Opportunity updated.')
            return redirect('corporate_dashboard')
    else:
        form = OpportunityForm(instance=opp)
    return render(request, 'opportunities/post.html', {'form': form, 'editing': True})


def youth_programs_list(request):
    from .models import YouthProgram
    programs = YouthProgram.objects.all().order_by('-created_at')
    return render(request, 'campus/youth_programs.html', {'programs': programs})
@login_required
def scrape_discovery(request):
    if not request.user.is_superuser:
        messages.error(request, "Permission denied.")
        return redirect('home')
    
    try:
        # Run synchronously to ensure scraping actually produces results even if
        # Celery worker/Redis are misconfigured in the environment.
        from django.core.management import call_command
        call_command('scrape', '--source', 'opportunities')
        
        # Notify the admin
        Notification.objects.create(
            user=request.user,
            message="Live web scraping for Opportunities has completed successfully.",
            link="/admin/scraping/scrapeditem/"
        )
        
        messages.success(request, "Live web scraping completed for Opportunities. Check the Scraped Items in Admin.")
    except Exception as e:
        messages.error(request, f"Scraping failed: {str(e)}")
        
    return redirect('corporate_dashboard')
