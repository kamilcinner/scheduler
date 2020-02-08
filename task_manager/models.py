import datetime

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Task(models.Model):
    class Meta:
        ordering = ['due_date']

    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=100, verbose_name='Task name')
    due_date = models.DateTimeField(default=datetime.datetime.now())
    description = models.TextField(max_length=5000)

    TASK_PRIORITIES = (
        ('h', 'High'),
        ('n', 'Normal'),
        ('l', 'Low')
    )

    priority = models.CharField(max_length=1, choices=TASK_PRIORITIES, default='n')

    def get_absolute_url(self):
        return reverse('task_manager:task-detail', args=[str(self.id)])

    def __str__(self):
        return f'{self.name} ({self.due_date.strftime("%Y-%m-%d %H:%M:%S")})'
