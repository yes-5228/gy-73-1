import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .models import Worker
from .serializers import worker_to_dict


@csrf_exempt
@require_http_methods(["GET", "POST"])
def worker_list(request):
    if request.method == "GET":
        return JsonResponse({"workers": [worker_to_dict(worker) for worker in Worker.objects.all()]})

    payload = json.loads(request.body.decode("utf-8"))
    worker = Worker.objects.create(
        name=payload["name"],
        phone=payload["phone"],
        vehicle=payload["vehicle"],
        service_area=payload.get("service_area", ""),
        rating=payload.get("rating", 5.0),
        status=payload.get("status", Worker.STATUS_AVAILABLE),
    )
    return JsonResponse(worker_to_dict(worker), status=201)
