from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from .models import CustomUser


@admin.register(CustomUser)
class UserAdmin(DjangoUserAdmin):
    list_display = ["username", "email", "role", "phone_number", "is_staff"]
    fieldsets = DjangoUserAdmin.fieldsets + (
        ("FAMECH", {"fields": ("role", "phone_number")}),
    )
