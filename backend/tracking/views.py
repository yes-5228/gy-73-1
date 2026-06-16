import json

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from orders.models import MoveOrder
from workers.models import Worker

from .models import ProgressEvent


def bad_request(message):
    return JsonResponse({"error": message}, status=400)


def event_to_dict(event):
    return {
        "id": event.id,
        "order_id": event.order_id,
        "stage": event.stage,
        "stage_label": event.get_stage_display(),
        "message": event.message,
        "created_at": event.created_at.isoformat(),
    }


@csrf_exempt
@require_http_methods(["POST"])
def add_progress(request, order_id):
    order = get_object_or_404(MoveOrder, pk=order_id)

    if order.status == MoveOrder.STATUS_CANCELLED:
        return bad_request("已取消的订单不能添加进度")

    payload = json.loads(request.body.decode("utf-8"))
    worker = None
    if payload.get("worker_id"):
        worker = get_object_or_404(Worker, pk=payload["worker_id"])

    stage = payload["stage"]
    event = ProgressEvent.objects.create(
        order=order,
        worker=worker,
        stage=stage,
        message=payload.get("message") or dict(ProgressEvent.STAGE_CHOICES).get(stage, stage),
    )
    if stage == ProgressEvent.STAGE_COMPLETED:
        order.status = MoveOrder.STATUS_COMPLETED
        if worker and worker.status == Worker.STATUS_BUSY:
            has_other_active_orders = MoveOrder.objects.filter(
                assigned_to=worker,
                status__in=[MoveOrder.STATUS_ASSIGNED, MoveOrder.STATUS_IN_PROGRESS],
            ).exclude(pk=order.pk).exists()
            if not has_other_active_orders:
                worker.status = Worker.STATUS_AVAILABLE
                worker.save(update_fields=["status"])
    elif stage in [ProgressEvent.STAGE_DEPARTED, ProgressEvent.STAGE_LOADING, ProgressEvent.STAGE_IN_TRANSIT, ProgressEvent.STAGE_UNLOADING]:
        order.status = MoveOrder.STATUS_IN_PROGRESS
        if worker and worker.status == Worker.STATUS_AVAILABLE:
            worker.status = Worker.STATUS_BUSY
            worker.save(update_fields=["status"])
    order.save(update_fields=["status", "updated_at"])
    return JsonResponse(event_to_dict(event), status=201)
