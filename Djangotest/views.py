from django.shortcuts import render , redirect
from backend.models import User,utilisateur,Post,Like, Group, UserGroup,PostClassroom,ClassRoom, follow, Event, Skills, Languages, Certification, Education, Experience, Research
from backend.forms import PostForm, GroupForm, EventForm , ClassRoomForm,PostClassroomForm
from django.core.mail import send_mail
from django.conf import settings
from backend import models
from django.db.models import QuerySet
from django.http import JsonResponse
from django.urls import reverse
from django.db.models import Count
from random import choice
from django.db.models import Q

import random
import string

def home_view(request):
    all_users_names = []
    post_form = None
    group_form = None
    posts_visitor = Post.objects.all()
    posts = []
    latest_event = Event.objects.order_by('-created_at').first()
    random_group = choice(Group.objects.annotate(member_count=Count('user')).order_by('-member_count'))

    if request.user.is_authenticated:
        all_my_followings = request.user.utilisateur.following.all()
        following_users = [f.followed.user for f in all_my_followings]
        following_posts = Post.objects.filter(user__in=following_users)
        user_groups = UserGroup.objects.filter(user=request.user).values_list('group', flat=True)
        group_posts = Post.objects.filter(group__in=user_groups)
        user_posts = Post.objects.filter(user=request.user)
        posts = following_posts.union(group_posts, user_posts).order_by('-created_at')
        groups = Group.objects.filter(usergroup__user=request.user)
    else:
        groups = None
        group_posts = Post.objects.filter(group__target='public')
        user_posts = Post.objects.filter(group=None)
        posts = group_posts.union(user_posts).order_by('-created_at')
    if request.user.is_authenticated and request.user.is_superuser :
        return redirect('admin_panel')

    #
    if request.user.is_authenticated:
        if request.method == 'POST':
            post_form = PostForm(request.POST, request.FILES)
            group_form = GroupForm(request.POST, request.FILES)
            if post_form.is_valid():
                post = post_form.save(commit=False)
                post.user = request.user
                post.save()
                return redirect('home')
            elif group_form.is_valid():
                group = group_form.save(commit=False)
                group.user = request.user
                try:
                    group.save()
                    return JsonResponse({'status': 'redirect', 'location': reverse('group_posts', kwargs={'group_name': group.group_name})})                
                except ValueError:
                    return JsonResponse({'status': 'error', 'message': 'A group with this name already exists.'})
            else:
                print("Error found!")
                for field, errors in group_form.errors.items():
                    for error in errors:
                        print(f"{field}: {error}")        
        else:
            post_form = PostForm()
            group_form = GroupForm()

        isguest = False
        user = request.user
        user_email = user.email        
        user_first_name = user.first_name
        user_pdp = user.utilisateur.profile_picture

        friends = set()
        for f in user.utilisateur.following.all():
            if f.followed.followers.filter(follower=user.utilisateur).exists():
                friends.add(f.followed)
        friends = {friend for friend in friends if friend.following.filter(followed=user.utilisateur).exists()}

        for friend in friends:
            if len(all_users_names) >= 6:
                break
            full_name = f"{friend.user.first_name} {friend.user.last_name}"
            online = friend.online_status
            pdp = friend.profile_picture

            obj = {
                'full_name': full_name,
                "online": 'online' if online else 'offline',
                'profile_picture': pdp
            }
            all_users_names.append(obj)

    else:
        isguest = True
        user_email = "Guest@g.uae.ac.ma"       
        user_first_name = "visiteur"
        user_pdp = 'Images/us2.png'
        allUsers = ''
    
    context = {'visiteur':isguest,
               'user_email':user_email,
               'user_first_name':user_first_name,
               'usersobj':all_users_names,
               'user_pdp':user_pdp,
                'post_form':post_form,
                'group_form':group_form,
                'posts':posts,
                'posts_visitor':posts_visitor,
                'groups':groups,
                'isHomePage':True,
                'eventform': EventForm(),
                'latest_event': latest_event,
                'random_group': random_group,
               }
    
    return render(request, 'HTML/home/home.html', context)

