from django.db import models


class Worker(models.Model):
    STATUS_AVAILABLE = "available"
    STATUS_BUSY = "busy"
    STATUS_OFFLINE = "offline"
    STATUS_CHOICES = [
        (STATUS_AVAILABLE, "可接单"),
        (STATUS_BUSY, "服务中"),
        (STATUS_OFFLINE, "离线"),
    ]

    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=30)
    vehicle = models.CharField(max_length=80)
    service_area = models.CharField(max_length=120)
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=5.0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_AVAILABLE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name
