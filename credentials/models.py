from django.db import models
from django.conf import settings


class Credential(models.Model):
    provider = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    description = models.TextField()
    duration = models.CharField(max_length=100, blank=True, help_text='e.g. 6 weeks')
    category = models.CharField(max_length=100, blank=True)
    logo = models.ImageField(upload_to='credentials/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} by {self.provider}"

    class Meta:
        ordering = ['provider', 'name']


class Enrollment(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                 related_name='enrollments', limit_choices_to={'portal_type': 'student'})
    credential = models.ForeignKey(Credential, on_delete=models.CASCADE, related_name='enrollments')
    progress = models.PositiveIntegerField(default=0, help_text='0–100%')
    enrolled_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.student.username} → {self.credential.name}"

    @property
    def is_completed(self):
        return self.progress >= 100

    class Meta:
        unique_together = ('student', 'credential')


class Simulation(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=100, help_text="e.g. Finance, Tech, Health")
    difficulty = models.CharField(max_length=50, choices=[('Beginner', 'Beginner'), ('Intermediate', 'Intermediate'), ('Advanced', 'Advanced')])
    is_premium = models.BooleanField(default=False, help_text="Check if this requires a premium subscription")
    duration_minutes = models.PositiveIntegerField(default=30)
    
    # New fields for employer management
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, 
                                    related_name='created_simulations', null=True, blank=True,
                                    limit_choices_to={'portal_type': 'employer'})
    content_url = models.URLField(blank=True, help_text="Link to external scenario content or interactive video")
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({'Premium' if self.is_premium else 'Free'})"


class ProfessionalQualification(models.Model):
    title = models.CharField(max_length=200)
    provider = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=100, blank=True)
    duration = models.CharField(max_length=100, blank=True)
    link = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} — {self.provider}"

    class Meta:
        ordering = ['-created_at']
