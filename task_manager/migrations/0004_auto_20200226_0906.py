# Generated by Django 3.0.2 on 2020-02-26 08:06

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('task_manager', '0003_auto_20200225_2243'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='due_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 2, 26, 10, 0, tzinfo=utc)),
        ),
    ]
