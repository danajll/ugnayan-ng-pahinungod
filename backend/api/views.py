from datetime import datetime
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import (Event, Volunteer, EventParticipation, ParticipationStatus, VolunteerContact, VolunteerAddress, VolunteerBackground, EmergencyContact,
    VolunteerMeta, StudentProfile, FacultyProfile, StaffProfile, AlumniProfile, Program, Subject, VolunteerBackgroundStatus,
)
from .serializers import (EventSerializer, VolunteerSerializer, EventParticipationSerializer, RegisterSerializer, VolunteerContactSerializer, VolunteerAddressSerializer,
    VolunteerBackgroundSerializer, EmergencyContactSerializer, ProgramSerializer, SubjectSerializer, OnboardingSerializer,
)
from .permissions import IsAdminOrReadOnly


# ─────────────────────────────────────────────────────────────
# HEALTH CHECK
# ─────────────────────────────────────────────────────────────

@api_view(["GET"])
def health_check(request):
    return Response({"status": "ok", "service": "backend"})


# ─────────────────────────────────────────────────────────────
# EVENTS CRUD
# ─────────────────────────────────────────────────────────────

@api_view(["GET", "POST"])
@permission_classes([IsAdminOrReadOnly])
def event_list_create(request):
    if request.method == "GET":
        events = Event.objects.all().order_by("-start_datetime")
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)

    serializer = EventSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "PATCH", "DELETE"])
