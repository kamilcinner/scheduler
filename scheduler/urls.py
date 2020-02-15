"""scheduler URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView


urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),

    path('register/', include('django_registration.urls')),

    path('scheduler/', include('task_manager.urls')),
    path('', RedirectView.as_view(url='scheduler/', permanent=True)),
]


handler400 = 'task_manager.views.bad_request'
# handler403 = 'task_manager.views.permission_denied'
handler404 = 'task_manager.views.page_not_found'
# handler500 = 'task_manager.views.server_error'
