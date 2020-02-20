from django.urls import path
from task_manager import views

app_name = 'task_manager'
urlpatterns = [
    path('tasks/', views.TaskListView.as_view(), name='task-list'),
    path('task/<uuid:pk>/', views.TaskDetailView.as_view(), name='task-detail'),
    path('task/create/', views.TaskCreateView.as_view(), name='task-create'),
    path('task/<uuid:pk>/update/', views.TaskUpdateView.as_view(), name='task-update'),
    path('task/<uuid:pk>/delete/', views.TaskDeleteView.as_view(), name='task-delete'),
    path('task/<uuid:pk>/mark/', views.mark_task_done, name='task-mark'),
    path('task/<uuid:pk>/share/', views.share_task, name='task-share'),
]
