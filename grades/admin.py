from django.contrib import admin
from .models import Grade


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('student_name', 'unit_name', 'grade', 'grade_points_display', 'credit_hours', 'semester', 'year')
    list_filter = ('grade', 'year', 'semester')
    search_fields = ('student__first_name', 'student__last_name', 'unit_name')
    ordering = ('-year', 'semester')
    list_select_related = ['student']

    def student_name(self, obj):
        return obj.student.get_full_name() or obj.student.username
    student_name.short_description = 'Student'

    def grade_points_display(self, obj):
        return obj.grade_points
    grade_points_display.short_description = 'Grade Points'
