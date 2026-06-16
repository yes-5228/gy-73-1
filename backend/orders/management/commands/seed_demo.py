from datetime import date, time, timedelta

from django.core.management.base import BaseCommand

from orders.models import MoveOrder
from tracking.models import ProgressEvent
from workers.models import Worker


class Command(BaseCommand):
    help = "Seed demo workers and moving orders."

    def handle(self, *args, **options):
        workers = [
            {
                "name": "张师傅",
                "phone": "13800000001",
                "vehicle": "4.2米厢货",
                "service_area": "浦东新区",
                "rating": 4.9,
            },
            {
                "name": "李师傅",
                "phone": "13800000002",
                "vehicle": "金杯面包车",
                "service_area": "徐汇区",
                "rating": 4.8,
            },
            {
                "name": "王师傅",
                "phone": "13800000003",
                "vehicle": "6.8米货车",
                "service_area": "静安区",
                "rating": 4.7,
            },
        ]
        for data in workers:
            Worker.objects.get_or_create(phone=data["phone"], defaults=data)

        if MoveOrder.objects.exists():
            self.stdout.write(self.style.SUCCESS("Demo data already exists."))
            return

        order = MoveOrder.objects.create(
            customer_name="陈女士",
            customer_phone="13900000088",
            origin="上海市徐汇区漕溪北路 88 号",
            destination="上海市浦东新区张江路 168 号",
            move_date=date.today() + timedelta(days=2),
            move_time=time(9, 30),
            items="两室一厅家具、冰箱、洗衣机、纸箱 20 个",
            note="需要拆装一张双人床",
        )
        ProgressEvent.objects.create(order=order, stage=ProgressEvent.STAGE_CREATED, message="客户已提交搬家预约")

        self.stdout.write(self.style.SUCCESS("Demo data seeded."))
