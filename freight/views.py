import os

import requests
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.views import View
from dotenv import load_dotenv

from core.utils import send_email

from .forms import ShipmentForm, TrackingEventForm
from .models import Shipment, TrackingEvent

load_dotenv()


class TrackShipments(View):
    def get(self, request):
        tracking_number = request.GET.get("tracking_number")
        if not tracking_number:
            return redirect("home")
        print(f"Tracking: {tracking_number}")
        try:
            shipment_ob = Shipment.objects.get(
                tracking_number=tracking_number.strip().upper()
            )
        except Shipment.DoesNotExist:
            messages.error(
                request,
                f"Shipment with ID '{tracking_number.strip().upper()}' not found, confirm the tracking number and try again!",
            )
            return redirect("home")
        events = shipment_ob.events.all()

        context = {
            "shipment": shipment_ob,
            "events": events,
        }
        return render(request, "freight/track_results.html", context)


class CreateShipment(View):
    def get(self, request):
        if not request.user.is_authenticated:
            messages.error(request, "Only accessible to Admins.")
            return redirect("login")
        return render(request, "freight/shipment.html")

    def post(self, request):
        if not request.user.is_authenticated:
            messages.error(request, "Only accessible to Admins.")
            return redirect("login")
        forms = ShipmentForm(data=request.POST)
        if forms.is_valid():
            shipment = forms.save()
            email = forms.cleaned_data.get("email", "")
            name = forms.cleaned_data.get("client", "")
            if email:
                context = {
                    "client": name,
                    "url": "planetplusexpress.com",
                    "shipment": shipment,
                }
                template = render_to_string("freight/user_shipment.html", context)
                send_email(email, "Shipment Update", template)
            messages.success(request, "Shipment successfully added!")
            return redirect("shipment_details", pk=shipment.pk)
        messages.error(request, "Error! Confirm the details and try again.")
        return render(request, "freight/shipment.html")


def view_shipments(request):
    if not request.user.is_authenticated:
        messages.error(request, "Only accessible to Admins.")
        return redirect("login")
    shipments = Shipment.objects.all()
    return render(request, "freight/all_shipments.html", {"shipments": shipments})


def shipment_detail(request, pk):
    if not request.user.is_authenticated:
        messages.error(request, "Only accessible to Admins.")
        return redirect("login")
    shipment = get_object_or_404(Shipment, pk=pk)
    events = shipment.events.all()  # Because of related_name="events"

    if request.method == "POST":
        form = TrackingEventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.shipment = shipment
            event.save()

            # Update shipment fields based on event
            shipment.last_location = event.location
            shipment.status = event.status_description
            shipment.save()

            email = shipment.email

            if email:
                context = {
                    "client": shipment.client,
                    "url": "planetplusexpress.com",
                    "shipment": shipment,
                    "event": event,
                }
                template = render_to_string("freight/user_shipment_update.html", context)
                send_email(email, "Shipment Update", template)

            return redirect("shipment_details", pk=shipment.pk)
    else:
        form = TrackingEventForm()

    return render(
        request,
        "freight/shipment_detail.html",
        {
            "shipment": shipment,
            "events": events,
            "form": form,
        },
    )
