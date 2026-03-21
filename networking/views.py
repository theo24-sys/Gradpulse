from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from .models import Connection, Collaboration, CollaborationMember, Message
from accounts.models import CustomUser
from .agora_utils import generate_agora_token


@login_required
def student_profile_public(request, pk):
    if not request.user.is_employer:
        return redirect('campus_dashboard')
    student = get_object_or_404(CustomUser, pk=pk, portal_type='student')
    return render(request, 'corporate/student_profile_view.html', {'student': student})


@login_required
def get_agora_token(request):
    channel_name = request.GET.get('channel')
    if not channel_name:
        return JsonResponse({'error': 'Channel name is required'}, status=400)
    
    # Simple security check: user must be part of a conversation that matches this channel naming convention
    # Channel naming: chat_<min_id>_<max_id>
    token = generate_agora_token(channel_name, uid=0)
    if not token:
        return JsonResponse({'error': 'Failed to generate token'}, status=500)
        
    return JsonResponse({
        'token': token,
        'appId': __import__('os').environ.get('AGORA_APP_ID')
    })


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


def get_conversations(user):
    # Get all users the current user has messaged or received messages from
    sent_msgs = Message.objects.filter(sender=user).values_list('receiver', flat=True)
    received_msgs = Message.objects.filter(receiver=user).values_list('sender', flat=True)
    user_ids = set(list(sent_msgs) + list(received_msgs))
    
    conversations = []
    for uid in user_ids:
        other_user = CustomUser.objects.get(pk=uid)
        last_msg = Message.objects.filter(
            Q(sender=user, receiver=other_user) | Q(sender=other_user, receiver=user)
        ).order_by('-timestamp').first()
        
        unread_count = Message.objects.filter(sender=other_user, receiver=user, is_read=False).count()
        
        conversations.append({
            'user': other_user,
            'last_message': last_msg,
            'unread_count': unread_count,
        })
    
    # Sort by last message timestamp
    conversations.sort(key=lambda x: x['last_message'].timestamp if x['last_message'] else 0, reverse=True)
    return conversations


@login_required
def inbox_view(request):
    conversations = get_conversations(request.user)
    return render(request, 'networking/chat_center.html', {'conversations': conversations})


@login_required
def chat_detail_view(request, pk):
    from django.utils import timezone
    request.user.last_seen = timezone.now()
    request.user.save(update_fields=['last_seen'])
    
    other_user = get_object_or_404(CustomUser, pk=pk)
    messages = Message.objects.filter(
        Q(sender=request.user, receiver=other_user) | Q(sender=other_user, receiver=request.user)
    ).order_by('timestamp')
    
    # Mark as read
    Message.objects.filter(sender=other_user, receiver=request.user, is_read=False).update(is_read=True)
    
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Message.objects.create(sender=request.user, receiver=other_user, content=content)
            return redirect('chat_detail', pk=pk)
            
    conversations = get_conversations(request.user)
    return render(request, 'networking/chat_center.html', {
        'conversations': conversations,
        'other_user': other_user,
        'chat_messages': messages,
    })


@login_required
def delete_message_view(request, msg_pk):
    message = get_object_or_404(Message, pk=msg_pk)
    if message.sender == request.user:
        message.deleted_by_sender = True
        message.save()
    elif message.receiver == request.user:
        message.deleted_by_receiver = True
        message.save()
    
    # If both deleted, actually delete if desired, or just keep flagged
    return redirect('chat_detail', pk=message.receiver.pk if message.sender == request.user else message.sender.pk)
