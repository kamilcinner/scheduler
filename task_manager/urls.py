from django.urls import path
from task_manager import views

app_name = 'task_manager'
urlpatterns = [
    path('', views.index_view, name='index'),
    path('about/', views.about_view, name='about'),
    path('other/projects/', views.other_projects_view, name='other-projects'),

    path('tasks/', views.TaskListView.as_view(), name='task-list'),
    path('task/<int:pk>', views.TaskDetailView.as_view(), name='task-detail'),
    path('task/create/', views.TaskCreateView.as_view(), name='task-create'),
    path('task/<int:pk>/update/', views.TaskUpdateView.as_view(), name='task-update'),
    path('task/<int:pk>/delete/', views.TaskDeleteView.as_view(), name='task-delete'),
    path('task/<int:pk>/mark/', views.mark_task_done, name='task-mark'),

    path('shoppinglists/', views.ShoppingListListView.as_view(), name='slist-list'),
    path('shoppinglist/<uuid:pk>', views.ShoppingListDetailView.as_view(), name='slist-detail'),
    path('shoppinglistitem/<int:pk>', views.mark_slist_item_bought, name='slist-item-mark-bought'), # TODO: fix because this is not safe
    path('shoppinglist/create/', views.ShoppingListCreateView.as_view(), name='slist-create'),
    path('shoppinglist/<uuid:pk>/update/', views.shoppinglist_update_view, name='slist-update'),
    path('shoppinglist/<uuid:pk>/delete/', views.ShoppingListDeleteView.as_view(), name='slist-delete'),
    path('shoppinglist/<uuid:pk>/share/', views.share_slist, name='slist-share'),
    # path('shared/<uuid:pk>', views.SharedShoppingListDetailView.as_view(), name='sslist-detail'),

    path('inactive/', views.inactive_yet_view, name='inactive-yet')
]