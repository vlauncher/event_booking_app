from django.urls import path
from . import views

urlpatterns = [
    path("events/", views.EventListView.as_view(), name="event-list"),
    path("event/<int:pk>/", views.EventDetailView.as_view(), name="event-detail"),
    path("event/new/", views.EventCreateView.as_view(), name="event-create"),
    path(
        "event/<int:pk>/update/", views.EventUpdateView.as_view(), name="event-update"
    ),
    path(
        "event/<int:pk>/delete/", views.EventDeleteView.as_view(), name="event-delete"
    ),
    path("event/<int:pk>/book/", views.BookEventView.as_view(), name="event-book"),
    path("my-bookings/", views.MyBookingsView.as_view(), name="my_bookings"),
    path("all-bookings/", views.AllBookingsView.as_view(), name="all_bookings"),
    path(
        "cancel-booking/<int:booking_id>/",
        views.CancelBookingView.as_view(),
        name="cancel_booking",
    ),
]
