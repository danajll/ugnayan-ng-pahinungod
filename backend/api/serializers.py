from rest_framework import serializers
from .models import Event

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