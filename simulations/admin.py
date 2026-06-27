from django.contrib import admin
from .models import MarketChallenge, CourseObjective, StudentSimulation

@admin.register(MarketChallenge)
class MarketChallengeAdmin(admin.ModelAdmin):
    list_display = ('title', 'company_name', 'sector', 'difficulty', 'is_active', 'created_at')
    list_filter = ('difficulty', 'sector', 'is_active')
    search_fields = ('title', 'company_name', 'description', 'required_skills')

@admin.register(CourseObjective)
class CourseObjectiveAdmin(admin.ModelAdmin):
    list_display = ('course_code', 'course_title', 'institution', 'created_at')
    list_filter = ('institution',)
    search_fields = ('course_code', 'course_title', 'objectives_keywords', 'institution')

@admin.register(StudentSimulation)
class StudentSimulationAdmin(admin.ModelAdmin):
    list_display = ('student_name', 'challenge_title', 'course_code', 'status', 'score_earned', 'matched_at')
    list_filter = ('status', 'challenge__difficulty')
    search_fields = ('student__first_name', 'student__last_name', 'student__username', 'challenge__title')
    list_editable = ('status', 'score_earned')

    def student_name(self, obj):
        return obj.student.get_full_name() or obj.student.username
    student_name.short_description = 'Student'

    def challenge_title(self, obj):
        return obj.challenge.title
    challenge_title.short_description = 'Market Challenge'

    def course_code(self, obj):
        return obj.course_objective.course_code if obj.course_objective else '—'
    course_code.short_description = 'Course Code'
