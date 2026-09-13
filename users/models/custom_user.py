import uuid

from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

phone_number_validator = RegexValidator(
    regex=r"^\+?[0-9\s-]{9,15}$",
    message="Enter a valid phone number (e.g. 0241234567 or +233241234567).",
)


class Role(models.TextChoices):
    OWNER = "owner", "Owner"
    MECHANIC = "mechanic", "Mechanic"


class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role = models.CharField(max_length=20, choices=Role.choices)
    phone_number = models.CharField(
        max_length=20, blank=True, validators=[phone_number_validator]
    )
