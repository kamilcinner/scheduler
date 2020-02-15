# Generated by Django 3.0.2 on 2020-02-14 11:15

import datetime
from django.db import migrations, models
from django.utils.timezone import utc
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('task_manager', '0003_auto_20200214_0146'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='task',
            options={'ordering': ['status', 'due_date', 'priority']},
        ),
        migrations.AlterField(
            model_name='shoppinglist',
            name='date_added',
            field=models.DateTimeField(default=datetime.datetime(2020, 2, 14, 11, 15, 28, 548061, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='shoppinglist',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='task',
            name='due_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 2, 14, 11, 15, 28, 547332, tzinfo=utc)),
        ),
    ]