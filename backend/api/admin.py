from django.contrib import admin
from .models import (
    Volunteer, Event, EventParticipation, Badge, VolunteerBadge,
    StudentProfile, FacultyProfile, StaffProfile, AlumniProfile,
    VolunteerContact, VolunteerAddress, VolunteerBackground,
    EmergencyContact, VolunteerMeta,
    Program, Subject, VolunteerBackgroundStatus,       
)

# Register your models here.
@admin.register(Volunteer)
class VolunteerAdmin(admin.ModelAdmin):
    list_display = ("full_name", "volunteer_identifier", "affiliation_type", "status")
    list_filter = ("affiliation_type", "status")
    search_fields = ("first_name", "last_name", "volunteer_identifier")

    @admin.display(description="Name")
    def full_name(self, obj):
        return obj.full_name
    
@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "is_active")
    list_filter = ("is_active",)
    search_fields = ("code", "name")


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "is_active")
    list_filter = ("is_active",)
    search_fields = ("code", "name")


@admin.register(VolunteerBackgroundStatus)
class VolunteerBackgroundStatusAdmin(admin.ModelAdmin):
    list_display = ("volunteer", "application_status", "wants_operations_group")
    list_filter = ("application_status", "wants_operations_group")

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