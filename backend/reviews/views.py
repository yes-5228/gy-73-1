import json

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from orders.models import MoveOrder

from .models import ServiceReview


def review_to_dict(review):
    return {
        "id": review.id,
        "order_id": review.order_id,
        "rating": review.rating,
        "comment": review.comment,
        "created_at": review.created_at.isoformat(),
    }


@csrf_exempt
@require_http_methods(["POST"])
def create_review(request, order_id):
    order = get_object_or_404(MoveOrder, pk=order_id)
    if order.status != MoveOrder.STATUS_COMPLETED:
        return JsonResponse({"error": "服务完成后才能评价"}, status=400)

    payload = json.loads(request.body.decode("utf-8"))
    review, _created = ServiceReview.objects.update_or_create(
        order=order,
        defaults={"rating": payload["rating"], "comment": payload.get("comment", "")},
    )
    return JsonResponse(review_to_dict(review), status=201)


@require_http_methods(["GET"])
def review_list(_request):
    return JsonResponse({"reviews": [review_to_dict(review) for review in ServiceReview.objects.select_related("order")]})
