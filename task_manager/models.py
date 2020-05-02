import uuid

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone

from task_manager.utils import get_default_datetime


class Task(models.Model):
    class Meta:
        ordering = ['status', 'due_date', 'priority']

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=100, verbose_name='Task name')
    due_date = models.DateTimeField(default=get_default_datetime())
    description = models.TextField(max_length=5000)
    status = models.BooleanField(default=False, verbose_name='Done')
    is_shared = models.BooleanField(default=False)

    TASK_PRIORITIES = (
        ('h', 'High'),
        ('n', 'Normal'),
        ('l', 'Low')
    )

    priority = models.CharField(max_length=1, choices=TASK_PRIORITIES, default='n')

    @property
    def is_overdue(self):
        if self.due_date < timezone.now():
            return True
        return False

    @property
    def crispy_time(self):
        return f'{self.due_date.astimezone(timezone.get_default_timezone()).time().strftime("%H:%M")}'

    def get_absolute_url(self):
        return reverse('task_manager:task-detail', args=[str(self.id)])

    def __str__(self):
        return f'{self.name} ({self.due_date.astimezone(timezone.get_default_timezone()).strftime("%d %b %Y %H:%M")})'
