from django.urls import path
from shoppinglist_manager import views

app_name = 'shoppinglist_manager'
urlpatterns = [
    path('shoppinglists/', views.ShoppingListListView.as_view(), name='slist-list'),
    path('shoppinglist/<uuid:pk>/', views.ShoppingListDetailView.as_view(), name='slist-detail'),
    path('shoppinglistitem/<uuid:pk>/', views.mark_slist_item_bought, name='slist-item-mark-bought'),
    path('shoppinglist/create/', views.ShoppingListCreateView.as_view(), name='slist-create'),
    path('shoppinglist/<uuid:pk>/update/', views.shoppinglist_update_view, name='slist-update'),
    path('shoppinglist/<uuid:pk>/delete/', views.ShoppingListDeleteView.as_view(), name='slist-delete'),
    path('shoppinglist/<uuid:pk>/share/', views.share_slist, name='slist-share'),
]
