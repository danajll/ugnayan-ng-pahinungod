from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.db import transaction
from rest_framework import serializers
from .models import (
    Badge,
    Event,
    EventParticipation,
    EmergencyContact,
    FacultyProfile,
    AlumniProfile,
    ParticipationStatus,
    StaffProfile,
    StudentProfile,
    Volunteer,
    VolunteerAddress,
    VolunteerBackground,
    VolunteerContact,
    VolunteerBadge,
    VolunteerMeta,
)

# Create your tests here.
class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = [
            "id",
            "name",
            "description",
            "start_datetime",
            "end_datetime",
            "location",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]


class VolunteerSerializer(serializers.ModelSerializer):
    service_hours = serializers.IntegerField(read_only=True)

    class Meta:
        model = Volunteer
        fields = [
            "id",
            "user",
            "volunteer_identifier",
            "name",
            "sex",
            "birthdate",
            "affiliation_type",
            "status",
            "service_hours",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "service_hours",
            "created_at",
            "updated_at",
        ]


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
    # Read-only display fields
    volunteer_name = serializers.CharField(source="volunteer.name", read_only=True)
    event_name = serializers.CharField(source="event.name", read_only=True)

    class Meta:
        model = EventParticipation
        fields = [
            "id",
            "volunteer",          # read-only (derived from request.user)
            "volunteer_name",     # convenience for frontend
            "event",
            "event_name",         # convenience for frontend
            "status",
            "hours_rendered",
            "registered_at",
        ]
        read_only_fields = ["id", "volunteer", "registered_at", "hours_rendered"]


class JoinEventSerializer(serializers.Serializer):
    """Used for POST /api/events/<id>/join/"""
    event_id = serializers.IntegerField()

class RegisterSerializer(serializers.Serializer):
    # ── User fields ──
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=8)

    # ── Volunteer core fields ──
    name = serializers.CharField(max_length=200)
    sex = serializers.ChoiceField(choices=["M", "F", "O"])
    birthdate = serializers.DateField()
    affiliation_type = serializers.ChoiceField(
        choices=["student", "faculty", "staff", "alumni"]
    )

    # ── Profile-specific fields (all optional here; validated below) ──
    student_number = serializers.CharField(required=False, allow_blank=True)
    course = serializers.CharField(required=False, allow_blank=True)

    employee_id = serializers.CharField(required=False, allow_blank=True)
    department = serializers.CharField(required=False, allow_blank=True)
    office = serializers.CharField(required=False, allow_blank=True)

    degree_obtained = serializers.CharField(required=False, allow_blank=True)
    year_graduated = serializers.IntegerField(required=False, allow_null=True)

    # year_retired = serializers.IntegerField(required=False, allow_null=True)
    # former_office = serializers.CharField(required=False, allow_blank=True)

    # ── Cross-field validation ──
    def validate(self, data):
        affiliation = data["affiliation_type"]
        errors = {}

        if not data.get("sex"):
            errors["sex"] = "This field is required."
        if not data.get("birthdate"):
            errors["birthdate"] = "This field is required."

        # Helper: require a field only for the given affiliation
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

        # elif affiliation == "retiree":
        #     require("year_retired")
        #     require("former_office")

        if errors:
            raise serializers.ValidationError(errors)
        return data

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

    @transaction.atomic
    def create(self, validated_data):
        affiliation = validated_data["affiliation_type"]

        # 1. User
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
        )

        # 2. Volunteer
        volunteer = Volunteer.objects.create(
            user=user,
            volunteer_identifier=f"VOL-{user.id:05d}",
            name=validated_data["name"],
            sex=validated_data["sex"],             
            birthdate=validated_data["birthdate"],  
            affiliation_type=affiliation,
        )

        # 3. Always create the meta row
        VolunteerMeta.objects.create(volunteer=volunteer)

        # 4. Create the correct profile row
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
        # elif affiliation == "retiree":
        #     RetireeProfile.objects.create(
        #         volunteer=volunteer,
        #         year_retired=validated_data["year_retired"],
        #         former_office=validated_data["former_office"],
        #     )

        return user

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
        fields = ["contact_name", "contact_number"]


class VolunteerProfileSerializer(serializers.Serializer):
    """
    Combined read/write serializer for the current volunteer's
    optional profile information.
    """
    contact = VolunteerContactSerializer(required=False)
    address = VolunteerAddressSerializer(required=False)
    background = VolunteerBackgroundSerializer(required=False)
    emergency = EmergencyContactSerializer(required=False)