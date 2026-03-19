from events.models import Event
from django.utils import timezone

def live_counts(request):
    if request.user.is_authenticated:
        return {
            'upcoming_events_count': Event.objects.filter(date__gt=timezone.now()).count()
        }
    return {'upcoming_events_count': 0}
