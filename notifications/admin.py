from django.contrib import admin
from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'message_short', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    list_editable = ('is_read',)
    search_fields = ('user__username', 'message')
    ordering = ('-created_at',)

    def message_short(self, obj):
        return obj.message[:60] + '...' if len(obj.message) > 60 else obj.message
    message_short.short_description = 'Message'

    actions = ['mark_all_read']

    def mark_all_read(self, request, qs):
        qs.update(is_read=True)
    mark_all_read.short_description = '✓ Mark as read'
