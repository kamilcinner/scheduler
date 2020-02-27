import uuid

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone

from schedule_manager.utils import get_default_time


class Activity(models.Model):
    class Meta:
        ordering = [
            'date',
            'time_start'
        ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=100, verbose_name='Activity name')
    description = models.TextField(max_length=500, blank=True, null=True)
    time_start = models.TimeField(default=get_default_time())
    time_end = models.TimeField(default=get_default_time(hours_shift=2))
    date = models.DateField(default=timezone.datetime.today)
    status_active = models.BooleanField(default=True)
    repeat_weekly = models.BooleanField(default=False)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.name}, {self.date} ({self.get_week_day_name}) ({self.get_crispy_time})'

    def get_absolute_url(self):
        return reverse('schedule_manager:activity-detail', args=[str(self.id)])

    @property
    def get_week_day_name(self):
        return f'{self.date.strftime("%A")}'

    @property
    def get_crispy_time(self):
        return f'{self.time_start.strftime("%H:%M")} - {self.time_end.strftime("%H:%M")}'
