from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from django.utils import timezone
import json
from .models import StudentSimulation, MarketChallenge
from .ai_matching import generate_matched_scenarios

@login_required
def market_simulations_list(request):
    if not request.user.is_student:
        return redirect('corporate_dashboard')
    
    simulations = StudentSimulation.objects.filter(student=request.user).select_related('challenge', 'course_objective')
    
    assigned_count = simulations.filter(status='assigned').count()
    in_progress_count = simulations.filter(status='in_progress').count()
    completed_count = simulations.filter(status='completed').count()
    
    # Check if student has grades to suggest transcript upload
    has_grades = request.user.grades.exists()
    
    return render(request, 'campus/market_simulations.html', {
        'simulations': simulations,
        'assigned_count': assigned_count,
        'in_progress_count': in_progress_count,
        'completed_count': completed_count,
        'has_grades': has_grades,
    })

@login_required
def market_simulation_workspace(request, pk):
    if not request.user.is_student:
        return redirect('corporate_dashboard')
        
    simulation = get_object_or_404(StudentSimulation, pk=pk, student=request.user)
    
    if simulation.status == 'assigned':
        simulation.status = 'in_progress'
        simulation.save()
        
    return render(request, 'campus/market_simulation_workspace.html', {
        'simulation': simulation
    })

@login_required
@require_POST
def trigger_matching(request):
    if not request.user.is_student:
        return JsonResponse({'error': 'Unauthorized'}, status=403)
        
    student = request.user
    matches = generate_matched_scenarios(student)
    
    if matches:
        messages.success(request, f"AI matched {len(matches)} new market simulations for your courses!")
    else:
        messages.info(request, "No new matches found. Make sure you have transcript grades uploaded.")
        
    return redirect('market_simulations_list')

@login_required
@require_POST
def simulation_progress_update(request, pk):
    if not request.user.is_student:
        return JsonResponse({'error': 'Unauthorized'}, status=403)
        
    simulation = get_object_or_404(StudentSimulation, pk=pk, student=request.user)
    
    try:
        data = json.loads(request.body)
        score = data.get('score')
        status = data.get('status')
        
        if score is not None:
            simulation.score_earned = float(score)
            
        if status in ['assigned', 'in_progress', 'completed']:
            simulation.status = status
            if status == 'completed':
                simulation.completed_at = timezone.now()
                
        simulation.save()
        return JsonResponse({'status': 'success', 'score': float(simulation.score_earned or 0)})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
