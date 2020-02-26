import uuid

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


# TODO: this must be created when initializing Activity ||| or just get rid of this Model
# class ScheduledDay(models.Model):
#     class Meta:
#         ordering = ['date']
#
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4)
#     date = models.DateField(default=timezone.datetime.today)
#     owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)


# TODO: add create, update, delete ModelView
class Activity(models.Model):
    class Meta:
        ordering = [
            'date',
            'time_start'
        ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=100, verbose_name='Activity name')
    time_start = models.TimeField(default=timezone.datetime.now().time())  # TODO: change this later
    time_end = models.TimeField(default=timezone.datetime.now().time())  # TODO: change this later
    # day = models.ForeignKey(ScheduledDay, on_delete=models.SET_NULL, null=True)
    date = models.DateField(default=timezone.datetime.today)
    status_active = models.BooleanField(default=True)  # TODO: implement this in view
    repeat_weekly = models.BooleanField(default=True)  # TODO: implement this in view
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)  # for safety purposes

    def __str__(self):
        return f'{self.name} {self.time_start.strftime("%H:%M")} - {self.time_end.strftime("%H:%M")}'
