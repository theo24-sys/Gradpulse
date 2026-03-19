from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Notification


@login_required
def notifications_view(request):
    notes = Notification.objects.filter(user=request.user)
    notes.update(is_read=True)
    return render(request, 'notifications/list.html', {'notifications': notes})
