"""
URL configuration for Djangotest project.

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
from django.urls import path

from . import views
from backend import views as backendviews


urlpatterns = [
    path('admin/', admin.site.urls),
    #
    path('home/', views.home_view, name='home'),
    #
    path('', views.welcome_view, name='welcome'),
    #
    path('panel/', views.admin_panel, name='admin_panel'),
    #
    path('groups/', views.group_view, name='groups'),
    #
    path('login/', backendviews.login_in, name='login'),
    #
    path('signup/', backendviews.signup, name='signup'),
    #
    path('logout/',backendviews.login_out,name='logout'),
    #
    path('profile/', views.profile, name='profile'),
    #
    path('classroom/home',views.homeClass_view,name='Classroom'),
    #
    path('classroom/Todo',views.todo_view,name='Todo'),

    #
    path('about/',views.index_view,name='about'),
    
    #
    path('chatApp/', views.chat_app_view, name='chat_app'),



    
]
