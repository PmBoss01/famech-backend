from rest_framework import serializers

from mechanics.models import MechanicProfile


class MechanicProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = MechanicProfile
        fields = [
            "id",
            "business_name",
            "bio",
            "specialties",
            "years_experience",
            "latitude",
            "longitude",
            "location_landmark",
            "service_radius_km",
            "is_available",
            "is_verified",
        ]
        read_only_fields = ["id", "is_verified"]
