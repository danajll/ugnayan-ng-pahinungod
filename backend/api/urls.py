from django.urls import path
from . import views

urlpatterns = [
    # Health Check
    path("health/", views.health_check),

    # Events CRUD
    path("events/", views.event_list_create, name="event-list-create"),
    path("events/<int:pk>/", views.event_detail, name="event-detail"),

    # Volunteers CRUD
    path("volunteers/", views.volunteer_list_create, name="volunteer-list-create"),
    path("volunteers/<int:pk>/", views.volunteer_detail, name="volunteer-detail"),
]