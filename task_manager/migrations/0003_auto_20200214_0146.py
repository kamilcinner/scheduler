# Generated by Django 3.0.2 on 2020-02-14 00:46

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task_manager', '0002_auto_20200211_0115'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='shoppinglistitem',
            options={'ordering': ['status', 'name']},
        ),
        migrations.AddField(
            model_name='task',
            name='status',
            field=models.BooleanField(default=False, verbose_name='Done'),
        ),
        migrations.AlterField(
            model_name='shoppinglist',
            name='date_added',
            field=models.DateTimeField(default=datetime.datetime(2020, 2, 14, 1, 46, 44, 67012)),
        ),
        migrations.AlterField(
            model_name='shoppinglistitem',
            name='name',
            field=models.CharField(blank=True, max_length=100, verbose_name='Product name'),
        ),
        migrations.AlterField(
            model_name='shoppinglistitem',
            name='status',
            field=models.BooleanField(default=False, verbose_name='Bought'),
        ),
        migrations.AlterField(
            model_name='task',
            name='due_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 2, 14, 1, 46, 44, 66067)),
        ),
    ]
