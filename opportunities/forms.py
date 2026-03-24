from django import forms
from .models import Opportunity, Application


class OpportunityForm(forms.ModelForm):
    class Meta:
        model = Opportunity
        fields = ['title', 'type', 'sector', 'location', 'external_company_name', 'description', 'requirements',
                  'skills_required', 'stipend_min', 'stipend_max', 'deadline', 'external_link', 'status']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 6}),
            'requirements': forms.Textarea(attrs={'rows': 4}),
            'skills_required': forms.TextInput(attrs={'placeholder': 'Python, Django, SQL ...'}),
            'deadline': forms.DateInput(attrs={'type': 'date'}),
            'external_link': forms.URLInput(attrs={'placeholder': 'https://example.com/apply'}),
            'external_company_name': forms.TextInput(attrs={'placeholder': 'E.g., Ministry of Health'}),
        }


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['cover_letter']
        widgets = {
            'cover_letter': forms.Textarea(attrs={'rows': 6, 'placeholder': 'Tell us why you are a great fit...'}),
        }
