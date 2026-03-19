from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    PORTAL_STUDENT = 'student'
    PORTAL_EMPLOYER = 'employer'
    PORTAL_CHOICES = [
        (PORTAL_STUDENT, 'Student'),
        (PORTAL_EMPLOYER, 'Employer'),
    ]

    portal_type = models.CharField(max_length=20, choices=PORTAL_CHOICES, default=PORTAL_STUDENT)

    # Common fields
    profile_photo = models.ImageField(upload_to='profiles/', blank=True, null=True)
    bio = models.TextField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    location = models.CharField(max_length=100, blank=True)
    is_verified = models.BooleanField(default=False)
    is_premium = models.BooleanField(default=False)

    # Student fields
    institution = models.CharField(max_length=200, blank=True)
    course = models.CharField(max_length=200, blank=True)
    year_of_study = models.PositiveIntegerField(null=True, blank=True)
    graduation_year = models.PositiveIntegerField(null=True, blank=True)
    skills = models.TextField(blank=True, help_text='Comma-separated skills')
    linkedin_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    portfolio_url = models.URLField(blank=True)
    open_to_work = models.BooleanField(default=True)
    gpa = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)

    # Employer fields
    company_name = models.CharField(max_length=200, blank=True)
    company_logo = models.ImageField(upload_to='logos/', blank=True, null=True)
    sector = models.CharField(max_length=100, blank=True)
    company_size = models.CharField(max_length=50, blank=True)
    kra_pin = models.CharField(max_length=50, blank=True)
    website = models.URLField(blank=True)
    company_about = models.TextField(blank=True)
    actively_hiring = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.portal_type == self.PORTAL_EMPLOYER:
            return f"{self.company_name or self.get_full_name()} (Employer)"
        return f"{self.get_full_name()} ({self.institution or 'Student'})"

    def get_skills_list(self):
        return [s.strip() for s in self.skills.split(',') if s.strip()]

    @property
    def display_name(self):
        return self.get_full_name() or self.username

    @property
    def is_student(self):
        return self.portal_type == self.PORTAL_STUDENT

    @property
    def is_employer(self):
        return self.portal_type == self.PORTAL_EMPLOYER

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
