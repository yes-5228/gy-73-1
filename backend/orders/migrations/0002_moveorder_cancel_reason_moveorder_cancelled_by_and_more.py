# Generated manually for order cancellation feature

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='moveorder',
            name='status',
            field=models.CharField(
                choices=[
                    ('pending', '待抢单'),
                    ('claimed', '已抢单'),
                    ('assigned', '已派单'),
                    ('in_progress', '服务中'),
                    ('completed', '已完成'),
                    ('cancelled', '已取消'),
                ],
                default='pending',
                max_length=20,
            ),
        ),
        migrations.AddField(
            model_name='moveorder',
            name='cancel_reason',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='moveorder',
            name='cancelled_by',
            field=models.CharField(
                blank=True,
                choices=[
                    ('customer', '客户取消'),
                    ('dispatcher', '调度员取消'),
                ],
                max_length=20,
                null=True,
            ),
        ),
    ]
