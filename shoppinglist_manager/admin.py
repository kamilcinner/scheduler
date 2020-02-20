from django.contrib import admin

from shoppinglist_manager.models import ShoppingList, ShoppingListItem


admin.site.register(ShoppingList)
admin.site.register(ShoppingListItem)
