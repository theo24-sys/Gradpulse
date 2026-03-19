from django import forms
from .models import Simulation

class SimulationForm(forms.ModelForm):
    class Meta:
        model = Simulation
        fields = ['title', 'description', 'category', 'difficulty', 'duration_minutes', 'content_url']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'content_url': forms.URLInput(attrs={'placeholder': 'https://example.com/scenario-data'}),
        }
