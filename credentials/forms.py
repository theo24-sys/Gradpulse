from django import forms
from .models import Simulation

class SimulationForm(forms.ModelForm):
    class Meta:
        model = Simulation
        fields = ['title', 'description', 'category', 'difficulty', 'duration_minutes']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }
