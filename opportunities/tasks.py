from celery import shared_task
from django.utils import timezone
from .models import Opportunity
from events.models import Event

@shared_task
def delete_expired_items():
    """
    Deletes opportunities that have passed their deadline
    and events that have passed their date.
    """
    now = timezone.now()
    
    # Delete expired opportunities
    # Check if deadline is before today's date
    expired_opportunities = Opportunity.objects.filter(deadline__lt=now.date())
    opp_count = expired_opportunities.count()
    expired_opportunities.delete()
    
    # Delete expired events
    # Check if event date is before now
    expired_events = Event.objects.filter(date__lt=now)
    event_count = expired_events.count()
    expired_events.delete()
    
    return f"Deleted {opp_count} expired opportunities and {event_count} expired events."
