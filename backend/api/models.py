from datetime import date
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum


# ─────────────────────────────────────────────────────────────
# CHOICES
# ─────────────────────────────────────────────────────────────

class AffiliationType(models.TextChoices):
    STUDENT = "student", "Student"
    FACULTY = "faculty", "Faculty Member"
    STAFF = "staff", "UP Representative / Admin Staff"
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


class Sex(models.TextChoices):                                 
    MALE = "M", "Male"
    FEMALE = "F", "Female"


class ApplicationStatus(models.TextChoices):                   
    FIRST_TIME = "first_time", "First time to apply as volunteer with no engagements"
    PREVIOUS_NO_ENGAGEMENT = "previous_no_engagement", "Already signed up in previous form but no engagements yet"
    PREVIOUS_WITH_ENGAGEMENT = "previous_with_engagement", "Already signed up in previous form and has engagements"


class YesNo(models.TextChoices):                                
    YES = "yes", "Yes"
    NO = "no", "No"


class YesNoNA(models.TextChoices):                              
    YES = "yes", "Yes"
    NO = "no", "No"
    NA = "n_a", "N/A"


# ─────────────────────────────────────────────────────────────
# PROGRAM / SUBJECT LOOKUP TABLES
# ─────────────────────────────────────────────────────────────

class Program(models.Model):                                 
    name = models.CharField(max_length=200, unique=True)
    code = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Subject(models.Model):                                 
    name = models.CharField(max_length=200, unique=True)
    code = models.SlugField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


# ─────────────────────────────────────────────────────────────
# CORE MODELS
# ─────────────────────────────────────────────────────────────

class Volunteer(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="volunteer",
    )
    volunteer_identifier = models.CharField(max_length=50, unique=True)

    # ── Personal information ──
    first_name = models.CharField(max_length=100)                
    middle_name = models.CharField(max_length=100, blank=True)   
    last_name = models.CharField(max_length=100)                 
    nickname = models.CharField(max_length=100, blank=True)       

    sex = models.CharField(                                       
        max_length=1, choices=Sex.choices,
    )
    birthdate = models.DateField()                                

    indigenous_affiliation = models.CharField(                  
        max_length=200, blank=True,
    )
    mobile_number = models.CharField(max_length=30)             
    facebook_link = models.URLField(blank=True)                  
    hobbies = models.TextField(blank=True)                      
    affiliated_organizations = models.TextField(blank=True)      
    permanent_address = models.TextField()                       
    up_address = models.TextField(blank=True)                    

    # ── Affiliation ──
    affiliation_type = models.CharField(
        max_length=20, choices=AffiliationType.choices,
    )
    status = models.CharField(
        max_length=20,
        choices=VolunteerStatus.choices,
        default=VolunteerStatus.ACTIVE,
    )

    # ── Programs & subjects (M2M) ──
    programs = models.ManyToManyField(                          
        Program, blank=True, related_name="volunteers",
    )
    affirmative_action_subjects = models.ManyToManyField(      
        Subject, blank=True, related_name="volunteers",
    )

    # ── Onboarding completion ──
    is_profile_complete = models.BooleanField(default=False)    
    onboarding_completed_at = models.DateTimeField(             
        null=True, blank=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.last_name}, {self.first_name} ({self.volunteer_identifier})"

    @property
    def full_name(self):
        parts = [self.first_name, self.middle_name, self.last_name]
        return " ".join(p for p in parts if p)

    @property
    def age(self):                                          
        if not self.birthdate:
            return None
        today = date.today()
        return today.year - self.birthdate.year - (
            (today.month, today.day) < (self.birthdate.month, self.birthdate.day)
        )

    @property
    def service_hours(self):
        result = self.event_participations.filter(
            status=ParticipationStatus.ATTENDED,
        ).aggregate(total=Sum("hours_rendered"))["total"]
        return result or 0


