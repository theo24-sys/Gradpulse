from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Credential, Enrollment, Simulation


@login_required
def credentials_list(request):
    credentials = Credential.objects.all()
    enrolled_ids = []
    if request.user.is_student:
        enrolled_ids = list(Enrollment.objects.filter(student=request.user).values_list('credential_id', flat=True))
    return render(request, 'campus/credentials.html', {'credentials': credentials, 'enrolled_ids': enrolled_ids})


@login_required
def enroll_credential(request, pk):
    if not request.user.is_student:
        return redirect('home')
    credential = get_object_or_404(Credential, pk=pk)
    Enrollment.objects.get_or_create(student=request.user, credential=credential)
    messages.success(request, f'Enrolled in "{credential.name}"!')
    return redirect('credentials_list')


@login_required
def simulations_list(request):
    simulations = Simulation.objects.all().order_by('-created_at')
    return render(request, 'campus/simulations.html', {'simulations': simulations})


@login_required
def premium_upgrade(request):
    """
    Mock payment gateway endpoint for Premium Upgrades (Stripe/Mpesa placeholder).
    """
    if request.method == 'POST':
        # Here we would normally redirect to Stripe Checkout or initiate Mpesa STK Push
        request.user.is_premium = True
        request.user.save()
        messages.success(request, 'Payment successful! You are now a Premium member.')
        return redirect('simulations_list')
        
    return render(request, 'campus/premium_upgrade.html')
