from math import cos, radians

from django.db.models import F, FloatField, Value
from django.db.models.functions import ACos, Cast, Cos, Greatest, Least, Radians, Sin
from django.utils import timezone

from mechanics.models import MechanicProfile
from service_requests.models import Job, JobStatus, RequestStatus

EARTH_RADIUS_KM = 6371


def find_nearest_mechanics(lat, lon, limit=5, search_radius_km=50):
    lat = float(lat)
    lon = float(lon)
    lat_delta = search_radius_km / 111.0
    lon_delta = search_radius_km / (111.0 * max(cos(radians(lat)), 0.01))

    # latitude/longitude are DecimalFields; cast to FloatField so they don't
    # clash with the plain-float lat/lon literals in the same expression
    # (mixing Decimal and Float arithmetic makes Django's ORM unable to
    # infer a single output_field and raises FieldError).
    db_lat = Cast(F("latitude"), output_field=FloatField())
    db_lon = Cast(F("longitude"), output_field=FloatField())

    haversine_arg = Sin(Radians(lat)) * Sin(Radians(db_lat)) + Cos(Radians(lat)) * Cos(
        Radians(db_lat)
    ) * Cos(Radians(db_lon) - Radians(lon))
    # Clamp to [-1, 1]: float rounding can push this a hair past 1.0 for
    # near-coincident points, which makes SQLite's ACOS() raise a domain error.
    clamped = Greatest(Value(-1.0), Least(Value(1.0), haversine_arg))

    return (
        MechanicProfile.objects.filter(
            is_available=True,
            is_verified=True,
            latitude__range=(lat - lat_delta, lat + lat_delta),
            longitude__range=(lon - lon_delta, lon + lon_delta),
        )
        .annotate(distance_km=EARTH_RADIUS_KM * ACos(clamped))
        .filter(distance_km__lte=F("service_radius_km"))
        .order_by("distance_km")[:limit]
    )


def accept_job(job):
    now = timezone.now()
    job.status = JobStatus.ACCEPTED
    job.responded_at = now
    job.save(update_fields=["status", "responded_at", "updated_at"])

    request = job.request
    request.status = RequestStatus.ACCEPTED
    request.save(update_fields=["status", "updated_at"])

    Job.objects.filter(request=request, status=JobStatus.PENDING).exclude(id=job.id).update(
        status=JobStatus.DECLINED, responded_at=now
    )
    return job


def decline_job(job):
    job.status = JobStatus.DECLINED
    job.responded_at = timezone.now()
    job.save(update_fields=["status", "responded_at", "updated_at"])
    return job


def complete_job(job):
    now = timezone.now()
    job.status = JobStatus.COMPLETED
    job.completed_at = now
    job.save(update_fields=["status", "completed_at", "updated_at"])

    request = job.request
    request.status = RequestStatus.COMPLETED
    request.save(update_fields=["status", "updated_at"])
    return job
