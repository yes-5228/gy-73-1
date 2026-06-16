from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class ServiceReview(models.Model):
    order = models.OneToOneField("orders.MoveOrder", related_name="service_review", on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"订单 {self.order_id}: {self.rating} 星"
