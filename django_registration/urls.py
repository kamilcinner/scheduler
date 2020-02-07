from django.urls import path
from django_registration import views

app_name = 'django_registration'
urlpatterns = [
    path('', views.UserCreateView.as_view(), name='user-create'),
]