import uuid

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class ScheduledDay(models.Model):
    class Meta:
        ordering = ['date']

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    date = models.DateField(default=timezone.datetime.today)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)


class Activity(models.Model):
    class Meta:
        ordering = ['time_start']

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=100)
    time_start = models.TimeField()
    time_end = models.TimeField()
    day = models.ForeignKey(ScheduledDay, on_delete=models.SET_NULL, null=True)
    status_active = models.BooleanField(default=True)
    repeat_weekly = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.name} {self.time_start.strftime("%H:%M")} - {self.time_end.strftime("%H:%M")}'
