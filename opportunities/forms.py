from django import forms
from .models import Opportunity, Application


class OpportunityForm(forms.ModelForm):
    class Meta:
        model = Opportunity
        fields = ['title', 'type', 'sector', 'location', 'description', 'requirements',
                  'skills_required', 'stipend_min', 'stipend_max', 'deadline', 'status']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 6}),
            'requirements': forms.Textarea(attrs={'rows': 4}),
            'skills_required': forms.TextInput(attrs={'placeholder': 'Python, Django, SQL ...'}),
            'deadline': forms.DateInput(attrs={'type': 'date'}),
        }


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['cover_letter']
        widgets = {
            'cover_letter': forms.Textarea(attrs={'rows': 6, 'placeholder': 'Tell us why you are a great fit...'}),
        }
