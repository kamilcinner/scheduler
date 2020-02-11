from django.contrib import admin

from task_manager.models import Task, ShoppingList, ShoppingListItem

admin.site.register(Task)
admin.site.register(ShoppingList)
admin.site.register(ShoppingListItem)