import uuid

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone


class ShoppingList(models.Model):
    class Meta:
        ordering = ['date_added']

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=100, verbose_name='Shopping list name')
    date_added = models.DateTimeField(default=timezone.now)  # TODO: maybe change name to last_edit because we-re using this that way
    is_shared = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse('shoppinglist_manager:slist-detail', args=[str(self.id)])

    def __str__(self):
        return f'{self.name} ({self.date_added.strftime("%d %b %Y %H:%M")})'


class ShoppingListItem(models.Model):
    class Meta:
        ordering = ['status', 'name']

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    s_list = models.ForeignKey(ShoppingList, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100, verbose_name='Product name', blank=True)
    status = models.BooleanField(default=False, verbose_name='Bought')

    def __str__(self):
        inscription = f'{self.name} '
        if self.status:
            inscription += '(Already bought)'
        else:
            inscription += '(Not bought)'
        return inscription
