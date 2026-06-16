from django.contrib import admin

from .models import ServiceReview


@admin.register(ServiceReview)
class ServiceReviewAdmin(admin.ModelAdmin):
    list_display = ("id", "order", "rating", "created_at")
    list_filter = ("rating",)
    search_fields = ("comment",)
