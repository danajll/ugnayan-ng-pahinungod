from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum

# Create your models here.

# -- CHOICES FOR CORE ATTRIBUTES --

class AffiliationType(models.TextChoices):
    STUDENT = "student", "Student"
    FACULTY = "faculty", "Faculty"
    STAFF = "staff", "Staff"
    ALUMNI = "alumni", "Alumni"


class VolunteerStatus(models.TextChoices):
    ACTIVE = "active", "Active"
    INACTIVE = "inactive", "Inactive"
    SUSPENDED = "suspended", "Suspended"


class BadgeCriteriaType(models.TextChoices):
    HOURS = "hours", "Hours-based"
    EVENT_COUNT = "event_count", "Event count-based"
    MANUAL = "manual", "Manually awarded"


class ParticipationStatus(models.TextChoices):
    REGISTERED = "registered", "Registered"
    ATTENDED = "attended", "Attended"
    CANCELLED = "cancelled", "Cancelled"
    NO_SHOW = "no_show", "No-show"


# -- CORE MODELS --
# Core entities including Volunteer, Events, Badge
# Tables linking entities EventParticipation, VolunteerBadge

class Volunteer(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="volunteer",
    )
    volunteer_identifier = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=200)
    sex = models.CharField(max_length=20, blank=True)
    birthdate = models.DateField(null=True, blank=True)
    affiliation_type = models.CharField(
        max_length=20,
        choices=AffiliationType.choices,
    )
    status = models.CharField(
        max_length=20,
        choices=VolunteerStatus.choices,
        default=VolunteerStatus.ACTIVE,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.volunteer_identifier})"

    @property
    def service_hours(self):
        """Total hours across all attended events."""
        result = self.event_participations.filter(
            status=ParticipationStatus.ATTENDED,
        ).aggregate(total=Sum("hours_rendered"))["total"]
        return result or 0


class Event(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    location = models.CharField(max_length=300, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.start_datetime.date()})"


class EventParticipation(models.Model):
    volunteer = models.ForeignKey(
        Volunteer,
        on_delete=models.CASCADE,
        related_name="event_participations",
    )
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name="participations",
    )
    status = models.CharField(
        max_length=20,
        choices=ParticipationStatus.choices,
        default=ParticipationStatus.REGISTERED,
    )
    hours_rendered = models.IntegerField(default=0)
    registered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("volunteer", "event")

    def __str__(self):
        return f"{self.volunteer.name} @ {self.event.name} — {self.status}"


class Badge(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    icon_url = models.URLField(blank=True)
    criteria_type = models.CharField(
        max_length=20,
        choices=BadgeCriteriaType.choices,
        default=BadgeCriteriaType.MANUAL,
    )

    def __str__(self):
        return self.name


class VolunteerBadge(models.Model):
    volunteer = models.ForeignKey(
        Volunteer,
        on_delete=models.CASCADE,
        related_name="badges",
    )
    badge = models.ForeignKey(
        Badge,
        on_delete=models.CASCADE,
        related_name="awarded_to",
    )
    event = models.ForeignKey(
        Event,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="badges_awarded",
    )
    date_awarded = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("volunteer", "badge")

    def __str__(self):
        return f"{self.volunteer.name} — {self.badge.name}"


# -- PROFILE TABLES -- 
# One-to-One Relationship with Volunteers 
# A volunteer account falls into either one of these categories

class StudentProfile(models.Model):
    volunteer = models.OneToOneField(
        Volunteer, on_delete=models.CASCADE, related_name="student_profile",
    )
    student_number = models.CharField(max_length=50, unique=True)
    course = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.volunteer.name} — {self.student_number}"


class FacultyProfile(models.Model):
    volunteer = models.OneToOneField(
        Volunteer, on_delete=models.CASCADE, related_name="faculty_profile",
    )
    employee_id = models.CharField(max_length=50, unique=True)
    department = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.volunteer.name} — {self.employee_id}"


class StaffProfile(models.Model):
    volunteer = models.OneToOneField(
        Volunteer, on_delete=models.CASCADE, related_name="staff_profile",
    )
    employee_id = models.CharField(max_length=50, unique=True)
    office = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.volunteer.name} — {self.employee_id}"


class AlumniProfile(models.Model):
    volunteer = models.OneToOneField(
        Volunteer, on_delete=models.CASCADE, related_name="alumni_profile",
    )
    degree_obtained = models.CharField(max_length=200)
    year_graduated = models.IntegerField()

    def __str__(self):
        return f"{self.volunteer.name} — {self.year_graduated}"


# VOLUNTEER DETAIL TABLES 
# One-to-One with Volunteer 
# Volunteers have all of information stored

class VolunteerContact(models.Model):
    volunteer = models.OneToOneField(
        Volunteer, on_delete=models.CASCADE, related_name="contact",
    )
    phone_number = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.volunteer.name} — {self.phone_number}"


class VolunteerAddress(models.Model):
    volunteer = models.OneToOneField(
        Volunteer, on_delete=models.CASCADE, related_name="address",
    )
    street_address = models.CharField(max_length=300)
    city = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.volunteer.name} — {self.city}"


class VolunteerBackground(models.Model):
    volunteer = models.OneToOneField(
        Volunteer, on_delete=models.CASCADE, related_name="background",
    )
    skills = models.TextField(blank=True)

    def __str__(self):
        return f"{self.volunteer.name} — background"


class EmergencyContact(models.Model):
    volunteer = models.OneToOneField(
        Volunteer, on_delete=models.CASCADE, related_name="emergency_contact",
    )
    contact_name = models.CharField(max_length=200)
    contact_number = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.volunteer.name} — emergency: {self.contact_name}"


class VolunteerMeta(models.Model):
    volunteer = models.OneToOneField(
        Volunteer, on_delete=models.CASCADE, related_name="meta",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.volunteer.name} — meta"