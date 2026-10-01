from rest_framework import serializers
from .models import Event, Volunteer

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