import os
import uuid

from django.db import models
from django.db.models import UniqueConstraint
from django.utils.text import slugify
from rest_framework.exceptions import ValidationError

from bus_station import settings


class Facility(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name_plural = "facilities"

    def __str__(self):
        return self.name


def bus_image_file_path(instance, filename) -> str:
    _, extension = os.path.splitext(filename)

    filename = f"{slugify(instance.info)}-{uuid.uuid4()}{extension}"

    return os.path.join("uploads/buses/", filename)


class Bus(models.Model):
    info = models.CharField(max_length=255, null=True)
    num_seats = models.IntegerField()
    facilities = models.ManyToManyField(
        Facility, related_name="buses", blank=True
    )
    image = models.ImageField(null=True, upload_to=bus_image_file_path)

    class Meta:
        verbose_name_plural = "buses"

    @property
    def is_mini(self):
        return self.num_seats <= 10

    def __str__(self):
        return self.info


class Trip(models.Model):
    source = models.CharField(max_length=255)
    destination = models.CharField(max_length=255)
    departure = models.DateTimeField()
    bus = models.ForeignKey(
        "Bus", on_delete=models.CASCADE, related_name="trips"
    )

    def __str__(self):
        return f"{self.source} - {self.destination} ({self.departure})"


class Ticket(models.Model):
    seat = models.IntegerField()
    trip = models.ForeignKey(
        "Trip", on_delete=models.CASCADE, related_name="tickets"
    )
    order = models.ForeignKey(
        "Order", on_delete=models.CASCADE, related_name="tickets"
    )

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=["seat", "trip"], name="unique_ticket_seat_trip"
            )
        ]
        ordering = ["trip", "seat"]

    def __str__(self):
        return f"{self.trip} - (seat: {self.seat})"

    @staticmethod
    def validate_seat(seat: int, num_seats: int, error_to_raise):
        if not (1 <= seat <= num_seats):
            raise error_to_raise(
                {"seat": f"seat must be in range [1, {num_seats}], not {seat}"}
            )

    def clean(self):
        Ticket.validate_seat(
            seat=self.seat,
            num_seats=self.trip.bus.num_seats,
            error_to_raise=ValidationError,
        )

    def save(
        self,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None,
    ):
        self.full_clean()
        return super(Ticket, self).save(
            force_insert, force_update, using, update_fields
        )


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.created_at}"
