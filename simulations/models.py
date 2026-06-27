from django.db import models
from django.conf import settings
import os
import zipfile
import logging

logger = logging.getLogger(__name__)

class MarketChallenge(models.Model):
    DIFFICULTY_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced')
    ]
    company_name = models.CharField(max_length=255)
    title = models.CharField(max_length=300)
    description = models.TextField()
    required_skills = models.TextField(help_text="Comma-separated skills")
    sector = models.CharField(max_length=100, blank=True)
    difficulty = models.CharField(choices=DIFFICULTY_CHOICES, max_length=20)
    adapt_build_zip = models.FileField(upload_to='adapt_build_zips/', blank=True, null=True)
    adapt_build_url = models.URLField(blank=True, max_length=500, help_text="URL to hosted Adapt HTML5 index.html")
    submitted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'portal_type': 'employer'}
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def extract_zip(self):
        if not self.adapt_build_zip:
            return
        try:
            zip_path = self.adapt_build_zip.path
            extract_dir = os.path.join(settings.MEDIA_ROOT, 'adapt_builds', f'challenge_{self.id}')
            os.makedirs(extract_dir, exist_ok=True)
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(extract_dir)
            
            # Construct the relative URL under MEDIA_URL
            relative_url = f"{settings.MEDIA_URL.rstrip('/')}/adapt_builds/challenge_{self.id}/index.html"
            # Update database directly to avoid recursive save triggers
            MarketChallenge.objects.filter(id=self.id).update(adapt_build_url=relative_url)
            self.adapt_build_url = relative_url
            logger.info(f"Successfully extracted Adapt zip for challenge ID {self.id}")
        except Exception as e:
            logger.error(f"Error extracting ZIP for challenge ID {self.id}: {e}")

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        file_changed = False
        if not is_new:
            try:
                old_instance = MarketChallenge.objects.get(pk=self.pk)
                if old_instance.adapt_build_zip != self.adapt_build_zip:
                    file_changed = True
            except MarketChallenge.DoesNotExist:
                pass
        else:
            file_changed = bool(self.adapt_build_zip)

        super().save(*args, **kwargs)

        if file_changed and self.adapt_build_zip:
            self.extract_zip()

    def __str__(self):
        return f"{self.title} ({self.company_name})"


class CourseObjective(models.Model):
    course_code = models.CharField(max_length=50, unique=True)
    course_title = models.CharField(max_length=300)
    objectives_keywords = models.TextField(help_text="Comma-separated keywords describing learning objectives")
    institution = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.course_code}: {self.course_title}"


class StudentSimulation(models.Model):
    STATUS_CHOICES = [
        ('assigned', 'Assigned'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed')
    ]
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='market_simulations'
    )
    challenge = models.ForeignKey(
        MarketChallenge,
        on_delete=models.CASCADE,
        related_name='student_assignments'
    )
    course_objective = models.ForeignKey(
        CourseObjective,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    adapt_config_json = models.JSONField(
        default=dict,
        blank=True,
        help_text="Configuration mapping for Adapt layout"
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='assigned')
    score_earned = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    matched_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.student.username} -> {self.challenge.title}"
