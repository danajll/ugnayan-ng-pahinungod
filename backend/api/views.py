from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import Event, Volunteer
from .serializers import EventSerializer, VolunteerSerializer

# Create your views here.

# -- Health Check API --
@api_view(["GET"])
def health_check(request):
    return Response({"status": "ok", "service": "backend"})

# -- Events CRUD API --
@api_view(["GET", "POST"])
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


# -- Volunteers CRUD API --
@api_view(["GET", "POST"])
def volunteer_list_create(request):
    """
    GET  /api/volunteers/   -> list all volunteers
    POST /api/volunteers/   -> create a new volunteer
    """
    if request.method == "GET":
        volunteers = Volunteer.objects.all().order_by("-created_at")
        serializer = VolunteerSerializer(volunteers, many=True)
        return Response(serializer.data)

    serializer = VolunteerSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "PATCH", "DELETE"])
def volunteer_detail(request, pk):
    """
    GET    /api/volunteers/<id>/   -> retrieve one volunteer
    PUT    /api/volunteers/<id>/   -> full update
    PATCH  /api/volunteers/<id>/   -> partial update
    DELETE /api/volunteers/<id>/   -> delete
    """
    volunteer = get_object_or_404(Volunteer, pk=pk)

    if request.method == "GET":
        serializer = VolunteerSerializer(volunteer)
        return Response(serializer.data)

    if request.method in ["PUT", "PATCH"]:
        partial = request.method == "PATCH"
        serializer = VolunteerSerializer(
            volunteer,
            data=request.data,
            partial=partial,
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    volunteer.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)