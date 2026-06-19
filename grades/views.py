from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django import forms
from .models import Grade
from .utils import extract_text_from_pdf, parse_transcript_with_ai


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


@login_required
def upload_transcript(request):
    if not request.user.is_student:
        return redirect('corporate_dashboard')
        
    if request.method == 'POST' and request.FILES.get('transcript'):
        pdf_file = request.FILES['transcript']
        
        # 1. Extract Text
        text = extract_text_from_pdf(pdf_file)
        if not text:
            messages.error(request, 'Could not extract text from the PDF. Is it an image or scanned document?')
            return redirect('grades')
            
        # 2. Extract Data via OpenAI
        grades_data = parse_transcript_with_ai(text)
        if not grades_data:
            messages.error(request, 'AI could not parse sufficient academic grades from the document.')
            return redirect('grades')
            
        # 3. Create Records
        count = 0
        for item in grades_data:
            try:
                credit = int(item.get('credit_hours', 3))
            except (ValueError, TypeError):
                credit = 3
                
            y = item.get('year')
            year_val = y if isinstance(y, int) else None
            
            Grade.objects.create(
                student=request.user,
                unit_name=str(item.get('unit_name', 'Unknown'))[:200],
                grade=str(item.get('grade', 'C'))[:3],
                credit_hours=credit,
                semester=str(item.get('semester', ''))[:20],
                year=year_val
            )
            count += 1
            
        messages.success(request, f'Successfully extracted and auto-filled {count} grades from your transcript!')
        
    return redirect('grades')
