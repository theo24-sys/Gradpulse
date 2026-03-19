from django.contrib import admin
from .models import Event, RSVP


class RSVPInline(admin.TabularInline):
    model = RSVP
    extra = 0
    readonly_fields = ('student', 'registered_at')
    can_delete = False


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'location', 'is_virtual', 'rsvp_count_display', 'organizer_name')
    list_filter = ('is_virtual', 'date')
    search_fields = ('title', 'location')
    inlines = [RSVPInline]
    readonly_fields = ('created_at',)

    def rsvp_count_display(self, obj):
        return obj.rsvp_count
    rsvp_count_display.short_description = 'RSVPs'

    def organizer_name(self, obj):
        return obj.organizer.get_full_name() if obj.organizer else '—'
    organizer_name.short_description = 'Organizer'


@admin.register(RSVP)
class RSVPAdmin(admin.ModelAdmin):
    list_display = ('student_name', 'event_title', 'registered_at')
    list_filter = ('event',)
    search_fields = ('student__first_name', 'student__last_name', 'event__title')

    def student_name(self, obj):
        return obj.student.get_full_name() or obj.student.username
    student_name.short_description = 'Student'

    def event_title(self, obj):
        return obj.event.title
    event_title.short_description = 'Event'