class VolunteerBackgroundStatus(models.Model):              
    volunteer = models.OneToOneField(
        Volunteer, on_delete=models.CASCADE, related_name="background_status",
    )
    application_status = models.CharField(
        max_length=30, choices=ApplicationStatus.choices,
    )
    wants_operations_group = models.CharField(
        max_length=3, choices=YesNo.choices,
    )
    is_part_of_other_org = models.CharField(
        max_length=3, choices=YesNo.choices,
    )
    other_org_name = models.CharField(max_length=200, blank=True)
    referral_source = models.CharField(max_length=300, blank=True)

    def __str__(self):
        return f"{self.volunteer.full_name} — background"


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
        Volunteer, on_delete=models.CASCADE, related_name="event_participations",
    )
    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, related_name="participations",
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
        return f"{self.volunteer.full_name} @ {self.event.name} — {self.status}"


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
        Volunteer, on_delete=models.CASCADE, related_name="badges",
    )
    badge = models.ForeignKey(
        Badge, on_delete=models.CASCADE, related_name="awarded_to",
    )
    event = models.ForeignKey(
        Event, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="badges_awarded",
    )
    date_awarded = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("volunteer", "badge")

    def __str__(self):
        return f"{self.volunteer.full_name} — {self.badge.name}"


# ─────────────────────────────────────────────────────────────
# PROFILE TABLES
# ─────────────────────────────────────────────────────────────

class StudentProfile(models.Model):
    volunteer = models.OneToOneField(
        Volunteer, on_delete=models.CASCADE, related_name="student_profile",
    )

    student_number = models.CharField(max_length=50, unique=True, blank=True, null=True)
    course = models.CharField(max_length=100, blank=True)

    senior_high_school = models.CharField(max_length=300, blank=True)
    bachelor_degree = models.CharField(max_length=300, blank=True)
    first_to_college = models.CharField(
        max_length=3, choices=YesNo.choices, blank=True,
    )
    first_to_graduate = models.CharField(
        max_length=3, choices=YesNoNA.choices, blank=True,
    )
    first_in_up = models.CharField(
        max_length=3, choices=YesNo.choices, blank=True,
    )

    def __str__(self):
        return f"{self.volunteer.full_name} — student"


class FacultyProfile(models.Model):
    volunteer = models.OneToOneField(
        Volunteer, on_delete=models.CASCADE, related_name="faculty_profile",
    )
    employee_id = models.CharField(max_length=50, unique=True, blank=True, null=True)
    department = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.volunteer.full_name} — faculty"


class StaffProfile(models.Model):
    volunteer = models.OneToOneField(
        Volunteer, on_delete=models.CASCADE, related_name="staff_profile",
    )
    employee_id = models.CharField(max_length=50, unique=True, blank=True, null=True)
    office = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.volunteer.full_name} — staff"


class AlumniProfile(models.Model):
    volunteer = models.OneToOneField(
        Volunteer, on_delete=models.CASCADE, related_name="alumni_profile",
    )
    degree_obtained = models.CharField(max_length=200, blank=True)
    year_graduated = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.volunteer.full_name} — alumni"


# ─────────────────────────────────────────────────────────────
# VOLUNTEER DETAIL TABLES
# ─────────────────────────────────────────────────────────────

class VolunteerContact(models.Model):
    volunteer = models.OneToOneField(
        Volunteer, on_delete=models.CASCADE, related_name="contact",
    )
    phone_number = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return f"{self.volunteer.full_name} — {self.phone_number}"


class VolunteerAddress(models.Model):
    volunteer = models.OneToOneField(
        Volunteer, on_delete=models.CASCADE, related_name="address",
    )
    street_address = models.CharField(max_length=300, blank=True)
    city = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.volunteer.full_name} — {self.city}"


class VolunteerBackground(models.Model):
    volunteer = models.OneToOneField(
        Volunteer, on_delete=models.CASCADE, related_name="background",
    )
    skills = models.TextField(blank=True)

    def __str__(self):
        return f"{self.volunteer.full_name} — background"


class EmergencyContact(models.Model):
    volunteer = models.OneToOneField(
        Volunteer, on_delete=models.CASCADE, related_name="emergency_contact",
    )
    contact_name = models.CharField(max_length=200)
    relationship = models.CharField(max_length=100)          
    contact_mobile_number = models.CharField(max_length=30)     
    complete_address = models.TextField(blank=True)            

    def __str__(self):
        return f"{self.volunteer.full_name} — emergency: {self.contact_name}"


class VolunteerMeta(models.Model):
    volunteer = models.OneToOneField(
        Volunteer, on_delete=models.CASCADE, related_name="meta",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.volunteer.full_name} — meta"