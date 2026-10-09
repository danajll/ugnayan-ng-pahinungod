from datetime import timedelta

from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Event, EventParticipation, ParticipationStatus, Volunteer


class ApiTestCase(APITestCase):
    def user(self, name="user", staff=False):
        return User.objects.create_user(
            username=name,
            email=f"{name}@example.com",
            password="StrongPass123!",
            is_staff=staff,
        )

    def volunteer(self, name="volunteer", staff=False):
        user = self.user(name, staff)
        return user, Volunteer.objects.create(
            user=user,
            volunteer_identifier=f"VOL-{user.pk:05d}",
            name=f"{name.title()} Volunteer",
            sex="M",
            birthdate="2000-01-15",
            affiliation_type="student",
        )

    def event_data(self, name="Community Cleanup"):
        start = timezone.now() + timedelta(days=1)
        return {
            "name": name,
            "description": "A volunteer activity.",
            "start_datetime": start.isoformat(),
            "end_datetime": (start + timedelta(hours=3)).isoformat(),
            "location": "UP Mindanao",
        }

    def registration_data(self, username="new-volunteer"):
        return {
            "username": username,
            "email": f"{username}@example.com",
            "password": "StrongPass123!",
            "name": "New Volunteer",
            "sex": "M",
            "birthdate": "2001-02-03",
            "affiliation_type": "student",
            "student_number": f"STU-{username}",
            "course": "Computer Science",
        }


