from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .utils import get_items_for_student
from django.db import ProgrammingError

@login_required
def external_opportunities(request):
    """View to display scraped internships and jobs matched to student profile."""
    try:
        opportunities = get_items_for_student(
            student=request.user,
            source_type='opportunities',
            limit=20
        )
    except Exception as e:
        print(f"Scraping view error: {e}")
        opportunities = []
    
    return render(request, 'campus/external_opportunities.html', {
        'items': opportunities,
        'title': 'External Internships & Jobs',
        'category': 'opportunities'
    })

@login_required
def external_events(request):
    try:
        events = get_items_for_student(student=request.user, source_type='events', limit=20)
    except Exception:
        events = []
    return render(request, 'campus/external_opportunities.html', {
        'items': events,
        'title': 'Industry Events',
        'category': 'events'
    })

@login_required
def external_learning(request):
    try:
        items = get_items_for_student(student=request.user, source_type='credentials', limit=20)
    except Exception:
        items = []
    return render(request, 'campus/external_opportunities.html', {
        'items': items,
        'title': 'Micro-Credentials & Courses',
        'category': 'credentials'
    })
