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
    path('profile/<str:first_name>-<str:last_name>/', views.view_profile, name='hisprofile'),
    #
    path('follow/<str:first_name>-<str:last_name>/', backendviews.follow_user, name='follow'),
    #
    path('unfollow/<str:first_name>-<str:last_name>/', backendviews.unfollow_user, name='unfollow'),
    #
    path('remove_follower/<str:first_name>-<str:last_name>/', backendviews.remove_follower, name='remove_follower'),
    #
    path('classroom/home',views.homeClass_view,name='Classroom'),
    #
    path('classroom/Join/<str:uid>',views.classroomJoin,name='classroomJoin'),
    #
    path('classroom/Todo',views.todo_view,name='Todo'),
    #
    path('classroom/course/<str:uid>',views.course_view,name='Course'),
    #
    path('create_QCM/<str:uid>/',views.createQCM , name="creatQCM"),
    #
    path('classroom/qcm/<int:qcmID>',views.qcm_view,name='qcm'),
    #
    path('addquestion/',views.addquestiontoqcm,name='addquestion'),
    #
    path('create_Classroom/',views.create_Classroom,name='createClassroom'),
    #
    path('create_Classroom_post/<str:uid>/', views.create_Classroom_post, name='createClassroomPost'),    
    #
    path('create_Task/<str:uid>/', views.create_Task, name='createTask'),    
    #
    path('deletequestion/<int:qstid>/',views.deletequestion , name="deletequestion"),
    #
    path('deleteClassroom/<str:uid>',views.delete_Classroom,name='deleteClassroom'),
    #
    path('deleteClassroomPost/<int:id>',views.delete_ClassroomPost,name='deleteClassroomPost'),
    #
    path('kickParticipant/<int:id>',views.kickparticipant , name='kickparticipant'),
    #
    path('about/',views.index_view,name='about'),
    #
    path('chatApp/', views.chat_app_view, name='chat_app'),
    #
    path('settings/',backendviews.profile_settings , name='settings'),
    #
    path('mes-recherches/',backendviews.Researches , name='recherches'),
    #
    path('deleterecherches/<int:id>',backendviews.deleteResearches , name='Deleterecherches'),
    #
    path('educations-settings/',backendviews.educationsSettings , name='educations-settings'),
    #
    path('deleteEducation/<int:id>',backendviews.deleteEducation,name='deleteEducation'),
    #
    # path('mes-groups/',backendviews.mesgroupes , name='mes-groups'),
    #
    path('certificates-settings/',backendviews.certificatesSettings , name='certificates-settings'),
    #
    path('deleteCertificate/<int:id>',backendviews.deletecertificates , name='delete-certificates-settings'),
    #
    path('Experiences-settings/',backendviews.ExperiencesSettings , name='Experiences-settings'),
    #
    path('deleteExperiences/<int:id>',backendviews.deleteExperiences,name='deleteExperiences'),
    #
    path('my-Followers/',backendviews.myfollowers , name='myfollowers'),
    #
    path('my-Followings/',backendviews.myfollowings , name='myfollowings'),
    #
    path('test/',backendviews.test,name="test"),
    #
    path('removeSkill/<int:id>',backendviews.removeSkill,name="removeSkill"),
    #
    path('removeLanguage/<int:id>',backendviews.removeLanguage,name="removeLanguage"),
    #
    path('contact/',views.contact_view,name="contact"),
    #
    path('delete_post/<int:post_id>/', backendviews.delete_post, name='delete_post'),
    #
    path('like_post/<int:post_id>/', backendviews.like_post, name='like_post'),
    #
    path('post/',views.post_view, name='post_view'),
    #
    path('groups/<str:group_name>/about', views.group_about, name='group_about'),
    #
    path('groups/<str:group_name>', views.group_posts, name='group_posts'),
    #
    path('groups/<str:group_name>/events', views.group_events, name='group_events'),
    #
    path('search_people/', backendviews.search_people, name='search_people'),  # new URL pattern
    #
    path('event/<int:id>',views.view_event,name='view_event'),
    #
    path('create_event/',views.create_event,name='create_event'),
    #
    path('deleteEvent/<int:id>',views.deleteEvent,name='deleteEvent'),
    #
    path('events/',views.all_events,name='all_events'),
    #
    path('invite_user/', backendviews.invite_user, name='invite_user'),
    #
    path('get_pending_invitations/', backendviews.get_pending_invitations, name='get_pending_invitations'),
    #
    path('accept_invitation/', backendviews.accept_invitation, name='accept_invitation'),
    #
    path('reject_invitation/', backendviews.reject_invitation, name='reject_invitation'),
    #
    path('join_group/', backendviews.join_group, name='join_group'),
    #
    path('leave_group/', backendviews.leave_group, name='leave_group'),
    #
    path('group/<str:group_name>/settings/', backendviews.group_settings, name='group_settings'),
    #
    path('toggle_admin/', backendviews.toggle_admin, name='toggle_admin'),
    #
    path('kick_user/', backendviews.kick_user, name='kick_user'),
    #
    path('cancel_invitation/', backendviews.cancel_invitation, name='cancel_invitation'),
    #
    path('chat/', views.chat, name='chat'),
    #
    path('get_friends/', backendviews.get_friends, name='get_friends'),
    #
    path('send_message/', backendviews.send_message, name='send_message'),
    #
    path('get_or_create_conversation/', backendviews.get_or_create_conversation, name='get_or_create_conversation'),


    
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)