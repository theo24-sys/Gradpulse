import os
from urllib.parse import quote
from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    PORTAL_STUDENT = 'student'
    PORTAL_EMPLOYER = 'employer'
    PORTAL_UNISMART = 'unismart'
    PORTAL_CHOICES = [
        (PORTAL_STUDENT, 'Student'),
        (PORTAL_EMPLOYER, 'Employer'),
        (PORTAL_UNISMART, 'UniSmart (High School & Careers)'),
    ]

    # UniSmart Categories
    CAT_JSS = 'jss'
    CAT_SSS = 'sss'
    CAT_GRADUATE = 'graduate'
    CATEGORY_CHOICES = [
        (CAT_JSS, 'Junior Secondary (Grade 7-9)'),
        (CAT_SSS, 'Senior Secondary (Form 1-4)'),
        (CAT_GRADUATE, 'KCSE Graduate'),
    ]

    portal_type = models.CharField(max_length=20, choices=PORTAL_CHOICES, default=PORTAL_STUDENT)
    
    # UniSmart specific fields
    student_category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, blank=True, null=True)
    grade_level = models.CharField(max_length=50, blank=True, null=True, help_text="e.g. Grade 7, Form 4")
    target_career = models.CharField(max_length=200, blank=True, null=True)

    # Common fields
    profile_photo = models.ImageField(upload_to='profiles/', blank=True, null=True)
    bio = models.TextField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    location = models.CharField(max_length=100, blank=True)
    is_verified = models.BooleanField(default=False)
    is_premium = models.BooleanField(default=False)
    is_mentor = models.BooleanField(default=False, help_text="Available to mentor UniSmart students")

    # Student fields
    admission_number = models.CharField(max_length=50, blank=True, null=True, unique=True)
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
    last_seen = models.DateTimeField(null=True, blank=True)

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

    @property
    def is_unismart(self):
        return self.portal_type == self.PORTAL_UNISMART

    @property
    def is_online(self):
        if self.last_seen:
            from django.utils import timezone
            from datetime import timedelta
            return self.last_seen > timezone.now() - timedelta(minutes=5)
        return False

    def get_avatar_url(self):
        if self.profile_photo:
            try:
                if self.profile_photo.storage.exists(self.profile_photo.name):
                    return self.profile_photo.url
            except Exception:
                pass
        
        name_param = quote(self.display_name)
        return f"https://ui-avatars.com/api/?name={name_param}&background=008b8b&color=fff&size=128"

    def get_logo_url(self):
        if self.company_logo:
            try:
                if self.company_logo.storage.exists(self.company_logo.name):
                    return self.company_logo.url
            except Exception:
                pass
        
        name_param = quote(self.company_name or self.username)
        return f"https://ui-avatars.com/api/?name={name_param}&background=00ced1&color=fff&size=128"

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'


class UniSmartResource(models.Model):
    RESOURCE_TYPES = [
        ('pdf', 'PDF Document'),
        ('link', 'External Link'),
        ('video', 'Video Guide'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    resource_type = models.CharField(max_length=20, choices=RESOURCE_TYPES, default='pdf')
    file = models.FileField(upload_to='unismart/resources/', blank=True, null=True)
    url = models.URLField(blank=True, null=True, help_text="Link if not a file")
    
    category = models.CharField(max_length=20, choices=CustomUser.CATEGORY_CHOICES)
    is_active = models.BooleanField(default=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.get_category_display()})"

    class Meta:
        ordering = ['-uploaded_at']
