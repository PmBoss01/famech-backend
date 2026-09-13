from rest_framework import serializers

from users.models import CustomUser, phone_number_validator


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "username", "email", "first_name", "last_name", "role", "phone_number"]
        read_only_fields = ["id", "role"]


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    # Declared explicitly (required=True) since the model field is blank=True
    # for backward compatibility with pre-existing accounts — re-attach the
    # model's format validator since overriding the field drops DRF's
    # auto-derived one.
    phone_number = serializers.CharField(required=True, validators=[phone_number_validator])

    class Meta:
        model = CustomUser
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "role",
            "phone_number",
            "password",
        ]
        read_only_fields = ["id"]

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        return user
