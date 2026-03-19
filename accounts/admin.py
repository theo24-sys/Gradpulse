from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'get_full_name', 'portal_type', 'institution_or_company',
                    'is_verified', 'open_to_work', 'is_active', 'created_at', 'photo_preview')
    list_filter = ('portal_type', 'is_verified', 'open_to_work', 'is_active', 'is_staff', 'sector')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'company_name', 'institution')
    ordering = ('-created_at',)
    list_per_page = 25
    list_editable = ('is_verified', 'open_to_work', 'is_active')
    date_hierarchy = 'created_at'

    fieldsets = UserAdmin.fieldsets + (
        ('Portal & Status', {
            'fields': ('portal_type', 'is_verified', 'profile_photo', 'bio', 'phone', 'location'),
        }),
        ('Student Info', {
            'classes': ('collapse',),
            'fields': ('institution', 'course', 'year_of_study', 'graduation_year',
                       'gpa', 'skills', 'linkedin_url', 'github_url', 'portfolio_url', 'open_to_work'),
        }),
        ('Employer Info', {
            'classes': ('collapse',),
            'fields': ('company_name', 'company_logo', 'sector', 'company_size',
                       'kra_pin', 'website', 'company_about', 'actively_hiring'),
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'portal_type', 'password1', 'password2'),
        }),
    )

    def institution_or_company(self, obj):
        return obj.company_name if obj.is_employer else obj.institution
    institution_or_company.short_description = 'Institution / Company'

    def photo_preview(self, obj):
        img = obj.company_logo if obj.is_employer else obj.profile_photo
        if img:
            return format_html('<img src="{}" style="width:36px;height:36px;border-radius:50%;object-fit:cover;">', img.url)
        return '—'
    photo_preview.short_description = 'Photo'

    actions = ['verify_users', 'unverify_users']

    def verify_users(self, request, queryset):
        queryset.update(is_verified=True)
        self.message_user(request, f"{queryset.count()} user(s) verified.")
    verify_users.short_description = '✔ Verify selected users'

    def unverify_users(self, request, queryset):
        queryset.update(is_verified=False)
        self.message_user(request, f"{queryset.count()} user(s) unverified.")
    unverify_users.short_description = '✖ Unverify selected users'
