from django.contrib import admin

from mechanics.models import MechanicProfile


@admin.register(MechanicProfile)
class MechanicProfileAdmin(admin.ModelAdmin):
    list_display = ["business_name", "user", "is_available", "is_verified", "service_radius_km"]
    list_filter = ["is_available", "is_verified"]
    search_fields = ["business_name", "user__username", "user__email"]