def index_view(request):
    context = {}  # You can pass context data to the template if needed
    return render(request,'HTML/index/index.html',context)

def admin_panel(request):
    context = {}  # You can pass context data to the template if needed
    return render(request,'HTML/admin_panel/admin_panel.html', context)

def group_view(request):
    context = {}  # You can pass context data to the template if needed
    return render(request,'HTML/home/groupe_page.html', context)

def login_view(request):
    context = {}  # You can pass context data to the template if needed
    return render(request,'HTML/home/login.html', context)

# seeing my profile
def profile(request):
    context = {
            'userdata':request.user,
            'user_pdp':request.user.utilisateur.profile_picture,
            'utilisateurdata':request.user.utilisateur,
            'skills':models.Skills.objects.filter(utilisateur=request.user.utilisateur),
            'languages':models.Languages.objects.filter(utilisateur=request.user.utilisateur),
            'certificates':models.Certification.objects.filter(utilisateur=request.user.utilisateur),
            'Educations':models.Education.objects.filter(utilisateur=request.user.utilisateur),
            'Experiences':models.Experience.objects.filter(utilisateur=request.user.utilisateur),
            'Reaserches':models.Research.objects.filter(utilisateur=request.user.utilisateur),
            'myprofile':True,
               }  # You can pass context data to the template if needed
    return render(request,'HTML/userProfile/profile.html', context)

# seeing others profiles
def view_profile(request,first_name, last_name):
    
    user = User.objects.get(first_name=first_name, last_name=last_name)
    if user is not None:    
        u = utilisateur.objects.get(user_id = user.id)
        if u is not None:
            context = {'userdata':user,
                       'user_pdp': u.profile_picture,
                        'first_name':first_name,
                        'last_name':last_name,
                        'utilisateurdata':u,
            'skills':models.Skills.objects.filter(utilisateur=u),
            'languages':models.Languages.objects.filter(utilisateur=u),
            'certificates':models.Certification.objects.filter(utilisateur=u),
            'Educations':models.Education.objects.filter(utilisateur=u),
            'Experiences':models.Experience.objects.filter(utilisateur=u),
            'Reaserches':models.Research.objects.filter(utilisateur=u),
                        'myprofile':False,
               }  
            return render(request, 'HTML/userProfile/profile.html', context)
        
    return redirect('home')
        
   

def welcome_view(request):
    context = {}  # You can pass context data to the template if needed
    return render(request,'HTML/welcome/welcome.html',context)

# 
def homeClass_view(request):
    if request.user.is_authenticated:
        context = {
            'userdata':request.user,
            'classrooms':models.ClassRoom.objects.all(),
            'ClassRoomform':ClassRoomForm()
            }  
        return render(request,'HTML/classroom/home.html',context)
    else:
        return redirect('login')

def todo_view(request):
    context = {}  # You can pass context data to the template if needed
    return render(request,'HTML/classroom/Todo.html',context)


def chat_app_view(request):
    return render(request, 'HTML/userProfile/chatApp.html')


def contact_view(request):
    return render(request, 'HTML/userProfile/contactInfo.html')

 
def post_view(request):
    context = {}  
    return render(request,'HTML/userProfile/post.html', context)


 
# def post_view(request):
#     context = {}  
#     return render(request,'HTML/userProfile/post.html', context)


def generate_random_code(length=8):
    characters = string.ascii_letters + string.digits  # includes both uppercase and lowercase letters and digits
    return ''.join(random.choice(characters) for _ in range(length))


#
def create_Classroom(request):
    if request.user.is_authenticated and request.method == 'POST':
        form = ClassRoomForm(request.POST,request.FILES)
        if form.is_valid():
            
            unique_code = generate_random_code()
            while models.ClassRoom.objects.filter(UniqueinvitationCode=unique_code).exists():
                unique_code = generate_random_code() 

            f = form.save(commit=False)
            f.Admin_Professor = models.Professor.objects.filter(utilisateur=request.user.utilisateur).first()
            f.UniqueinvitationCode = unique_code
            f.save()

    return redirect('Classroom')

