from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Connection, Collaboration, CollaborationMember
from accounts.models import CustomUser


@login_required
def networking_view(request):
    q = request.GET.get('q', '')
    students = CustomUser.objects.filter(portal_type='student', is_active=True).exclude(pk=request.user.pk)
    if q:
        students = students.filter(Q(first_name__icontains=q) | Q(last_name__icontains=q) | Q(skills__icontains=q))
    my_connections = Connection.objects.filter(
        Q(from_user=request.user, status='accepted') | Q(to_user=request.user, status='accepted')
    )
    pending_received = Connection.objects.filter(to_user=request.user, status='pending')
    return render(request, 'campus/networking.html', {
        'students': students, 'q': q,
        'my_connections': my_connections, 'pending_received': pending_received,
    })


@login_required
def send_connection(request, pk):
    to_user = get_object_or_404(CustomUser, pk=pk)
    Connection.objects.get_or_create(from_user=request.user, to_user=to_user)
    messages.success(request, f'Connection request sent to {to_user.display_name}.')
    return redirect('networking')


@login_required
def accept_connection(request, pk):
    conn = get_object_or_404(Connection, pk=pk, to_user=request.user)
    conn.status = 'accepted'
    conn.save()
    messages.success(request, f'Connected with {conn.from_user.display_name}!')
    return redirect('networking')


@login_required
def collaborations_view(request):
    collabs = Collaboration.objects.all().order_by('-created_at')
    return render(request, 'campus/collaborations.html', {'collabs': collabs})
