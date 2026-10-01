from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import Event
from .serializers import EventSerializer

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