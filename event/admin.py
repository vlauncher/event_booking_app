from django.contrib import admin
from .models import Event, EventBooking


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ["name", "category", "time", "duration"]


@admin.register(EventBooking)
class EventBookingAdmin(admin.ModelAdmin):
    list_display = ["user", "event", "booked_at", "booking_details"]