#
def create_event(request):
    if request.user.is_authenticated and request.method == 'POST':
        form = EventForm(request.POST,request.FILES)
        print(request.POST)
        if form.is_valid():
            f = form.save(commit=False)
            f.utilisateur = models.utilisateur.objects.get(user_id=request.user.id)
            f.save()

    return redirect('all_events')


def view_event(request,id):   
    if request.user.is_authenticated:
        visiteur =False
    else:
        visiteur = True
    context={
        'eventContent':models.Event.objects.filter(id=id).first(),
        'user':request.user,
        'visiteur':visiteur,
    }
    return render(request,'HTML/Events/event.html',context)

# delete event
def deleteEvent(request, id):
    ev = models.Event.objects.filter(id=id).first()
    if ev is not None:
        ev.delete()
        return redirect('all_events')

    return redirect('home')


def all_events(request):
    
    if request.user.is_authenticated:
        isGuest = False
        user = request.user
        user_first_name = user.first_name
        user_pdp = user.utilisateur.profile_picture
    else:
        isGuest = True
        user_first_name = "visiteur"
        user_pdp = 'Images/us2.png'

    context = {'visiteur':isGuest,
               'user_first_name':user_first_name,
               'user_pdp':user_pdp,
                'isHomePage':False,
                'isEventsPage':True,
                'all_events':models.Event.objects.all(),
               }

    return render(request,'HTML/home/home.html',context)


def group_about(request, group_name):
    group = Group.objects.filter(group_name=group_name).first()
    isguest = not request.user.is_authenticated
    is_member = group.is_member(request.user)
    is_admin = group.is_admin(request.user)
    target = group.target
    members_count = UserGroup.objects.filter(group=group,invitation_on=True).count()
    context = {'group': group, 'members_count': members_count, 'is_member': is_member, 'is_admin': is_admin, 'user': request.user, 'visiteur': isguest, 'target': target}
    return render(request, 'HTML/home/group-about.html', context)

def group_posts(request, group_name):
    isguest = not request.user.is_authenticated
    group = Group.objects.filter(group_name=group_name).first()
    posts = Post.objects.filter(group=group).order_by('-created_at')
    is_member = group.is_member(request.user)
    is_admin = group.is_admin(request.user)
    target = group.target
    if request.method == 'POST':
        post_form = PostForm(request.POST, request.FILES)
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.user = request.user
            post.group = group
            post.save()
            return redirect('group_posts', group_name=group.group_name)
    else:
        post_form = PostForm()
    context = {'group': group, 'is_member': is_member, 'post_form': post_form, 'posts': posts, 'is_admin': is_admin, 'user': request.user, 'visiteur': isguest, 'target': target}
    return render(request, 'HTML/home/groupe_page.html', context)

def group_events(request, group_name):
    group = Group.objects.filter(group_name=group_name).first()
    isguest = not request.user.is_authenticated
    is_member = group.is_member(request.user)
    is_admin = group.is_admin(request.user)
    context = {'group': group, 'is_member': is_member, 'is_admin': is_admin, 'user': request.user, 'visiteur': isguest}
    return render(request, 'HTML/home/group_events.html', context)

def qcm_view(request):
    return render( request, 'HTML/classroom/qcm.html') 

 
def create_Classroom_post(request, uid):
    if request.user.is_authenticated and request.method == 'POST':
        classroom = models.ClassRoom.objects.get(UniqueinvitationCode=uid)
        print(classroom)
        if classroom is not None:
            form = PostClassroomForm(request.POST,request.FILES)
            print(form.is_valid())
            if form.is_valid():
                post = form.save(commit=False)
                post.classroom = classroom
                post.author = models.Professor.objects.filter(utilisateur=request.user.utilisateur).first()
                post.save()

    return redirect('Course', uid=uid)



def course_view(request, uid):
    if request.user.is_authenticated:
        classroom = ClassRoom.objects.get(UniqueinvitationCode=uid)
        context = {
            'userdata':request.user,
            'classroomDetails': classroom,
            'form':PostClassroomForm(),
            'classroom_posts':models.PostClassroom.objects.filter(classroom=classroom).order_by('-created_at')
            }  
        return render(request, 'HTML/classroom/course.html', context)
    


