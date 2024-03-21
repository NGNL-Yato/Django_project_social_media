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

from django.conf.urls.static import static
from django.conf import settings

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
    # profile route to see my profile 
    path('myprofile/', views.profile, name='profile'),
    #
    # getter route to see other users profiles
    path('profile/<str:first_name>-<str:last_name>/', views.view_profile, name='profile'),
    #
    path('follow/<str:first_name>-<str:last_name>/', backendviews.follow_user, name='follow'),
    #
    path('unfollow/<str:first_name>-<str:last_name>/', backendviews.unfollow_user, name='unfollow'),
    
    path('remove_follower/<str:first_name>-<str:last_name>/', backendviews.remove_follower, name='remove_follower'),

    #
    path('classroom/home',views.homeClass_view,name='Classroom'),
    #
    path('classroom/Todo',views.todo_view,name='Todo'),
    #
    path('about/',views.index_view,name='about'),
    #
    path('chatApp/', views.chat_app_view, name='chat_app'),
    #
    path('settings/',backendviews.profile_settings , name='settings'),
    #
    # path('mes-posts/',backendviews.mesposts , name='settings'),
    #
    # path('mes-groups/',backendviews.mesgroupes , name='settings'),
    #
    path('my-Followers/',backendviews.myfollowers , name='myfollowers'),
    #
    path('my-Followings/',backendviews.myfollowings , name='myfollowings'),
    #
    path('test/',backendviews.test,name="test"),
    #
    path('contact/',views.contact_view,name="contact"),
    #
    path('classroom/course',views.course_view,name='Course'),
    #
    path('delete_post/<int:post_id>/', backendviews.delete_post, name='delete_post'),
    #
    path('like_post/<int:post_id>/', backendviews.like_post, name='like_post'),

    
    

    
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)