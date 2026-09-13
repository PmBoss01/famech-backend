import uuid

from django.db import models
from uuslug import uuslug


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SlugBaseModel(BaseModel):
    slug = models.SlugField(max_length=256, unique=True, editable=False)

    def save(self, *args, **kwargs):
        title_or_name = getattr(self, "title", None) or getattr(self, "name", None)
        if title_or_name:
            self.slug = uuslug(title_or_name, instance=self)
        super().save(*args, **kwargs)

    class Meta:
        abstract = True
