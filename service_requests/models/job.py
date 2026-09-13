from django.conf import settings
from django.db import models

from setup.base_model import BaseModel


class JobStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    ACCEPTED = "accepted", "Accepted"
    DECLINED = "declined", "Declined"
    COMPLETED = "completed", "Completed"
    CANCELLED = "cancelled", "Cancelled"


class Job(BaseModel):
    request = models.ForeignKey(
        "service_requests.Request", on_delete=models.CASCADE, related_name="jobs"
    )
    mechanic = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="jobs"
    )
    status = models.CharField(max_length=20, choices=JobStatus.choices, default=JobStatus.PENDING)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    responded_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["request", "mechanic"], name="unique_job_per_request_mechanic"
            )
        ]

    def __str__(self):
        return f"Job {self.id} ({self.status})"
