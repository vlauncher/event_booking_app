from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from ..models import Event

User = get_user_model()


class EventViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            first_name="Test",
            last_name="User",
            email="test@example.com",
            password="password123",
        )
        self.superuser = User.objects.create_superuser(
            first_name="Admin",
            last_name="User",
            email="admin@example.com",
            password="adminpassword123",
        )
        self.event = Event.objects.create(
            name="Test Event",
            category="Music",
            notes="This is a test event",
            time="2024-10-23 12:00",
            duration=34,
            created_by=self.user,
        )

    def test_event_list_view(self):
        response = self.client.get(reverse("event-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "events/event_list.html")

    def test_event_create_view_superuser(self):
        self.client.login(email="admin@example.com", password="adminpassword123")
        response = self.client.get(reverse("event-create"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "events/event_form.html")

    def test_event_create_view_not_superuser(self):
        self.client.login(email="test@example.com", password="password123")
        response = self.client.get(reverse("event-create"))
        self.assertEqual(response.status_code, 403)  # Permission Denied

    def test_my_bookings_view(self):
        self.client.login(email="test@example.com", password="password123")
        response = self.client.get(reverse("my_bookings"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "events/my_bookings.html")

    def test_all_bookings_view_superuser(self):
        self.client.login(email="admin@example.com", password="adminpassword123")
        response = self.client.get(reverse("all_bookings"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "events/all_bookings.html")

    def test_all_bookings_view_not_superuser(self):
        self.client.login(email="test@example.com", password="password123")
        response = self.client.get(reverse("all_bookings"))
        self.assertEqual(response.status_code, 403)
