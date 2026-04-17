from django.db import models
from django.conf import settings


class Opportunity(models.Model):
    TYPE_CHOICES = [
        ('internship', 'Internship'),
        ('job', 'Full-time Job'),
        ('part_time', 'Part-time'),
        ('freelance', 'Freelance'),
        ('attachment', 'Industrial Attachment'),
        ('volunteer', 'Volunteer'),
        ('funding', 'Funding / Grants / Loans'),
    ]
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('closed', 'Closed'),
        ('draft', 'Draft'),
    ]
    SECTOR_CHOICES = [
        ('Technology', 'Technology'), ('Finance', 'Finance'), ('Healthcare', 'Healthcare'),
        ('Education', 'Education'), ('Manufacturing', 'Manufacturing'), ('Agriculture', 'Agriculture'),
        ('Media', 'Media'), ('Consulting', 'Consulting'), ('NGO', 'NGO'), ('Government', 'Government'), ('Other', 'Other'),
    ]

    company = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                 related_name='opportunities', limit_choices_to={'portal_type': 'employer'}, null=True, blank=True)
    external_company_name = models.CharField(max_length=200, blank=True, help_text="Name of organization if not registered on GradPulse")
    title = models.CharField(max_length=200)
    poster = models.ImageField(upload_to='opportunities/posters/', blank=True, null=True)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='internship')
    sector = models.CharField(max_length=100, choices=SECTOR_CHOICES)
    location = models.CharField(max_length=200)
    description = models.TextField()
    requirements = models.TextField(blank=True)
    skills_required = models.CharField(max_length=500, blank=True, help_text='Comma-separated')
    stipend_min = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    stipend_max = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    deadline = models.DateField(null=True, blank=True)
    external_link = models.URLField(blank=True, help_text="Link to apply externally if not using GradPulse")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    views_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} — {self.display_company_name}"

    @property
    def display_company_name(self):
        return self.external_company_name or (self.company.company_name if self.company else '') or getattr(self.company, 'username', 'External')

    def get_skills_list(self):
        return [s.strip() for s in self.skills_required.split(',') if s.strip()]

    @property
    def application_count(self):
        return self.applications.count()

    class Meta:
        verbose_name_plural = 'Opportunities'
        ordering = ['-created_at']


class Application(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('shortlisted', 'Shortlisted'),
        ('rejected', 'Rejected'),
        ('hired', 'Hired'),
        ('withdrawn', 'Withdrawn'),
    ]

    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                 related_name='applications', limit_choices_to={'portal_type': 'student'})
    opportunity = models.ForeignKey(Opportunity, on_delete=models.CASCADE, related_name='applications')
    cover_letter = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    applied_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    notes = models.TextField(blank=True, help_text='Internal employer notes')

    def __str__(self):
        return f"{self.student.display_name} → {self.opportunity.title}"

    class Meta:
        unique_together = ('student', 'opportunity')
class YouthProgram(models.Model):
    title = models.CharField(max_length=200)
    organization = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200, blank=True)
    category = models.CharField(max_length=100, blank=True)
    deadline = models.DateField(null=True, blank=True)
    link = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} by {self.organization}"

    class Meta:
        ordering = ['-created_at']
