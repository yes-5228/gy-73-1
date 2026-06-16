import json

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.dateparse import parse_date, parse_time
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from tracking.models import ProgressEvent
from workers.models import Worker

from .models import MoveOrder
from .serializers import order_to_dict


def read_json(request):
    if not request.body:
        return {}
    return json.loads(request.body.decode("utf-8"))


def bad_request(message):
    return JsonResponse({"error": message}, status=400)


@csrf_exempt
@require_http_methods(["GET", "POST"])
def order_list(request):
    if request.method == "GET":
        status_filter = request.GET.get("status")
        queryset = MoveOrder.objects.select_related("claimed_by", "assigned_to")
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        return JsonResponse({"orders": [order_to_dict(order) for order in queryset]})

    payload = read_json(request)
    required = ["customer_name", "customer_phone", "origin", "destination", "move_date", "move_time"]
    missing = [field for field in required if not payload.get(field)]
    if missing:
        return bad_request(f"缺少字段: {', '.join(missing)}")

    order = MoveOrder.objects.create(
        customer_name=payload["customer_name"],
        customer_phone=payload["customer_phone"],
        origin=payload["origin"],
        destination=payload["destination"],
        move_date=parse_date(payload["move_date"]),
        move_time=parse_time(payload["move_time"]),
        items=payload.get("items", ""),
        note=payload.get("note", ""),
    )
    ProgressEvent.objects.create(order=order, stage=ProgressEvent.STAGE_CREATED, message="客户已提交搬家预约")
    return JsonResponse(order_to_dict(order, include_detail=True), status=201)


@require_http_methods(["GET"])
def order_detail(request, order_id):
    order = get_object_or_404(MoveOrder.objects.select_related("claimed_by", "assigned_to"), pk=order_id)
    return JsonResponse(order_to_dict(order, include_detail=True))


@csrf_exempt
@require_http_methods(["POST"])
def claim_order(request, order_id):
    order = get_object_or_404(MoveOrder, pk=order_id)
    payload = read_json(request)
    worker = get_object_or_404(Worker, pk=payload.get("worker_id"))
    if order.status != MoveOrder.STATUS_PENDING:
        return bad_request("只有待抢单订单可以抢单")

    order.claimed_by = worker
    order.status = MoveOrder.STATUS_CLAIMED
    order.save(update_fields=["claimed_by", "status", "updated_at"])
    ProgressEvent.objects.create(order=order, stage=ProgressEvent.STAGE_CLAIMED, worker=worker, message=f"{worker.name} 已抢单")
    return JsonResponse(order_to_dict(order, include_detail=True))


@csrf_exempt
@require_http_methods(["POST"])
def assign_order(request, order_id):
    order = get_object_or_404(MoveOrder, pk=order_id)
    payload = read_json(request)
    worker = get_object_or_404(Worker, pk=payload.get("worker_id"))
    if order.status not in [MoveOrder.STATUS_PENDING, MoveOrder.STATUS_CLAIMED]:
        return bad_request("当前订单状态不能派单")

    order.assigned_to = worker
    order.status = MoveOrder.STATUS_ASSIGNED
    if not order.claimed_by:
        order.claimed_by = worker
    order.save(update_fields=["assigned_to", "claimed_by", "status", "updated_at"])

    if worker.status == Worker.STATUS_AVAILABLE:
        worker.status = Worker.STATUS_BUSY
        worker.save(update_fields=["status"])

    ProgressEvent.objects.create(order=order, stage=ProgressEvent.STAGE_ASSIGNED, worker=worker, message=f"平台已派单给 {worker.name}")
    return JsonResponse(order_to_dict(order, include_detail=True))


@csrf_exempt
@require_http_methods(["POST"])
def cancel_order(request, order_id):
    order = get_object_or_404(MoveOrder, pk=order_id)
    payload = read_json(request)

    if not order.is_cancellable:
        return bad_request("当前订单状态不能取消")

    cancel_reason = payload.get("cancel_reason", "").strip()
    if not cancel_reason:
        return bad_request("请填写取消原因")

    cancelled_by = payload.get("cancelled_by", MoveOrder.CANCELLED_BY_DISPATCHER)
    if cancelled_by not in [MoveOrder.CANCELLED_BY_CUSTOMER, MoveOrder.CANCELLED_BY_DISPATCHER]:
        return bad_request("取消发起方无效")

    assigned_worker = order.assigned_to

    order.status = MoveOrder.STATUS_CANCELLED
    order.cancel_reason = cancel_reason
    order.cancelled_by = cancelled_by
    order.save(update_fields=["status", "cancel_reason", "cancelled_by", "updated_at"])

    if assigned_worker and assigned_worker.status == Worker.STATUS_BUSY:
        has_other_active_orders = MoveOrder.objects.filter(
            assigned_to=assigned_worker,
            status__in=[MoveOrder.STATUS_ASSIGNED, MoveOrder.STATUS_IN_PROGRESS],
        ).exclude(pk=order.pk).exists()
        if not has_other_active_orders:
            assigned_worker.status = Worker.STATUS_AVAILABLE
            assigned_worker.save(update_fields=["status"])

    cancelled_by_label = dict(MoveOrder.CANCELLED_BY_CHOICES).get(cancelled_by, cancelled_by)
    ProgressEvent.objects.create(
        order=order,
        stage=ProgressEvent.STAGE_CANCELLED,
        worker=assigned_worker,
        message=f"{cancelled_by_label}，原因：{cancel_reason}",
    )

    return JsonResponse(order_to_dict(order, include_detail=True))
