from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django import forms
from .models import Grade


class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ['unit_name', 'grade', 'credit_hours', 'semester', 'year']
        widgets = {'year': forms.NumberInput(attrs={'placeholder': '2025'})}


@login_required
def grades_view(request):
    if not request.user.is_student:
        return redirect('corporate_dashboard')
    if request.method == 'POST':
        form = GradeForm(request.POST)
        if form.is_valid():
            g = form.save(commit=False)
            g.student = request.user
            g.save()
            messages.success(request, 'Grade added.')
            return redirect('grades')
    else:
        form = GradeForm()
    grades = Grade.objects.filter(student=request.user).order_by('-year', 'semester')
    # Compute GPA
    total_points = sum(g.grade_points * g.credit_hours for g in grades)
    total_credits = sum(g.credit_hours for g in grades)
    gpa = round(total_points / total_credits, 2) if total_credits else 0.0
    # Update user gpa
    request.user.gpa = gpa
    request.user.save(update_fields=['gpa'])
    # Chart data: per year average
    return render(request, 'campus/grades.html', {'form': form, 'grades': grades, 'gpa': gpa})
