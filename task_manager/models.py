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


class ShoppingList(models.Model):
    class Meta:
        ordering = ['date_added']

    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=100, verbose_name='Shopping list name')
    date_added = models.DateTimeField(default=datetime.datetime.now())

    def get_absolute_url(self):
        return reverse('task_manager:slist-detail', args=[str(self.id)])

    def __str__(self):
        return f'{self.name} ({self.date_added.strftime("%Y-%m-%d %H:%M:%S")})'


class ShoppingListItem(models.Model):
    class Meta:
        ordering = ['status', 'name']

    s_list = models.ForeignKey(ShoppingList, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=100, verbose_name='Product name', blank=True)
    status = models.BooleanField(default=False, verbose_name='Bought')

    def get_absolute_url(self):
        return reverse('task_manager:slist-item-detail', args=[str(self.id)])

    def __str__(self):
        inscription = f'{self.name} '
        if self.status:
            inscription += '(Already bought)'
        else:
            inscription += '(Not bought)'
        return inscription
