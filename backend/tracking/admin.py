from django.contrib import admin

from .models import ProgressEvent


@admin.register(ProgressEvent)
class ProgressEventAdmin(admin.ModelAdmin):
    list_display = ("id", "order", "stage", "worker", "created_at")
    list_filter = ("stage",)
    search_fields = ("message",)
