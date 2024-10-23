from django.test import SimpleTestCase
from django.urls import reverse, resolve
from ..views import (
    EventListView,
    MyBookingsView,
    AllBookingsView,
    EventCreateView,
    CancelBookingView,
)


class EventURLTest(SimpleTestCase):
    def test_event_list_url_is_resolved(self):
        url = reverse("event-list")
        self.assertEqual(resolve(url).func.view_class, EventListView)

    def test_my_bookings_url_is_resolved(self):
        url = reverse("my_bookings")
        self.assertEqual(resolve(url).func.view_class, MyBookingsView)

    def test_all_bookings_url_is_resolved(self):
        url = reverse("all_bookings")
        self.assertEqual(resolve(url).func.view_class, AllBookingsView)

    def test_event_create_url_is_resolved(self):
        url = reverse("event-create")
        self.assertEqual(resolve(url).func.view_class, EventCreateView)

    def test_booking_cancel_url_is_resolved(self):
        url = reverse("cancel_booking", args=[1])
        self.assertEqual(resolve(url).func.view_class, CancelBookingView)
