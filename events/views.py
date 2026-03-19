from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Event, RSVP


def events_list(request):
    upcoming = Event.objects.filter(date__gte=timezone.now()).order_by('date')
    past = Event.objects.filter(date__lt=timezone.now()).order_by('-date')[:6]
    rsvped_ids = []
    if request.user.is_authenticated and request.user.is_student:
        rsvped_ids = list(RSVP.objects.filter(student=request.user).values_list('event_id', flat=True))
    return render(request, 'campus/events.html', {
        'upcoming_events': upcoming, 'past_events': past, 'rsvped_ids': rsvped_ids,
    })


@login_required
def rsvp_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.user.is_student:
        RSVP.objects.get_or_create(student=request.user, event=event)
        messages.success(request, f'RSVP confirmed for "{event.title}"!')
    return redirect('events_list')
