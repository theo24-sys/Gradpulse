from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import ProgrammingError
from django.shortcuts import get_object_or_404, redirect, render
from .forms import SimulationForm
from accounts.ai_utils import generate_simulation_scenario
from .models import Credential, Enrollment, Simulation
from scraping.utils import get_items_for_student


@login_required
def credentials_list(request):
    credentials = Credential.objects.all()
    enrolled_ids = []
    if request.user.is_student:
        enrolled_ids = list(Enrollment.objects.filter(student=request.user).values_list('credential_id', flat=True))
    
    # NEW: Fetch live discoveries from scrapers (IBM, Microsoft, etc.)
    discoveries = get_items_for_student(student=request.user, source_type='credentials', limit=12)
    
    return render(request, 'campus/credentials.html', {
        'credentials': credentials, 
        'enrolled_ids': enrolled_ids,
        'discoveries': discoveries
    })


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
    try:
        simulations = Simulation.objects.all().order_by('-created_at')
        # Force evaluation
        list(simulations[:1])
    except ProgrammingError:
        simulations = []
        
    # NEW: Fetch live discoveries from scrapers
    discoveries = get_items_for_student(student=request.user, source_type='simulations', limit=12)
    
    return render(request, 'campus/simulations.html', {
        'simulations': simulations,
        'discoveries': discoveries
    })


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


@login_required
def manage_simulations(request):
    if not (request.user.is_employer or request.user.is_superuser):
        return redirect('home')
    if request.user.is_superuser:
        simulations = Simulation.objects.all()
    else:
        simulations = Simulation.objects.filter(created_by=request.user)
    return render(request, 'corporate/manage_simulations.html', {'simulations': simulations})


@login_required
def simulation_create(request):
    if not (request.user.is_employer or request.user.is_superuser):
        return redirect('home')
    if request.method == 'POST':
        form = SimulationForm(request.POST)
        if form.is_valid():
            simulation = form.save(commit=False)
            simulation.created_by = request.user
            simulation.is_premium = True  # Enforce premium status for platform income
            simulation.save()
            messages.success(request, 'Simulation created successfully!')
            return redirect('manage_simulations')
    else:
        form = SimulationForm()
    return render(request, 'corporate/simulation_form.html', {'form': form, 'title': 'Create Simulation'})

@login_required
def simulation_generate_ai(request):
    if not (request.user.is_employer or request.user.is_superuser):
        return redirect('home')

    if request.method == 'POST':
        topic = request.POST.get('topic')
        if topic:
            from .tasks import generate_simulation_ai_task
            generate_simulation_ai_task.delay(topic, request.user.id)
            messages.success(request, f"AI is generating a simulation for '{topic}'. It will appear in your list in ~30 seconds.")
            return redirect('manage_simulations')

    return render(request, 'corporate/simulation_ai_form.html')


@login_required
def simulation_play(request, pk):
    simulation = get_object_or_404(Simulation, pk=pk)
    
    # Premium check
    if simulation.is_premium and not request.user.is_premium:
        messages.warning(request, "This is a Premium simulation. Please upgrade to access.")
        return redirect('premium_upgrade')
        
    if simulation.is_ai_generated:
        return render(request, 'campus/simulation_play.html', {'simulation': simulation})
    
    messages.error(request, "This simulation has no interactive content.")
    return redirect('simulations_list')


def qualifications_list(request):
    from .models import ProfessionalQualification
    try:
        quals = ProfessionalQualification.objects.all().order_by('-created_at')
        # Force evaluation
        list(quals[:1])
    except ProgrammingError:
        quals = []
        
    # NEW: Fetch live discoveries from scrapers
    discoveries = get_items_for_student(student=request.user, source_type='qualifications', limit=12)
    
    return render(request, 'campus/qualifications.html', {
        'qualifications': quals,
        'discoveries': discoveries
    })
