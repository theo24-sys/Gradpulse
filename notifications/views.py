from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Notification


@login_required
def notifications_view(request):
    if request.GET.get('mark_read'):
        Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
        return redirect('notifications')
        
    notes = Notification.objects.filter(user=request.user).order_by('-created_at')
    # We no longer mark all as read automatically on view, 
    # as we have a button for it now and it's better for UX.
    return render(request, 'notifications/list.html', {'notifications': notes})
