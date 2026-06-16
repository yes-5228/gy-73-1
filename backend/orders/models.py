from django.db import models


class MoveOrder(models.Model):
    STATUS_PENDING = "pending"
    STATUS_CLAIMED = "claimed"
    STATUS_ASSIGNED = "assigned"
    STATUS_IN_PROGRESS = "in_progress"
    STATUS_COMPLETED = "completed"
    STATUS_CANCELLED = "cancelled"
    STATUS_CHOICES = [
        (STATUS_PENDING, "待抢单"),
        (STATUS_CLAIMED, "已抢单"),
        (STATUS_ASSIGNED, "已派单"),
        (STATUS_IN_PROGRESS, "服务中"),
        (STATUS_COMPLETED, "已完成"),
        (STATUS_CANCELLED, "已取消"),
    ]

    CANCELLED_BY_CUSTOMER = "customer"
    CANCELLED_BY_DISPATCHER = "dispatcher"
    CANCELLED_BY_CHOICES = [
        (CANCELLED_BY_CUSTOMER, "客户取消"),
        (CANCELLED_BY_DISPATCHER, "调度员取消"),
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
    cancel_reason = models.TextField(blank=True)
    cancelled_by = models.CharField(max_length=20, choices=CANCELLED_BY_CHOICES, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.customer_name}: {self.origin} -> {self.destination}"

    @property
    def is_cancellable(self):
        return self.status in [self.STATUS_PENDING, self.STATUS_CLAIMED, self.STATUS_ASSIGNED]
