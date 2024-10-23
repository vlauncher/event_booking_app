from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
    DetailView,
)
from django.views import View
from django.contrib import messages
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.conf import settings

from .models import Event, EventBooking
from .forms import EventForm, CancelBookingForm


# Utility function for sending emails
def send_email_to_user(subject, message, recipient):
    send_mail(
        subject, message, settings.DEFAULT_FROM_EMAIL, [recipient], fail_silently=False
    )


class IsSuperUserMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser


class EventListView(ListView):
    model = Event
    template_name = "events/event_list.html"
    context_object_name = "events"
    ordering = ["-time"]


class EventDetailView(DetailView):
    model = Event
    template_name = "events/event_detail.html"
    context_object_name = "event"


class EventCreateView(LoginRequiredMixin, IsSuperUserMixin, CreateView):
    model = Event
    form_class = EventForm
    template_name = "events/event_form.html"
    success_url = reverse_lazy("event-list")

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, "Event created successfully.")
        return super().form_valid(form)


class EventUpdateView(LoginRequiredMixin, IsSuperUserMixin, UpdateView):
    model = Event
    form_class = EventForm
    template_name = "events/event_form.html"
    success_url = reverse_lazy("event-list")


class EventDeleteView(LoginRequiredMixin, IsSuperUserMixin, DeleteView):
    model = Event
    template_name = "events/event_confirm_delete.html"
    success_url = reverse_lazy("event-list")


class BookEventView(LoginRequiredMixin, View):
    def post(self, request, pk):
        event = get_object_or_404(Event, pk=pk)
        if EventBooking.objects.filter(event=event, user=request.user).exists():
            messages.warning(request, "You have already booked this event.")
        else:
            EventBooking.objects.create(event=event, user=request.user)
            messages.success(request, "Event booked successfully.")

            # Send booking confirmation email
            mail_subject = "Event Booking Confirmation"
            message = (
                f"Dear {request.user.first_name},\n\n"
                f"You have successfully booked the event: {event.name}.\n"
                f"Event details:\n"
                f"Time: {event.time}\n"
                f"Duration: {event.duration} minutes\n\n"
                f"Thank you for booking with us!"
            )
            send_mail(
                mail_subject,
                message,
                "noreply@eventsbooking.com",
                [request.user.email],
                fail_silently=False,
            )
        return redirect("event-detail", pk=pk)


class MyBookingsView(LoginRequiredMixin, ListView):
    model = EventBooking
    template_name = "events/my_bookings.html"
    context_object_name = "bookings"

    def get_queryset(self):
        return (
            EventBooking.objects.filter(user=self.request.user)
            .select_related("event")
            .order_by("-booked_at")
        )


class AllBookingsView(IsSuperUserMixin, ListView):
    model = EventBooking
    template_name = "events/all_bookings.html"
    context_object_name = "bookings"

    def get_queryset(self):
        return EventBooking.objects.select_related("user", "event").order_by(
            "-booked_at"
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        bookings = EventBooking.objects.all()
        total_bookings = bookings.count()
        cancelled_bookings = bookings.filter(is_cancelled=True).count()
        attending_count = total_bookings - cancelled_bookings
        context.update(
            {
                "total_bookings": total_bookings,
                "cancelled_bookings": cancelled_bookings,
                "attending_count": attending_count,
            }
        )
        return context


class CancelBookingView(LoginRequiredMixin, View):
    template_name = "events/cancel_booking.html"
    form_class = CancelBookingForm

    def get_object(self):
        return get_object_or_404(
            EventBooking, id=self.kwargs["booking_id"], user=self.request.user
        )

    def get(self, request, *args, **kwargs):
        booking = self.get_object()
        form = self.form_class()
        return render(request, self.template_name, {"form": form, "booking": booking})

    def post(self, request, *args, **kwargs):
        booking = self.get_object()
        booking.is_cancelled = True
        form = self.form_class(request.POST)
        if form.is_valid():
            booking.cancellation_reason = form.cleaned_data["cancellation_reason"]
            booking.save()
            send_email_to_user(
                subject="Booking Cancelled",
                message=f"Your booking for {booking.event.name} on {booking.event.time} has been cancelled.",
                recipient=booking.user.email,
            )
            messages.success(request, "Your booking has been cancelled successfully.")
            return redirect("my_bookings")
        return render(request, self.template_name, {"form": form, "booking": booking})
