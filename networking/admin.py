from django.contrib import admin
from .models import Connection, Collaboration, CollaborationMember


@admin.register(Connection)
class ConnectionAdmin(admin.ModelAdmin):
    list_display = ('from_user', 'to_user', 'status', 'created_at')
    list_filter = ('status',)
    list_editable = ('status',)
    search_fields = ('from_user__username', 'to_user__username')


class CollaborationMemberInline(admin.TabularInline):
    model = CollaborationMember
    extra = 0
    readonly_fields = ('joined_at',)


@admin.register(Collaboration)
class CollaborationAdmin(admin.ModelAdmin):
    list_display = ('title', 'creator_name', 'field', 'status', 'member_count', 'created_at')
    list_filter = ('status', 'field')
    search_fields = ('title', 'field')
    inlines = [CollaborationMemberInline]

    def creator_name(self, obj):
        return obj.creator.get_full_name() or obj.creator.username
    creator_name.short_description = 'Creator'

    def member_count(self, obj):
        return obj.members.count()
    member_count.short_description = 'Members'
