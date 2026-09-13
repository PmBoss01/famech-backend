from django.contrib import admin

from service_requests.models import Job, Request


@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    list_display = ["id", "owner", "status", "created_at"]
    list_filter = ["status"]
    search_fields = ["description", "owner__username"]


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ["id", "request", "mechanic", "status", "created_at"]
    list_filter = ["status"]
    search_fields = ["mechanic__username"]
