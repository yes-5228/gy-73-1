from django.db import models


class ProgressEvent(models.Model):
    STAGE_CREATED = "created"
    STAGE_CLAIMED = "claimed"
    STAGE_ASSIGNED = "assigned"
    STAGE_DEPARTED = "departed"
    STAGE_LOADING = "loading"
    STAGE_IN_TRANSIT = "in_transit"
    STAGE_UNLOADING = "unloading"
    STAGE_COMPLETED = "completed"
    STAGE_CHOICES = [
        (STAGE_CREATED, "已预约"),
        (STAGE_CLAIMED, "已抢单"),
        (STAGE_ASSIGNED, "已派单"),
        (STAGE_DEPARTED, "已出发"),
        (STAGE_LOADING, "装车中"),
        (STAGE_IN_TRANSIT, "运输中"),
        (STAGE_UNLOADING, "卸货中"),
        (STAGE_COMPLETED, "已完成"),
    ]

    order = models.ForeignKey("orders.MoveOrder", related_name="progress_events", on_delete=models.CASCADE)
    worker = models.ForeignKey("workers.Worker", null=True, blank=True, on_delete=models.SET_NULL)
    stage = models.CharField(max_length=20, choices=STAGE_CHOICES)
    message = models.CharField(max_length=220)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.order_id} - {self.get_stage_display()}"
