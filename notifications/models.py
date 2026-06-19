from django.db import models
from django.conf import settings


class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                              related_name='notifications')
    message = models.CharField(max_length=500)
    link = models.CharField(max_length=300, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{'✓' if self.is_read else '✗'}] {self.user.username}: {self.message[:50]}"

    class Meta:
        ordering = ['-created_at']