def chat(request):
    context = {}  
    return render(request,'HTML/Messaging/messages-page.html', context)

def delete_Classroom(request, uid):
    classroom = models.ClassRoom.objects.filter(UniqueinvitationCode=uid).first()
    if classroom is not None:
        classroom.delete()
        return redirect('Classroom')

#
def delete_ClassroomPost(request, id):
    post = models.PostClassroom.objects.filter(id=id).first()
    if post is not None:
            uid = post.classroom.UniqueinvitationCode

            post.delete()
            return redirect('Course',uid=uid)
#
def all_groups(request):
    query = request.GET.get('q')
    if query:
        groups = models.Group.objects.filter(target='public', group_name__icontains=query)
    else:
        groups = models.Group.objects.filter(target='public')
    context = {'groups': groups}
    return render(request, 'HTML/components/groups.html', context)

from django.db.models import Q

def all_utilisateurs(request):
    query = request.GET.get('q')
    skills_query = request.GET.get('skills')
    experiences_query = request.GET.get('experiences')
    languages_query = request.GET.get('languages')
    certifications_query = request.GET.get('certifications')
    educations_query = request.GET.get('educations')
    researches_query = request.GET.get('researches')

    users = models.User.objects.filter(is_superuser=False)
    if query or skills_query or experiences_query or languages_query or certifications_query or educations_query or researches_query:
        if query:
            users = users.filter(Q(first_name__icontains=query) | Q(last_name__icontains=query))
        if skills_query:
            users = users.filter(utilisateur__skills__SkillName__icontains=skills_query)
        if experiences_query:
            users = users.filter(Q(utilisateur__experience__titre__icontains=experiences_query) | Q(utilisateur__experience__entreprise__icontains=experiences_query))
        if languages_query:
            users = users.filter(utilisateur__languages__Language__icontains=languages_query)
        if certifications_query:
            users = users.filter(utilisateur__certification__Nom_Certificat__icontains=certifications_query)
        if educations_query:
            users = users.filter(Q(utilisateur__education__UniversityName__icontains=educations_query) | Q(utilisateur__education__FiledOfStudy__icontains=educations_query))
        if researches_query:
            users = users.filter(utilisateur__research__recherche_referrence__icontains=researches_query)

        skills = Skills.objects.filter(SkillName__icontains=skills_query) if skills_query else Skills.objects.none()
        experiences = Experience.objects.filter(Q(titre__icontains=experiences_query) | Q(entreprise__icontains=experiences_query)) if experiences_query else Experience.objects.none()
        languages = Languages.objects.filter(Language__icontains=languages_query) if languages_query else Languages.objects.none()
        certifications = Certification.objects.filter(Nom_Certificat__icontains=certifications_query) if certifications_query else Certification.objects.none()
        educations = Education.objects.filter(Q(UniversityName__icontains=educations_query) | Q(FiledOfStudy__icontains=educations_query)) if educations_query else Education.objects.none()
        researches = Research.objects.filter(recherche_referrence__icontains=researches_query) if researches_query else Research.objects.none()

        etudiants = [user.utilisateur for user in users if hasattr(user, 'utilisateur') and hasattr(user.utilisateur, 'etudiant')]
        professors = list(set([user.utilisateur for user in users if hasattr(user, 'utilisateur') and hasattr(user.utilisateur, 'professor')]))
        enterprises = [user.utilisateur for user in users if hasattr(user, 'utilisateur') and hasattr(user.utilisateur, 'enterprise')]

        context = {'etudiants': etudiants, 'professors': professors, 'enterprises': enterprises, 'skills': skills, 'experiences': experiences, 'languages': languages, 'certifications': certifications, 'educations': educations, 'researches': researches}
    
    else:
        users = models.User.objects.filter(is_superuser=False)[:20]
        context = {'users': users}

    return render(request, 'HTML/components/users.html', context)