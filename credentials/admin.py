from django.contrib import admin
from .models import Credential, Enrollment


@admin.register(Credential)
class CredentialAdmin(admin.ModelAdmin):
    list_display = ('name', 'provider', 'category', 'duration', 'enrollment_count')
    list_filter = ('provider', 'category')
    search_fields = ('name', 'provider', 'category')

    def enrollment_count(self, obj):
        return obj.enrollments.count()
    enrollment_count.short_description = 'Enrollments'


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student_name', 'credential_name', 'progress', 'is_completed', 'enrolled_at')
    list_filter = ('credential', 'progress')
    search_fields = ('student__first_name', 'student__last_name', 'credential__name')
    list_editable = ('progress',)

    def student_name(self, obj):
        return obj.student.get_full_name() or obj.student.username
    student_name.short_description = 'Student'

    def credential_name(self, obj):
        return obj.credential.name
    credential_name.short_description = 'Credential'

    def is_completed(self, obj):
        return obj.is_completed
    is_completed.boolean = True
    is_completed.short_description = 'Completed'
