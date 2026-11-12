from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.db import transaction
from rest_framework import serializers
from django.db.models import Count, Q

from .models import (
    AlumniProfile,
    Badge,
    EmergencyContact,
    Event,
    EventParticipation,
    FacultyProfile,
    ParticipationStatus,
    Program,
    StaffProfile,
    StudentProfile,
    Subject,
    Volunteer,
    VolunteerAddress,
    VolunteerBackground,
    VolunteerBackgroundStatus,
    VolunteerContact,
    VolunteerBadge,
    VolunteerMeta,
)


# ─────────────────────────────────────────────────────────────
# LOOKUP TABLES
# ─────────────────────────────────────────────────────────────

class ProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = Program
        fields = ["id", "code", "name", "description"]


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ["id", "code", "name"]


# ─────────────────────────────────────────────────────────────
# CORE SERIALIZERS
# ─────────────────────────────────────────────────────────────

class EventSerializer(serializers.ModelSerializer):
    registered_count = serializers.SerializerMethodField()
    capacity_left = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = [
            "id", "name", "description", "start_datetime", "end_datetime",
            "location", "category", "status", "quota", "prerequisites",
            "cover_image", "created_at", "registered_count", "capacity_left",
        ]
        read_only_fields = ["id", "created_at", "registered_count", "capacity_left"]

    def get_registered_count(self, obj):
        return obj.participations.filter(
            status__in=["registered", "attended"]
        ).count()

    def get_capacity_left(self, obj):
        return max((obj.quota or 0) - self.get_registered_count(obj), 0)

class VolunteerSerializer(serializers.ModelSerializer):
    service_hours = serializers.IntegerField(read_only=True)
    full_name = serializers.CharField(read_only=True)
    age = serializers.IntegerField(read_only=True)

    # NEW: computed degree based on affiliation_type
    degree = serializers.SerializerMethodField()

    class Meta:
        model = Volunteer
        fields = [
            "id", "user", "volunteer_identifier", "first_name", "middle_name",
            "last_name", "nickname", "full_name", "sex", "birthdate", "age",
            "indigenous_affiliation", "mobile_number", "facebook_link",
            "hobbies", "affiliated_organizations", "permanent_address",
            "up_address", "senior_high_school", "affiliation_type", "status",
            "is_profile_complete", "onboarding_completed_at", "service_hours",
            "degree", "created_at", "updated_at",
        ]
        read_only_fields = [
            "id", "service_hours", "full_name", "age", "degree",
            "is_profile_complete", "onboarding_completed_at",
            "created_at", "updated_at",
        ]

    def get_degree(self, obj):
        try:
            if obj.affiliation_type == "student":
                return getattr(obj.student_profile, "course", "") or ""
            if obj.affiliation_type == "faculty":
                return getattr(obj.faculty_profile, "department", "") or ""
            if obj.affiliation_type == "staff":
                return getattr(obj.staff_profile, "office", "") or ""
            if obj.affiliation_type == "alumni":
                return getattr(obj.alumni_profile, "degree_obtained", "") or ""
        except Exception:
            # .student_profile etc. raises RelatedObjectDoesNotExist
            # if the profile row hasn't been created yet. Return blank.
            return ""
        return ""


class BadgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Badge
        fields = ["id", "name", "description", "icon_url", "criteria_type"]
        read_only_fields = ["id"]


class VolunteerBadgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = VolunteerBadge
        fields = ["id", "volunteer", "badge", "event", "date_awarded"]
        read_only_fields = ["id", "date_awarded"]


class VolunteerBadgeReadSerializer(serializers.ModelSerializer):
    badge = BadgeSerializer(read_only=True)

    class Meta:
        model = VolunteerBadge
        fields = ["id", "volunteer", "badge", "event", "date_awarded"]
        read_only_fields = fields


class EventParticipationSerializer(serializers.ModelSerializer):
    volunteer_name = serializers.CharField(source="volunteer.full_name", read_only=True)
    event_name = serializers.CharField(source="event.name", read_only=True)

    class Meta:
        model = EventParticipation
        fields = [
            "id",
            "volunteer",
            "volunteer_name",
            "event",
            "event_name",
            "status",
            "hours_rendered",
            "registered_at",
        ]
        read_only_fields = ["id", "volunteer", "registered_at", "hours_rendered"]


# ─────────────────────────────────────────────────────────────
# OPTIONAL PROFILE DETAIL TABLES
# ─────────────────────────────────────────────────────────────

class VolunteerContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = VolunteerContact
        fields = ["phone_number"]


class VolunteerAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = VolunteerAddress
        fields = ["street_address", "city"]


class VolunteerBackgroundSerializer(serializers.ModelSerializer):
    class Meta:
        model = VolunteerBackground
        fields = ["skills"]


class EmergencyContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmergencyContact
        fields = ["contact_name", "relationship", "contact_mobile_number", "complete_address"]


# ─────────────────────────────────────────────────────────────
# REGISTER (ADMIN FALLBACK / LEGACY)
# ─────────────────────────────────────────────────────────────

class RegisterSerializer(serializers.Serializer):
    # ── User fields ──
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=8)

    # ── Volunteer core fields ──
    first_name = serializers.CharField(max_length=100)
    middle_name = serializers.CharField(max_length=100, required=False, allow_blank=True)
    last_name = serializers.CharField(max_length=100)
    nickname = serializers.CharField(max_length=100, required=False, allow_blank=True)
    sex = serializers.ChoiceField(choices=["M", "F"])
    birthdate = serializers.DateField()

    indigenous_affiliation = serializers.CharField(required=False, allow_blank=True)
    mobile_number = serializers.CharField(max_length=30)
    facebook_link = serializers.URLField(required=False, allow_blank=True)
    hobbies = serializers.CharField(required=False, allow_blank=True)
    affiliated_organizations = serializers.CharField(required=False, allow_blank=True)
    permanent_address = serializers.CharField()
    up_address = serializers.CharField(required=False, allow_blank=True)
    senior_high_school = serializers.CharField(required=False, allow_blank=True)

    affiliation_type = serializers.ChoiceField(
        choices=["student", "faculty", "staff", "alumni"]
    )

    # ── Profile-specific fields ──
    student_number = serializers.CharField(required=False, allow_blank=True)
    course = serializers.CharField(required=False, allow_blank=True)
    employee_id = serializers.CharField(required=False, allow_blank=True)
    department = serializers.CharField(required=False, allow_blank=True)
    office = serializers.CharField(required=False, allow_blank=True)
    degree_obtained = serializers.CharField(required=False, allow_blank=True)
    year_graduated = serializers.IntegerField(required=False, allow_null=True)

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already taken.")
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already registered.")
        return value

    def validate_password(self, value):
        validate_password(value)
        return value

    def validate(self, data):
        affiliation = data["affiliation_type"]
        errors = {}

        def require(field):
            if not data.get(field):
                errors[field] = f"This field is required for {affiliation} volunteers."

        if affiliation == "student":
            require("student_number")
            require("course")
            if data.get("student_number") and StudentProfile.objects.filter(
                student_number=data["student_number"]
            ).exists():
                errors["student_number"] = "This student number is already registered."

        elif affiliation == "faculty":
            require("employee_id")
            require("department")
            if data.get("employee_id") and FacultyProfile.objects.filter(
                employee_id=data["employee_id"]
            ).exists():
                errors["employee_id"] = "This employee ID is already registered."

        elif affiliation == "staff":
            require("employee_id")
            require("office")
            if data.get("employee_id") and StaffProfile.objects.filter(
                employee_id=data["employee_id"]
            ).exists():
                errors["employee_id"] = "This employee ID is already registered."

        elif affiliation == "alumni":
            require("degree_obtained")
            require("year_graduated")

        if errors:
            raise serializers.ValidationError(errors)
        return data

    @transaction.atomic
    def create(self, validated_data):
        affiliation = validated_data["affiliation_type"]

        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
        )

        volunteer = Volunteer.objects.create(
            user=user,
            volunteer_identifier=f"VOL-{user.id:05d}",
            first_name=validated_data["first_name"],
            middle_name=validated_data.get("middle_name", ""),
            last_name=validated_data["last_name"],
            nickname=validated_data.get("nickname", ""),
            sex=validated_data["sex"],
            birthdate=validated_data["birthdate"],
            indigenous_affiliation=validated_data.get("indigenous_affiliation", ""),
            mobile_number=validated_data["mobile_number"],
            facebook_link=validated_data.get("facebook_link", ""),
            hobbies=validated_data.get("hobbies", ""),
            affiliated_organizations=validated_data.get("affiliated_organizations", ""),
            permanent_address=validated_data["permanent_address"],
            up_address=validated_data.get("up_address", ""),
            senior_high_school=validated_data.get("senior_high_school", ""),
            affiliation_type=affiliation,
            is_profile_complete=True,   # legacy register = complete
        )

        VolunteerMeta.objects.create(volunteer=volunteer)

        if affiliation == "student":
            StudentProfile.objects.create(
                volunteer=volunteer,
                student_number=validated_data["student_number"],
                course=validated_data["course"],
            )
        elif affiliation == "faculty":
            FacultyProfile.objects.create(
                volunteer=volunteer,
                employee_id=validated_data["employee_id"],
                department=validated_data["department"],
            )
        elif affiliation == "staff":
            StaffProfile.objects.create(
                volunteer=volunteer,
                employee_id=validated_data["employee_id"],
                office=validated_data["office"],
            )
        elif affiliation == "alumni":
            AlumniProfile.objects.create(
                volunteer=volunteer,
                degree_obtained=validated_data["degree_obtained"],
                year_graduated=validated_data["year_graduated"],
            )

        return user


