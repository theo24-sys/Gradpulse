from django.db import models
from django.conf import settings

class LibraryItem(models.Model):
    CATEGORY_CHOICES = [
        ('book', 'Book / E-Book'),
        ('outline', 'Course Outline'),
        ('past_paper', 'Past Paper'),
        ('notes', 'Study Notes'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='book')
    file = models.FileField(upload_to='library/', help_text="Upload PDFs, Docs, or Images")
    external_link = models.URLField(blank=True, help_text="Optional link to external resource")
    
    uploader = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='uploaded_resources')
    institution = models.CharField(max_length=200, blank=True, help_text="Specify institution if relevant")
    course_name = models.CharField(max_length=200, blank=True, help_text="Specify course if relevant")
    
    is_public = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.title} ({self.get_category_display()})"
    
    class Meta:
        ordering = ['-created_at']
