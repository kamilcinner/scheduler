from django.urls import path
from schedule_manager import views

app_name = 'schedule_manager'
urlpatterns = [
    path('scheduleweek/', views.schedule_week_detail_view, name='schedule-week'),

    path('activity/<uuid:pk>', views.ActivityDetailView.as_view(), name='activity-detail'),
    path('activity/create/', views.ActivityCreateView.as_view(), name='activity-create'),
    path('activity/<uuid:pk>/update', views.ActivityUpdateView.as_view(), name='activity-update'),
    path('activity/<uuid:pk>/delete', views.ActivityDeleteView.as_view(), name='activity-delete'),
]