class RegistrationAndLoginTests(ApiTestCase):
    def test_registration_success(self):
        response = self.client.post(
            reverse("register"), self.registration_data(), format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data["token"])
        self.assertTrue(
            Volunteer.objects.filter(user__username="new-volunteer").exists()
        )

    def test_registration_validation_error_does_not_create_user(self):
        data = self.registration_data()
        data.pop("course")
        response = self.client.post(reverse("register"), data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("course", response.data)
        self.assertFalse(User.objects.filter(username="new-volunteer").exists())

    def test_login_success(self):
        user = self.user()
        response = self.client.post(
            reverse("login"),
            {"username": user.username, "password": "StrongPass123!"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["user_id"], user.pk)
        self.assertTrue(response.data["token"])

    def test_login_rejects_invalid_credentials(self):
        user = self.user()
        response = self.client.post(
            reverse("login"),
            {"username": user.username, "password": "wrong"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class EventAndVolunteerPermissionTests(ApiTestCase):
    def test_event_reads_are_public_and_writes_require_staff(self):
        self.assertEqual(
            self.client.get(reverse("event-list-create")).status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(
            self.client.post(
                reverse("event-list-create"), self.event_data(), format="json"
            ).status_code,
            status.HTTP_401_UNAUTHORIZED,
        )
        self.client.force_authenticate(self.user())
        self.assertEqual(
            self.client.post(
                reverse("event-list-create"), self.event_data(), format="json"
            ).status_code,
            status.HTTP_403_FORBIDDEN,
        )

        self.client.force_authenticate(self.user("admin", staff=True))
        created = self.client.post(
            reverse("event-list-create"), self.event_data(), format="json"
        )
        self.assertEqual(created.status_code, status.HTTP_201_CREATED)
        url = reverse("event-detail", args=[created.data["id"]])
        self.assertEqual(
            self.client.patch(url, {"location": "New Location"}, format="json").status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(self.client.get(url).status_code, status.HTTP_200_OK)
        self.assertEqual(
            self.client.delete(url).status_code, status.HTTP_204_NO_CONTENT
        )

    def test_volunteer_list_detail_access_and_admin_only_update(self):
        _, volunteer = self.volunteer()
        list_response = self.client.get(reverse("volunteer-list"))
        self.assertEqual(list_response.status_code, status.HTTP_200_OK)
        self.assertEqual(list_response.data[0]["id"], volunteer.pk)
        detail_url = reverse("volunteer-detail", args=[volunteer.pk])
        self.assertEqual(self.client.get(detail_url).status_code, status.HTTP_200_OK)
        self.assertEqual(
            self.client.patch(detail_url, {"status": "inactive"}, format="json").status_code,
            status.HTTP_401_UNAUTHORIZED,
        )
        self.client.force_authenticate(self.user("regular"))
        self.assertEqual(
            self.client.patch(detail_url, {"status": "inactive"}, format="json").status_code,
            status.HTTP_403_FORBIDDEN,
        )
        self.client.force_authenticate(self.user("admin", staff=True))
        self.assertEqual(
            self.client.patch(detail_url, {"status": "inactive"}, format="json").status_code,
            status.HTTP_200_OK,
        )
        volunteer.refresh_from_db()
        self.assertEqual(volunteer.status, "inactive")

    def test_admin_can_create_volunteer(self):
        admin = self.user("admin", staff=True)
        new_user = self.user("new-volunteer")
        self.client.force_authenticate(admin)

        response = self.client.post(
            reverse("volunteer-list"),
            {
                "user": new_user.pk,
                "volunteer_identifier": "VOL-MANUAL-001",
                "name": "Manual Volunteer",
                "sex": "F",
                "birthdate": "2001-04-20",
                "affiliation_type": "student",
                "status": "active",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            Volunteer.objects.filter(
                user=new_user,
                volunteer_identifier="VOL-MANUAL-001",
            ).exists()
        )

    def test_put_requires_the_complete_volunteer_payload(self):
        admin = self.user("admin", staff=True)
        _, volunteer = self.volunteer()
        self.client.force_authenticate(admin)

        response = self.client.put(
            reverse("volunteer-detail", args=[volunteer.pk]),
            {"name": "Incomplete Replacement"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("user", response.data)
        self.assertIn("volunteer_identifier", response.data)

    def test_admin_can_replace_and_delete_volunteer(self):
        admin = self.user("admin", staff=True)
        user, volunteer = self.volunteer()
        self.client.force_authenticate(admin)
        detail_url = reverse("volunteer-detail", args=[volunteer.pk])

        put_response = self.client.put(
            detail_url,
            {
                "user": user.pk,
                "volunteer_identifier": volunteer.volunteer_identifier,
                "name": "Replacement Volunteer",
                "sex": "F",
                "birthdate": "2000-01-15",
                "affiliation_type": "student",
                "status": "suspended",
            },
            format="json",
        )
        self.assertEqual(put_response.status_code, status.HTTP_200_OK)
        volunteer.refresh_from_db()
        self.assertEqual(volunteer.name, "Replacement Volunteer")
        self.assertEqual(volunteer.status, "suspended")

        delete_response = self.client.delete(detail_url)
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Volunteer.objects.filter(pk=volunteer.pk).exists())


class EventParticipationTests(ApiTestCase):
    def setUp(self):
        self.user, self.volunteer_record = self.volunteer()
        self.event = Event.objects.create(
            name="Food Drive",
            description="Distribute food packs.",
            start_datetime=timezone.now() + timedelta(days=1),
            end_datetime=timezone.now() + timedelta(days=1, hours=2),
            location="Davao City",
        )

    def join(self):
        self.client.force_authenticate(self.user)
        return self.client.post(
            reverse("event-join", args=[self.event.pk]), {}, format="json"
        )

    def test_authenticated_volunteer_can_join_event(self):
        response = self.join()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            EventParticipation.objects.filter(
                volunteer=self.volunteer_record, event=self.event
            ).exists()
        )

    def test_duplicate_registration_is_rejected(self):
        self.join()
        response = self.join()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_join_requires_authentication(self):
        response = self.client.post(
            reverse("event-join", args=[self.event.pk]), {}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_participation_can_be_cancelled_and_deleted(self):
        self.join()
        participation = EventParticipation.objects.get(
            volunteer=self.volunteer_record, event=self.event
        )
        url = reverse("participation-detail", args=[participation.pk])
        response = self.client.patch(
            url, {"status": ParticipationStatus.CANCELLED}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        participation.refresh_from_db()
        self.assertEqual(participation.status, ParticipationStatus.CANCELLED)
        self.assertEqual(
            self.client.delete(url).status_code, status.HTTP_204_NO_CONTENT
        )
        self.assertFalse(EventParticipation.objects.filter(pk=participation.pk).exists())

    def test_participation_changes_require_authentication(self):
        participation = EventParticipation.objects.create(
            volunteer=self.volunteer_record, event=self.event
        )
        response = self.client.delete(
            reverse("participation-detail", args=[participation.pk])
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class ProfileTests(ApiTestCase):
    def setUp(self):
        self.user, self.volunteer_record = self.volunteer()
        self.url = reverse("volunteer-me-profile")

    def test_profile_get_requires_authentication(self):
        self.assertEqual(
            self.client.get(self.url).status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_authenticated_profile_get_and_patch(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["contact"], {})
        response = self.client.patch(
            self.url,
            {
                "contact": {"phone_number": "09171234567"},
                "address": {"street_address": "123 Main Street", "city": "Davao City"},
                "background": {"skills": "First aid"},
                "emergency": {
                    "contact_name": "Maria Volunteer",
                    "contact_number": "09987654321",
                },
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["contact"]["phone_number"], "09171234567")
        self.assertEqual(response.data["address"]["city"], "Davao City")
        self.assertEqual(response.data["background"]["skills"], "First aid")
        self.assertEqual(response.data["emergency"]["contact_name"], "Maria Volunteer")
