from django.core.exceptions import ValidationError

MAX_IMAGE_SIZE_BYTES = 5 * 1024 * 1024
MAX_AUDIO_SIZE_BYTES = 10 * 1024 * 1024


def validate_image_size(f):
    if f.size > MAX_IMAGE_SIZE_BYTES:
        raise ValidationError("Photo must be under 5MB.")


def validate_audio_size(f):
    if f.size > MAX_AUDIO_SIZE_BYTES:
        raise ValidationError("Audio must be under 10MB.")
