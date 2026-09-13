from django.conf import settings
from django.db import models

from setup.base_model import BaseModel


class MechanicProfile(BaseModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="mechanic_profile"
    )
    business_name = models.CharField(max_length=255, blank=True)
    bio = models.TextField(blank=True)
    specialties = models.JSONField(default=list, blank=True)
    years_experience = models.PositiveIntegerField(null=True, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    location_landmark = models.CharField(max_length=255, blank=True)
    service_radius_km = models.PositiveIntegerField(default=10)
    is_available = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)

    class Meta:
        indexes = [models.Index(fields=["latitude", "longitude"])]

    def __str__(self):
        return self.business_name or self.user.username
