from rest_framework import serializers

from service_requests.models import Request
from service_requests.serializers.job import JobOfferSummarySerializer


class RequestSerializer(serializers.ModelSerializer):
    jobs = JobOfferSummarySerializer(many=True, read_only=True)

    class Meta:
        model = Request
        fields = [
            "id",
            "owner",
            "description",
            "latitude",
            "longitude",
            "location_landmark",
            "photo",
            "audio",
            "vehicle_make",
            "vehicle_model",
            "vehicle_year",
            "status",
            "jobs",
            "created_at",
        ]
        read_only_fields = ["id", "owner", "status", "jobs", "created_at"]
