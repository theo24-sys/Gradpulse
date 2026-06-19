from django.db import models
from django.conf import settings


class Event(models.Model):
    organizer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                   related_name='organized_events', null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=300)
    is_virtual = models.BooleanField(default=False)
    virtual_link = models.URLField(blank=True)
    image = models.ImageField(upload_to='events/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    @property
    def rsvp_count(self):
        return self.rsvps.count()

    class Meta:
        ordering = ['date']


class RSVP(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                 related_name='rsvps', limit_choices_to={'portal_type': 'student'})
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='rsvps')
    registered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username} → {self.event.title}"

    class Meta:
        unique_together = ('student', 'event')
