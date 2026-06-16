from django.db import models


class MoveOrder(models.Model):
    STATUS_PENDING = "pending"
    STATUS_CLAIMED = "claimed"
    STATUS_ASSIGNED = "assigned"
    STATUS_IN_PROGRESS = "in_progress"
    STATUS_COMPLETED = "completed"
    STATUS_CHOICES = [
        (STATUS_PENDING, "待抢单"),
        (STATUS_CLAIMED, "已抢单"),
        (STATUS_ASSIGNED, "已派单"),
        (STATUS_IN_PROGRESS, "服务中"),
        (STATUS_COMPLETED, "已完成"),
    ]

    customer_name = models.CharField(max_length=50)
    customer_phone = models.CharField(max_length=30)
    origin = models.CharField(max_length=160)
    destination = models.CharField(max_length=160)
    move_date = models.DateField()
    move_time = models.TimeField()
    items = models.TextField(blank=True)
    note = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    claimed_by = models.ForeignKey(
        "workers.Worker",
        related_name="claimed_orders",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    assigned_to = models.ForeignKey(
        "workers.Worker",
        related_name="assigned_orders",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.customer_name}: {self.origin} -> {self.destination}"
