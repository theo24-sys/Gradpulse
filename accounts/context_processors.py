from django.utils import timezone
from events.models import Event
from networking.models import Message
from notifications.models import Notification

def live_counts(request):
    if request.user.is_authenticated:
        return {
            'upcoming_events_count': Event.objects.filter(date__gt=timezone.now()).count(),
            'unread_messages_count': Message.objects.filter(receiver=request.user, is_read=False).count(),
            'unread_notifications': Notification.objects.filter(user=request.user, is_read=False).count(),
        }
    return {
        'upcoming_events_count': 0,
        'unread_messages_count': 0,
        'unread_notifications': 0,
    }
