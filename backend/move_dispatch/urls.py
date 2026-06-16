from django.contrib import admin
from django.urls import include, path
from django.http import JsonResponse


def health(_request):
    return JsonResponse({"status": "ok", "service": "moving-dispatch-api"})


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/health/", health),
    path("api/orders/", include("orders.urls")),
    path("api/workers/", include("workers.urls")),
    path("api/tracking/", include("tracking.urls")),
    path("api/reviews/", include("reviews.urls")),
]