# ─────────────────────────────────────────────────────────────
# ONBOARDING
# ─────────────────────────────────────────────────────────────

class OnboardingPersonalInfoSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=100)
    middle_name = serializers.CharField(max_length=100, required=False, allow_blank=True)
    last_name = serializers.CharField(max_length=100)
    nickname = serializers.CharField(max_length=100)
    sex = serializers.ChoiceField(choices=["M", "F"])
    birthdate = serializers.DateField()
    indigenous_affiliation = serializers.CharField(required=False, allow_blank=True)
    mobile_number = serializers.CharField(max_length=30)
    facebook_link = serializers.URLField()
    hobbies = serializers.CharField()
    affiliated_organizations = serializers.CharField()
    permanent_address = serializers.CharField()
    up_address = serializers.CharField()
    senior_high_school = serializers.CharField(max_length=300)

class OnboardingStudentInfoSerializer(serializers.Serializer):
    student_number = serializers.CharField(required=False, allow_blank=True)
    course = serializers.CharField(required=False, allow_blank=True)
    bachelor_degree = serializers.CharField(required=False, allow_blank=True)
    first_to_college = serializers.ChoiceField(choices=["yes", "no"])
    first_to_graduate = serializers.ChoiceField(choices=["yes", "no", "n_a"])
    first_in_up = serializers.ChoiceField(choices=["yes", "no"])
    # senior_high_school = serializers.CharField(max_length=300)

class OnboardingEmergencySerializer(serializers.Serializer):
    contact_name = serializers.CharField(max_length=200)
    relationship = serializers.CharField(max_length=100)
    contact_mobile_number = serializers.CharField(max_length=30)
    complete_address = serializers.CharField(required=False, allow_blank=True)


class OnboardingBackgroundSerializer(serializers.Serializer):
    application_status = serializers.ChoiceField(
        choices=["first_time", "previous_no_engagement", "previous_with_engagement"]
    )
    operations_group = serializers.ChoiceField(choices=["yes", "no"])
    other_orgs = serializers.ChoiceField(choices=["yes", "no"])
    other_orgs_name = serializers.CharField(required=False, allow_blank=True)
    referral_source = serializers.CharField(required=False, allow_blank=True)


class OnboardingSerializer(serializers.Serializer):
    personal_info = OnboardingPersonalInfoSerializer()
    affiliation_type = serializers.ChoiceField(
        choices=["student", "faculty", "staff", "alumni"]
    )
    student_info = OnboardingStudentInfoSerializer()
    emergency_contact = OnboardingEmergencySerializer()
    programs = serializers.ListField(
        child=serializers.CharField(), allow_empty=False
    )
    affirmative_action_subjects = serializers.ListField(
        child=serializers.CharField(), required=False, allow_empty=True
    )
    background = OnboardingBackgroundSerializer()

    def validate_programs(self, value):
        codes = set(value)
        existing = set(Program.objects.filter(code__in=codes).values_list("code", flat=True))
        missing = codes - existing
        if missing:
            raise serializers.ValidationError(f"Unknown program codes: {sorted(missing)}")
        return value

    def validate_affirmative_action_subjects(self, value):
        codes = set(value)
        existing = set(Subject.objects.filter(code__in=codes).values_list("code", flat=True))
        missing = codes - existing
        if missing:
            raise serializers.ValidationError(f"Unknown subject codes: {sorted(missing)}")
        return value

    def validate(self, data):
        programs = data.get("programs", [])
        subjects = data.get("affirmative_action_subjects", [])
        if subjects and "AFFIRMATIVE_ACTION_PROGRAM" not in programs:
            raise serializers.ValidationError({
                "affirmative_action_subjects":
                    "Only valid when AFFIRMATIVE_ACTION_PROGRAM is selected."
            })
        return data