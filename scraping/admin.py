from django.contrib import admin, messages
from django.utils import timezone
from .models import ScrapedItem, ScrapeLog
from opportunities.models import Opportunity
from django.contrib.auth import get_user_model

User = get_user_model()

@admin.register(ScrapedItem)
class ScrapedItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'company', 'source_name', 'source_type', 'sector', 'status', 'scraped_at']
    list_filter = ['status', 'source_type', 'sector', 'source_name', 'scraped_at']
    search_fields = ['title', 'company', 'description']
    readonly_fields = ['url_hash', 'scraped_at']
    actions = ['approve_and_import', 'reject_selected']

    @admin.action(description="Approve and import to platform")
    def approve_and_import(self, request, queryset):
        # 1. Ensure we have a system user to own these opportunities
        system_user, created = User.objects.get_or_create(
            username='gradpulse_bot',
            defaults={
                'email': 'bot@gradpulse.com',
                'portal_type': 'employer',
                'company_name': 'GradPulse Aggregator',
                'is_active': True
            }
        )

        imported_count = 0
        for item in queryset.filter(source_type='opportunities', status='pending'):
            # Check if already exists in Opportunity (using title and company as proxy if no URL field)
            # Actually, the prompt implies Opportunity should have a way to be uniquely identified.
            # I'll check if any Opportunity has the same title and description start.
            if not Opportunity.objects.filter(title=item.title, description__startswith=item.description[:100]).exists():
                Opportunity.objects.create(
                    company=system_user,
                    title=item.title,
                    type='internship', # Default to internship for scraped data
                    sector='Other', # Mapping sector might be complex, default to Other
                    location=item.location or 'Remote',
                    description=item.description or item.title,
                    deadline=item.deadline,
                    status='active'
                )
                item.status = 'imported'
                item.imported_at = timezone.now()
                item.imported_by = request.user
                item.save()
                imported_count += 1
        
        self.message_user(request, f"Successfully imported {imported_count} opportunities.", messages.SUCCESS)

    @admin.action(description="Reject selected items")
    def reject_selected(self, request, queryset):
        updated = queryset.update(status='rejected')
        self.message_user(request, f"{updated} items marked as rejected.", messages.INFO)

@admin.register(ScrapeLog)
class ScrapeLogAdmin(admin.ModelAdmin):
    list_display = ['source', 'status', 'items_found', 'items_saved', 'items_skipped', 'started_at']
    list_filter = ['status', 'source']
    readonly_fields = ['source', 'status', 'started_at', 'finished_at', 'items_found', 'items_saved', 'items_skipped', 'error_message']

    def has_add_permission(self, request): return False
    def has_change_permission(self, request, obj=None): return False
