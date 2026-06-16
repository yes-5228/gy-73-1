from django.contrib import admin

from .models import MoveOrder


@admin.register(MoveOrder)
class MoveOrderAdmin(admin.ModelAdmin):
    list_display = ("id", "customer_name", "origin", "destination", "move_date", "status", "assigned_to")
    list_filter = ("status", "move_date")
    search_fields = ("customer_name", "customer_phone", "origin", "destination")
