from django.db import models
from django.conf import settings
from decimal import Decimal


class Grade(models.Model):
    GRADE_CHOICES = [
        ('A', 'A'), ('A-', 'A-'), ('B+', 'B+'), ('B', 'B'), ('B-', 'B-'),
        ('C+', 'C+'), ('C', 'C'), ('C-', 'C-'), ('D+', 'D+'), ('D', 'D'), ('E', 'E / F'),
    ]
    GRADE_POINTS = {
        'A': 4.0, 'A-': 3.7, 'B+': 3.3, 'B': 3.0, 'B-': 2.7,
        'C+': 2.3, 'C': 2.0, 'C-': 1.7, 'D+': 1.3, 'D': 1.0, 'E': 0.0,
    }

    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                 related_name='grades', limit_choices_to={'portal_type': 'student'})
    unit_name = models.CharField(max_length=200)
    grade = models.CharField(max_length=3, choices=GRADE_CHOICES)
    credit_hours = models.PositiveIntegerField(default=3)
    semester = models.CharField(max_length=20, blank=True)
    year = models.PositiveIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username} — {self.unit_name} ({self.grade})"

    @property
    def grade_points(self):
        return self.GRADE_POINTS.get(self.grade, 0.0)

    class Meta:
        ordering = ['-year', 'semester', 'unit_name']
