from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


class Event(models.Model):
    CATEGORY_CHOICES = [
        ("SEMINAR", "Seminar"),
        ("MEETING", "Meeting"),
        ("WORKSHOP", "Workshop"),
        ("CONFERENCE", "Conference"),
    ]

    name = models.CharField(max_length=255)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    notes = models.TextField(blank=True, null=True)
    time = models.DateTimeField()
    duration = models.PositiveIntegerField(help_text="Duration in minutes")
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="created_events"
    )

    def __str__(self):
        return self.name


class EventBooking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookings")
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="bookings")
    booked_at = models.DateTimeField(default=timezone.now)
    booking_details = models.CharField(max_length=255, blank=True)
    is_cancelled = models.BooleanField(default=False)
    cancellation_reason = models.CharField(max_length=255, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.booking_details:
            self.booking_details = f"An event '{self.event.name}' has been booked for {self.event.time.strftime('%B %d, %Y at %I:%M %p')}."
        super().save(*args, **kwargs)

    def __str__(self):
        return (
            f"{self.user.first_name} {self.user.last_name} has booked {self.event.name}"
        )
