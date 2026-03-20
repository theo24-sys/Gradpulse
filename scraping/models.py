from django.db import models
from django.conf import settings
import hashlib

class ScrapedItem(models.Model):
    SOURCE_TYPES = [
        ('opportunities', 'Internships & Jobs'),
        ('events', 'Events'),
        ('youth_programs', 'Youth Programs'),
        ('credentials', 'Micro-Credentials'),
        ('qualifications', 'Professional Qualifications'),
        ('simulations', 'Simulation Scenarios'),
    ]
    
    SECTOR_CHOICES = [
        ('government', 'Government'),
        ('ngo', 'NGO'),
        ('private', 'Private'),
        ('public', 'Public'),
        ('international', 'International'),
        ('academic', 'Academic'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('imported', 'Imported'),
    ]

    source_name = models.CharField(max_length=200)
    source_type = models.CharField(max_length=50, choices=SOURCE_TYPES)
    sector = models.CharField(max_length=50, choices=SECTOR_CHOICES, default='private')
    
    title = models.CharField(max_length=500)
    company = models.CharField(max_length=255, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    
    url = models.URLField(max_length=1000)
    url_hash = models.CharField(max_length=32, unique=True, db_index=True)
    
    deadline = models.DateField(null=True, blank=True)
    salary = models.CharField(max_length=255, blank=True, null=True)
    job_type = models.CharField(max_length=255, blank=True, null=True)
    
    course_tags = models.JSONField(default=list, blank=True, help_text="List of relevant course names")
    year_tags = models.JSONField(default=list, blank=True, help_text="List of relevant year levels (1-4)")
    raw_data = models.JSONField(default=dict, blank=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    scraped_at = models.DateTimeField(auto_now_add=True)
    imported_at = models.DateTimeField(null=True, blank=True)
    imported_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        limit_choices_to={'portal_type': 'admin'} # Or user.is_staff in general
    )

    def save(self, *args, **kwargs):
        if not self.url_hash:
            self.url_hash = hashlib.md5(self.url.encode('utf-8')).hexdigest()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} ({self.source_name})"

    class Meta:
        ordering = ['-scraped_at']


class ScrapeLog(models.Model):
    source = models.CharField(max_length=200)
    status = models.CharField(max_length=50)
    started_at = models.DateTimeField()
    finished_at = models.DateTimeField(null=True, blank=True)
    
    items_found = models.IntegerField(default=0)
    items_saved = models.IntegerField(default=0)
    items_skipped = models.IntegerField(default=0)
    
    error_message = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.source} - {self.status} ({self.started_at})"

    class Meta:
        ordering = ['-started_at']
