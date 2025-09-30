from django.db import models

from .utils import generate_tracking_number


class Shipment(models.Model):
    client = models.CharField(max_length=100, null=True, blank=True)
    tracking_number = models.CharField(max_length=50, unique=True)
    purchase_order = models.CharField(max_length=50, unique=True)
    waybill_number = models.CharField(max_length=50, unique=True)
    carrier = models.CharField(max_length=50, null=True, blank=True)
    origin = models.CharField(max_length=100, blank=True, null=True)
    destination = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(
        max_length=100, blank=True, null=True
    )  # e.g., "In Transit", "Delivered"
    last_location = models.CharField(max_length=100, blank=True, null=True)
    estimated_delivery = models.DateField(blank=True, null=True)
    last_updated = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.tracking_number} - {self.get_carrier_display()}"

    def save(self, *args, **kwargs):
        # Auto-generate tracking number if not provided
        if not self.tracking_number:
            tracking = f"CNEL{generate_tracking_number()}"
            while Shipment.objects.filter(tracking_number=tracking).exists():
                tracking = f"CNEL{generate_tracking_number()}"
            self.tracking_number = tracking.upper()
        else:
            self.tracking_number = self.tracking_number.upper()
        if self.purchase_order:
            self.purchase_order = self.purchase_order.upper()
        if self.waybill_number:
            self.waybill_number = self.waybill_number.upper()

        super().save(*args, **kwargs)


class TrackingEvent(models.Model):
    shipment = models.ForeignKey(
        Shipment, on_delete=models.CASCADE, related_name="events"
    )
    location = models.CharField(max_length=100)
    status_description = models.CharField(max_length=255)  # e.g., "Arrived at facility"
    timestamp = models.DateTimeField()

    class Meta:
        ordering = ["-timestamp"]

    def __str__(self):
        return f"{self.status_description} @ {self.location}"
