from django.test import TestCase
from django.contrib.auth import get_user_model
from ..models import Event, EventBooking
from datetime import datetime, timedelta

User = get_user_model()


class EventModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            first_name="Test",
            last_name="User",
            email="test@example.com",
            password="password123",
        )
        self.event = Event.objects.create(
            name="Test Event",
            category="Music",
            notes="This is a test event",
            time=datetime.now(),
            duration=45,
            created_by=self.user,
        )

    def test_event_creation(self):
        self.assertEqual(str(self.event), "Test Event")
        self.assertEqual(self.event.category, "Music")

    def test_event_booking_creation(self):
        booking = EventBooking.objects.create(
            user=self.user,
            event=self.event,
            booking_details="An event has been booked",
        )
        self.assertEqual(
            str(booking),
            f"{self.user.first_name} {self.user.last_name} has booked {self.event.name}",
        )
        self.assertEqual(booking.event, self.event)
        self.assertEqual(booking.user, self.user)
