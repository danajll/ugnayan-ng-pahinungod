from django.urls import path
from . import views

urlpatterns = [
    # Health Check
    path("health/", views.health_check),

    # Auth
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),

    # Events CRUD
    path("events/", views.event_list_create, name="event-list-create"),
    path("events/<int:pk>/", views.event_detail, name="event-detail"),
    path("events/<int:pk>/join/", views.join_event, name="event-join"),

    # Volunteers CRUD
    path("volunteers/me/profile/", views.my_profile, name="volunteer-me-profile"),
    path("volunteers/", views.volunteer_list_create, name="volunteer-list-create"),
    path("volunteers/<int:pk>/", views.volunteer_detail, name="volunteer-detail"),

    # Participations
    path("me/participations/", views.my_participations, name="my-participations"),
    path("participations/<int:pk>/", views.participation_detail, name="participation-detail"),
]