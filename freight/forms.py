from django import forms
from django.utils import timezone

from .models import Shipment, TrackingEvent


class ShipmentForm(forms.ModelForm):
    class Meta:
        model = Shipment
        fields = [
            "client",
            "carrier",
            "origin",
            "destination",
            "status",
            "last_location",
            "estimated_delivery",
        ]


class TrackingEventForm(forms.ModelForm):
    class Meta:
        model = TrackingEvent
        fields = ["location", "status_description", "timestamp"]

    def clean(self):
        cleaned_data = super().clean()
        # If timestamp is empty, set it to now
        if not cleaned_data.get("timestamp"):
            cleaned_data["timestamp"] = timezone.now()
        return cleaned_data
