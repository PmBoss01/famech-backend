from rest_framework import serializers

from service_requests.models import Job
from service_requests.serializers.request_summary import RequestSummarySerializer
from users.serializers import UserSerializer


class JobSerializer(serializers.ModelSerializer):
    mechanic = UserSerializer(read_only=True)
    request = RequestSummarySerializer(read_only=True)

    class Meta:
        model = Job
        fields = [
            "id",
            "request",
            "mechanic",
            "status",
            "price",
            "responded_at",
            "completed_at",
            "created_at",
        ]
        read_only_fields = ["id", "request", "mechanic", "status", "responded_at", "completed_at", "created_at"]


class JobOfferSummarySerializer(serializers.ModelSerializer):
    """Lightweight nested view of a Job for embedding on a Request's detail response."""

    mechanic_name = serializers.CharField(source="mechanic.username", read_only=True)

    class Meta:
        model = Job
        fields = ["id", "mechanic_name", "status", "price"]
