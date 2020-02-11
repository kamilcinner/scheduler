from django.urls import path
from task_manager import views

app_name = 'task_manager'
urlpatterns = [
    path('', views.index_view, name='index'),

    path('tasks/', views.TaskListView.as_view(), name='task-list'),
    path('task/<int:pk>', views.TaskDetailView.as_view(), name='task-detail'),
    path('task/create/', views.TaskCreateView.as_view(), name='task-create'),
    path('task/<int:pk>/update/', views.TaskUpdateView.as_view(), name='task-update'),
    path('task/<int:pk>/delete/', views.TaskDeleteView.as_view(), name='task-delete'),

    path('shoppinglists/', views.ShoppingListListView.as_view(), name='slist-list'),
    path('shoppinglist/<int:pk>', views.ShoppingListDetailView.as_view(), name='slist-detail'),
    path('shoppinglistitem/<int:pk>', views.mark_slist_item_bought, name='slist-item-mark-bought'),
    path('shoppinglist/create/', views.ShoppingListCreateView.as_view(), name='slist-create'),

    path('inactive/', views.inactive_yet_view, name='inactive-yet')
]