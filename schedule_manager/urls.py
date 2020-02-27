from django.urls import path
from schedule_manager import views

app_name = 'schedule_manager'
urlpatterns = [
    path('scheduleweek/', views.schedule_week_detail_view, name='schedule-week'),

    path('activity/<uuid:pk>', views.ActivityDetailView.as_view(), name='activity-detail'),
    path('activities/', views.ActivityListView.as_view(), name='activity-list'),
    path('activity/create/', views.ActivityCreateView.as_view(), name='activity-create'),
    path('activity/<uuid:pk>/update', views.ActivityUpdateView.as_view(), name='activity-update'),
    path('activity/<uuid:pk>/delete', views.ActivityDeleteView.as_view(), name='activity-delete'),

    path('activity/<uuid:pk>/changeactivity', views.change_activity_status, name='activity-change-active'),
    path('activity/<uuid:pk>/changerepeat', views.change_repeat_status, name='activity-change-repeat'),
]
