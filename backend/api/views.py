from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate
from django.db import transaction
from rest_framework.authtoken.models import Token

from .models import Event, Volunteer, EventParticipation, ParticipationStatus, VolunteerContact, VolunteerAddress, VolunteerBackground, EmergencyContact
from .serializers import EventSerializer, VolunteerSerializer, EventParticipationSerializer, RegisterSerializer, VolunteerProfileSerializer, VolunteerContactSerializer, VolunteerAddressSerializer, VolunteerBackgroundSerializer, EmergencyContactSerializer
from .permissions import IsAdminOrReadOnly

# Create your views here.

# -- Health Check API --
@api_view(["GET"])
def health_check(request):
    return Response({"status": "ok", "service": "backend"})

# -- Events CRUD API --
@api_view(["GET", "POST"])
@permission_classes([IsAdminOrReadOnly])
def event_list_create(request):
    """
    GET  /api/events/   → list all events
    POST /api/events/   → create a new event
    """
    if request.method == "GET":
        events = Event.objects.all().order_by("-start_datetime")
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "PATCH", "DELETE"])
@permission_classes([IsAdminOrReadOnly])
def event_detail(request, pk):
    """
    GET    /api/events/<id>/  → retrieve one event
    PUT    /api/events/<id>/  → full update
    PATCH  /api/events/<id>/  → partial update
    DELETE /api/events/<id>/  → delete
    """
    event = get_object_or_404(Event, pk=pk)

    if request.method == "GET":
        serializer = EventSerializer(event)
        return Response(serializer.data)

    elif request.method in ["PUT", "PATCH"]:
        # partial=True allows PATCH; PUT requires all fields
        partial = request.method == "PATCH"
        serializer = EventSerializer(event, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# -- Volunteers API --
@api_view(["GET"])
@permission_classes([IsAdminOrReadOnly])
def volunteer_list(request):
    """
    GET /api/volunteers/  → list all volunteers
    """
    volunteers = Volunteer.objects.all().order_by("-created_at")
    serializer = VolunteerSerializer(volunteers, many=True)
    return Response(serializer.data)


@api_view(["GET", "PATCH"])
@permission_classes([IsAdminOrReadOnly])
def volunteer_detail(request, pk):
    """
    GET    /api/volunteers/<id>/  → retrieve one volunteer
    PATCH  /api/volunteers/<id>/  → partial update (admin only)
    """
    volunteer = get_object_or_404(Volunteer, pk=pk)

    if request.method == "GET":
        serializer = VolunteerSerializer(volunteer)
        return Response(serializer.data)

    # PATCH — admin only (IsAdminOrReadOnly handles this)
    serializer = VolunteerSerializer(volunteer, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# -- EVENT PARTICIPATION -- 
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def join_event(request, pk):
    """
    POST /api/events/<pk>/join/
    Authenticated volunteer registers for an event.
    """
    event = get_object_or_404(Event, pk=pk)

    # Every authenticated user must have a Volunteer profile
    volunteer = getattr(request.user, "volunteer", None)
    if volunteer is None:
        return Response(
            {"detail": "You do not have a volunteer profile."},
            status=status.HTTP_403_FORBIDDEN,
        )

    # Prevent duplicate registration
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
    """
    GET /api/me/participations/
    Returns the current volunteer's event registrations.
    """
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
    serializer = EventParticipationSerializer(participations, many=True)
    return Response(serializer.data)


@api_view(["PATCH", "DELETE"])
@permission_classes([IsAuthenticated])
def participation_detail(request, pk):
    """
    PATCH  /api/participations/<pk>/  → cancel registration (set status=cancelled)
    DELETE /api/participations/<pk>/  → remove registration entirely
    """
    volunteer = getattr(request.user, "volunteer", None)
    if volunteer is None:
        return Response(
            {"detail": "You do not have a volunteer profile."},
            status=status.HTTP_403_FORBIDDEN,
        )

    participation = get_object_or_404(
        EventParticipation, pk=pk, volunteer=volunteer,  # ← ownership check
    )

    if request.method == "DELETE":
        participation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    # PATCH — only allow setting status to cancelled
    new_status = request.data.get("status")
    if new_status != ParticipationStatus.CANCELLED:
        return Response(
            {"detail": "You can only set status to 'cancelled'."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    participation.status = ParticipationStatus.CANCELLED
    participation.save()
    return Response(EventParticipationSerializer(participation).data)

# -- REGISTER API -- 
@api_view(["POST"])
def register_view(request):
    """
    POST /api/register/
    Body: {
        "username": "...", "email": "...", "password": "...",
        "name": "...", "affiliation_type": "student",
        "student_number": "...", "course": "..."
    }
    Returns: { token, user_id, username, volunteer_id }
    """
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

# -- LOGIN API -- 
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

# -- ADDITIONAL PROFILE INFORMATION API --
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

    # PATCH
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