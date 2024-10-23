from django import forms
from .models import Event


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ["name", "category", "notes", "time", "duration"]


from django import forms


class CancelBookingForm(forms.Form):
    cancellation_reason = forms.CharField(
        label="Reason for Cancelling",
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Please provide a reason for cancelling your booking.",
            }
        ),
        required=True,
        max_length=255,
    )
