from django.urls import path
from . import views

urlpatterns = [
    # Health Check
    path("health/", views.health_check),

    # Events CRUD
    path("events/", views.event_list_create, name="event-list-create"),
    path("events/<int:pk>/", views.event_detail, name="event-detail"),
]