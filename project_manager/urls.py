"""
URL configuration for project_manager project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path, include
from django.views.generic import RedirectView
from django.contrib.auth import views as auth_views
from mirenda_manage.views import (home_view, login_view, register_view, project_view, create_project, create_task,
                                  mark_task_as_done, delete_task)


urlpatterns = [
    path('', RedirectView.as_view(url='home/'), name='root'),
    path('admin/', admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path('login/', login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', register_view, name='register'),
    path('home/', home_view, name='home'),
    path('projects/<int:pk>/', project_view, name='project_view'),
    path('create_project/', create_project, name='create_project'),
    path('create_task/', create_task, name='create_task'),
    path('task/<int:pk>/done/', mark_task_as_done, name='mark_task_as_done'),
    path('task/<int:pk>/delete/', delete_task, name='delete_task'),
]
