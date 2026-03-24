from django.contrib import admin
from django.utils.html import format_html
from .models import Opportunity, Application


class ApplicationInline(admin.TabularInline):
    model = Application
    extra = 0
    fields = ('student', 'status', 'applied_at')
    readonly_fields = ('student', 'applied_at')
    can_delete = False


@admin.register(Opportunity)
class OpportunityAdmin(admin.ModelAdmin):
    list_display = ('title', 'company_name', 'type', 'sector', 'location', 'status',
                    'application_count_display', 'deadline', 'created_at')
    list_filter = ('type', 'sector', 'status')
    search_fields = ('title', 'company__company_name', 'location', 'skills_required')
    list_editable = ('status',)
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'
    inlines = [ApplicationInline]
    readonly_fields = ('views_count', 'created_at', 'updated_at')

    fieldsets = (
        ('Overview', {'fields': ('company', 'external_company_name', 'title', 'type', 'sector', 'status', 'poster')}),
        ('Details', {'fields': ('description', 'requirements', 'skills_required', 'location', 'deadline', 'external_link')}),
        ('Compensation', {'fields': ('stipend_min', 'stipend_max')}),
        ('Metrics', {'fields': ('views_count', 'created_at', 'updated_at'), 'classes': ('collapse',)}),
    )

    def company_name(self, obj):
        return obj.external_company_name or (obj.company.company_name if obj.company else '') or getattr(obj.company, 'username', 'External')
    company_name.short_description = 'Company'

    def application_count_display(self, obj):
        count = obj.application_count
        color = 'green' if count > 0 else 'gray'
        return format_html('<span style="color:{}; font-weight:bold;">{}</span>', color, count)
    application_count_display.short_description = 'Applications'


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('student_name', 'opportunity_title', 'company_name', 'status', 'applied_at', 'status_badge')
    list_filter = ('status', 'opportunity__type', 'opportunity__sector')
    search_fields = ('student__first_name', 'student__last_name', 'opportunity__title')
    list_editable = ('status',)
    ordering = ('-applied_at',)
    date_hierarchy = 'applied_at'
    readonly_fields = ('applied_at', 'updated_at')

    def student_name(self, obj):
        return obj.student.get_full_name() or obj.student.username
    student_name.short_description = 'Student'

    def opportunity_title(self, obj):
        return obj.opportunity.title
    opportunity_title.short_description = 'Opportunity'

    def company_name(self, obj):
        return obj.opportunity.company.company_name or obj.opportunity.company.username
    company_name.short_description = 'Company'

    STATUS_COLORS = {
        'pending': '#6c757d', 'shortlisted': '#0d6efd', 'rejected': '#dc3545',
        'hired': '#198754', 'withdrawn': '#ffc107',
    }

    def status_badge(self, obj):
        color = self.STATUS_COLORS.get(obj.status, '#6c757d')
        return format_html(
            '<span style="background:{};color:white;padding:2px 10px;border-radius:12px;font-size:12px;">{}</span>',
            color, obj.get_status_display()
        )
    status_badge.short_description = 'Status'

    actions = ['mark_shortlisted', 'mark_rejected', 'mark_hired']

    def mark_shortlisted(self, request, qs):
        qs.update(status='shortlisted')
    mark_shortlisted.short_description = '→ Mark as Shortlisted'

    def mark_rejected(self, request, qs):
        qs.update(status='rejected')
    mark_rejected.short_description = '→ Mark as Rejected'

    def mark_hired(self, request, qs):
        qs.update(status='hired')
    mark_hired.short_description = '→ Mark as Hired'
