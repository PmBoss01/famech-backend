from rest_framework import serializers

from service_requests.models import Request


class RequestSummarySerializer(serializers.ModelSerializer):
    """Lightweight nested view of a Request for embedding on a Job response —
    just enough for a mechanic to review the fault before accepting/declining."""

    class Meta:
        model = Request
        fields = [
            "id",
            "description",
            "latitude",
            "longitude",
            "location_landmark",
            "photo",
            "audio",
            "vehicle_make",
            "vehicle_model",
            "vehicle_year",
        ]
