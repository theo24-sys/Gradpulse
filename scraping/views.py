from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .utils import get_items_for_student

@login_required
def external_opportunities(request):
    """View to display scraped internships and jobs matched to student profile."""
    # Attempt to get student profile
    profile = getattr(request.user, 'student_profile', None)
    
    opportunities = get_items_for_student(
        student_profile=profile,
        source_type='opportunities',
        limit=20
    )
    
    return render(request, 'campus/external_opportunities.html', {
        'items': opportunities,
        'title': 'External Internships & Jobs',
        'category': 'opportunities'
    })

@login_required
def external_events(request):
    profile = getattr(request.user, 'student_profile', None)
    events = get_items_for_student(profile, source_type='events', limit=20)
    return render(request, 'campus/external_opportunities.html', {
        'items': events,
        'title': 'Industry Events',
        'category': 'events'
    })

@login_required
def external_learning(request):
    profile = getattr(request.user, 'student_profile', None)
    items = get_items_for_student(profile, source_type='credentials', limit=20)
    return render(request, 'campus/external_opportunities.html', {
        'items': items,
        'title': 'Micro-Credentials & Courses',
        'category': 'credentials'
    })
