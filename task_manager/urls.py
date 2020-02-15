from django.urls import path
from task_manager import views

app_name = 'task_manager'
urlpatterns = [
    path('', views.index_view, name='index'),
    path('about/', views.about_view, name='about'),
    path('other/projects/', views.other_projects_view, name='other-projects'),
    path('inactive/', views.inactive_yet_view, name='inactive-yet'),

    path('tasks/', views.TaskListView.as_view(), name='task-list'),
    path('task/<uuid:pk>/', views.TaskDetailView.as_view(), name='task-detail'),
    path('task/create/', views.TaskCreateView.as_view(), name='task-create'),
    path('task/<uuid:pk>/update/', views.TaskUpdateView.as_view(), name='task-update'),
    path('task/<uuid:pk>/delete/', views.TaskDeleteView.as_view(), name='task-delete'),
    path('task/<uuid:pk>/mark/', views.mark_task_done, name='task-mark'),
    path('task/<uuid:pk>/share/', views.share_task, name='task-share'),

    path('shoppinglists/', views.ShoppingListListView.as_view(), name='slist-list'),
    path('shoppinglist/<uuid:pk>/', views.ShoppingListDetailView.as_view(), name='slist-detail'),
    path('shoppinglistitem/<uuid:pk>/', views.mark_slist_item_bought, name='slist-item-mark-bought'),
    path('shoppinglist/create/', views.ShoppingListCreateView.as_view(), name='slist-create'),
    path('shoppinglist/<uuid:pk>/update/', views.shoppinglist_update_view, name='slist-update'),
    path('shoppinglist/<uuid:pk>/delete/', views.ShoppingListDeleteView.as_view(), name='slist-delete'),
    path('shoppinglist/<uuid:pk>/share/', views.share_slist, name='slist-share'),
]