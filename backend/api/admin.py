from django.contrib import admin
from .models import (
    Volunteer, Event, EventParticipation, Badge, VolunteerBadge,
    StudentProfile, FacultyProfile, StaffProfile, AlumniProfile,
    VolunteerContact, VolunteerAddress, VolunteerBackground,
    EmergencyContact, VolunteerMeta,
)

# Register your models here.
@admin.register(Volunteer)
class VolunteerAdmin(admin.ModelAdmin):
    list_display = ("name", "volunteer_identifier", "affiliation_type", "status")
    list_filter = ("affiliation_type", "status")
    search_fields = ("name", "volunteer_identifier")

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("name", "start_datetime", "end_datetime", "location")
    search_fields = ("name", "location")

@admin.register(EventParticipation)
class EventParticipationAdmin(admin.ModelAdmin):
    list_display = ("volunteer", "event", "status", "hours_rendered")
    list_filter = ("status",)

@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = ("name", "criteria_type")
    list_filter = ("criteria_type",)

@admin.register(VolunteerBadge)
class VolunteerBadgeAdmin(admin.ModelAdmin):
    list_display = ("volunteer", "badge", "event", "date_awarded")

admin.site.register(StudentProfile)
admin.site.register(FacultyProfile)
admin.site.register(StaffProfile)
admin.site.register(AlumniProfile)
admin.site.register(VolunteerContact)
admin.site.register(VolunteerAddress)
admin.site.register(VolunteerBackground)
admin.site.register(EmergencyContact)
admin.site.register(VolunteerMeta)