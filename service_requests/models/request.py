from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.db import models

from service_requests.validators import validate_audio_size, validate_image_size
from setup.base_model import BaseModel


class RequestStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    ACCEPTED = "accepted", "Accepted"
    COMPLETED = "completed", "Completed"
    CANCELLED = "cancelled", "Cancelled"


class Request(BaseModel):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="requests"
    )
    description = models.TextField()
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    location_landmark = models.CharField(max_length=255, blank=True)
    photo = models.ImageField(
        upload_to="requests/photos/", null=True, blank=True, validators=[validate_image_size]
    )
    audio = models.FileField(
        upload_to="requests/audio/",
        null=True,
        blank=True,
        validators=[
            FileExtensionValidator(["mp3", "m4a", "wav", "ogg", "webm"]),
            validate_audio_size,
        ],
    )
    vehicle_make = models.CharField(max_length=100, blank=True)
    vehicle_model = models.CharField(max_length=100, blank=True)
    vehicle_year = models.PositiveSmallIntegerField(null=True, blank=True)
    status = models.CharField(
        max_length=20, choices=RequestStatus.choices, default=RequestStatus.PENDING
    )

    def __str__(self):
        return f"Request {self.id} ({self.status})"
