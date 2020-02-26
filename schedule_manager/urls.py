from django.urls import path
from schedule_manager import views

app_name = 'schedule_manager'
urlpatterns = [
    path('scheduleweek/', views.schedule_week_detail_view, name='schedule-week'),
    path('activity/create/', views.ActivityCreateModelView.as_view(), name='activity-create')
]