@permission_classes([IsAdminOrReadOnly])
def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)

    if request.method == "GET":
        return Response(EventSerializer(event).data)

    if request.method in ["PUT", "PATCH"]:
        partial = request.method == "PATCH"
        serializer = EventSerializer(event, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    event.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


# ─────────────────────────────────────────────────────────────
# VOLUNTEERS
# ─────────────────────────────────────────────────────────────

@api_view(["GET"])
@permission_classes([IsAdminOrReadOnly])
def volunteer_list(request):
    volunteers = Volunteer.objects.all().order_by("-created_at")
    serializer = VolunteerSerializer(volunteers, many=True)
    return Response(serializer.data)


@api_view(["GET", "PATCH"])
@permission_classes([IsAdminOrReadOnly])
def volunteer_detail(request, pk):
    volunteer = get_object_or_404(Volunteer, pk=pk)

    if request.method == "GET":
        return Response(VolunteerSerializer(volunteer).data)

    serializer = VolunteerSerializer(volunteer, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ─────────────────────────────────────────────────────────────
# EVENT PARTICIPATION
# ─────────────────────────────────────────────────────────────

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def join_event(request, pk):
    event = get_object_or_404(Event, pk=pk)

    volunteer = getattr(request.user, "volunteer", None)
    if volunteer is None:
        return Response(
            {"detail": "You do not have a volunteer profile."},
            status=status.HTTP_403_FORBIDDEN,
        )

    if EventParticipation.objects.filter(volunteer=volunteer, event=event).exists():
        return Response(
            {"detail": "You are already registered for this event."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    participation = EventParticipation.objects.create(
        volunteer=volunteer,
        event=event,
        status=ParticipationStatus.REGISTERED,
    )
    return Response(
        EventParticipationSerializer(participation).data,
        status=status.HTTP_201_CREATED,
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def my_participations(request):
    volunteer = getattr(request.user, "volunteer", None)
    if volunteer is None:
        return Response(
            {"detail": "You do not have a volunteer profile."},
            status=status.HTTP_403_FORBIDDEN,
        )

    participations = (
        volunteer.event_participations
        .select_related("event")
        .order_by("-registered_at")
    )
    return Response(EventParticipationSerializer(participations, many=True).data)


@api_view(["PATCH", "DELETE"])
@permission_classes([IsAuthenticated])
def participation_detail(request, pk):
    volunteer = getattr(request.user, "volunteer", None)
    if volunteer is None:
        return Response(
            {"detail": "You do not have a volunteer profile."},
            status=status.HTTP_403_FORBIDDEN,
        )

    participation = get_object_or_404(
        EventParticipation, pk=pk, volunteer=volunteer,
    )

    if request.method == "DELETE":
        participation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    new_status = request.data.get("status")
    if new_status != ParticipationStatus.CANCELLED:
        return Response(
            {"detail": "You can only set status to 'cancelled'."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    participation.status = ParticipationStatus.CANCELLED
    participation.save()
    return Response(EventParticipationSerializer(participation).data)


# ─────────────────────────────────────────────────────────────
# AUTH
# ─────────────────────────────────────────────────────────────

@api_view(["POST"])
def register_view(request):
    """Legacy admin-fallback registration (username + password)."""
    serializer = RegisterSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    user = serializer.save()
    token, _ = Token.objects.get_or_create(user=user)

    return Response(
        {
            "token": token.key,
            "user_id": user.id,
            "username": user.username,
            "volunteer_id": user.volunteer.id,
        },
        status=status.HTTP_201_CREATED,
    )


@api_view(["POST"])
def login_view(request):
    username = request.data.get("username")
    password = request.data.get("password")

    if not username or not password:
        return Response(
            {"detail": "username and password are required."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    user = authenticate(username=username, password=password)
    if user is None:
        return Response(
            {"detail": "Invalid credentials."},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    token, _ = Token.objects.get_or_create(user=user)
    return Response({
        "token": token.key,
        "user_id": user.id,
        "username": user.username,
        "is_staff": user.is_staff,
        "is_superuser": user.is_superuser,
    })


# ─────────────────────────────────────────────────────────────
# OPTIONAL PROFILE INFORMATION
# ─────────────────────────────────────────────────────────────

def _serialize_profile(volunteer):
    def get_or_empty(model, serializer_cls):
        obj = model.objects.filter(volunteer=volunteer).first()
        return serializer_cls(obj).data if obj else {}
    return {
        "contact":    get_or_empty(VolunteerContact, VolunteerContactSerializer),
        "address":    get_or_empty(VolunteerAddress, VolunteerAddressSerializer),
        "background": get_or_empty(VolunteerBackground, VolunteerBackgroundSerializer),
        "emergency":  get_or_empty(EmergencyContact, EmergencyContactSerializer),
    }


@api_view(["GET", "PATCH"])
@permission_classes([IsAuthenticated])
@transaction.atomic
def my_profile(request):
    volunteer = getattr(request.user, "volunteer", None)
    if volunteer is None:
        return Response(
            {"detail": "You do not have a volunteer profile."},
            status=status.HTTP_403_FORBIDDEN,
        )

    if request.method == "GET":
        return Response(_serialize_profile(volunteer))

    sections = {
        "contact":    (VolunteerContact,    VolunteerContactSerializer),
        "address":    (VolunteerAddress,    VolunteerAddressSerializer),
        "background": (VolunteerBackground, VolunteerBackgroundSerializer),
        "emergency":  (EmergencyContact,    EmergencyContactSerializer),
    }

    errors = {}
    validated = []

    for key, (model, serializer_cls) in sections.items():
        if key not in request.data:
            continue
        obj = model.objects.filter(volunteer=volunteer).first()
        serializer = serializer_cls(obj, data=request.data[key], partial=True)
        if serializer.is_valid():
            validated.append((obj, serializer))
        else:
            errors[key] = serializer.errors

    if errors:
        return Response(errors, status=status.HTTP_400_BAD_REQUEST)

    for obj, serializer in validated:
        if obj is None:
            serializer.save(volunteer=volunteer)
        else:
            serializer.save()

    return Response(_serialize_profile(volunteer))


# ─────────────────────────────────────────────────────────────
# LOOKUP LISTS
# ─────────────────────────────────────────────────────────────

@api_view(["GET"])
def program_list(request):
    programs = Program.objects.filter(is_active=True).order_by("name")
    return Response(ProgramSerializer(programs, many=True).data)


@api_view(["GET"])
def subject_list(request):
    subjects = Subject.objects.filter(is_active=True).order_by("name")
    return Response(SubjectSerializer(subjects, many=True).data)


# ─────────────────────────────────────────────────────────────
# ONBOARDING
# ─────────────────────────────────────────────────────────────

@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
@transaction.atomic
def complete_onboarding(request):
    """
    PATCH /api/volunteers/me/onboarding/
    Saves the full onboarding form for the current volunteer.
    """
    volunteer = getattr(request.user, "volunteer", None)
    if volunteer is None:
        return Response(
            {"detail": "You do not have a volunteer profile."},
            status=status.HTTP_403_FORBIDDEN,
        )

    serializer = OnboardingSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    data = serializer.validated_data

    # Personal info
    pi = data["personal_info"]
    for field in [
        "first_name", "middle_name", "last_name", "nickname",
        "sex", "birthdate", "indigenous_affiliation",
        "mobile_number", "facebook_link", "hobbies",
        "affiliated_organizations", "permanent_address", "up_address", "senior_high_school",
    ]:
        setattr(volunteer, field, pi.get(field, ""))
    volunteer.affiliation_type = data["affiliation_type"]
    volunteer.is_profile_complete = True
    volunteer.onboarding_completed_at = timezone.now()
    volunteer.save()

    # Programs
    programs = Program.objects.filter(code__in=data["programs"])
    volunteer.programs.set(programs)

    # Affirmative action subjects
    subjects = Subject.objects.filter(code__in=data.get("affirmative_action_subjects", []))
    volunteer.affirmative_action_subjects.set(subjects)

    # Student info
    if "student_info" in data:
        si = data["student_info"]
        StudentProfile.objects.update_or_create(
            volunteer=volunteer,
            defaults={
                # "senior_high_school": si.get("senior_high_school", ""),
                "bachelor_degree": si.get("bachelor_degree", ""),
                "first_to_college": si.get("first_to_college", ""),
                "first_to_graduate": si.get("first_to_graduate", ""),
                "first_in_up": si.get("first_in_up", ""),
            },
        )

    # Emergency contact
    ec = data["emergency_contact"]
    EmergencyContact.objects.update_or_create(
        volunteer=volunteer,
        defaults={
            "contact_name": ec["contact_name"],
            "relationship": ec["relationship"],
            "contact_mobile_number": ec["contact_mobile_number"],
            "complete_address": ec.get("complete_address", ""),
        },
    )

    # Background status
    bg = data["background"]
    VolunteerBackgroundStatus.objects.update_or_create(
        volunteer=volunteer,
        defaults={
            "application_status": bg["application_status"],
            "wants_operations_group": bg["operations_group"],
            "is_part_of_other_org": bg["other_orgs"],
            "other_org_name": bg.get("other_orgs_name", ""),
            "referral_source": bg.get("referral_source", ""),
        },
    )

    return Response({
        "detail": "Onboarding complete.",
        "volunteer_id": volunteer.id,
        "is_profile_complete": True,
    })