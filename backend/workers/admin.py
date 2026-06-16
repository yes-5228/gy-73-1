from django.contrib import admin

from .models import Worker


@admin.register(Worker)
class WorkerAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "phone", "vehicle", "service_area", "rating", "status")
    list_filter = ("status", "service_area")
    search_fields = ("name", "phone", "vehicle")
