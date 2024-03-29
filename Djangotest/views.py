from django.shortcuts import render , redirect
from backend.models import User,utilisateur,Post,Like, Group, UserGroup,PostClassroom,ClassRoom
from backend.forms import PostForm, GroupForm, EventForm , ClassRoomForm,PostClassroomForm
from django.core.mail import send_mail
from django.conf import settings
from backend import models
from django.db.models import QuerySet
import random
import string

def home_view(request):
    all_users_names = []
    post_form = None
    group_form = None
    posts_visitor = Post.objects.all()
    posts = []

    if request.user.is_authenticated:
        all_my_followings = request.user.utilisateur.following.all()
        following_users = [f.followed.user for f in all_my_followings]
        following_posts = Post.objects.filter(user__in=following_users)

        user_groups = UserGroup.objects.filter(user=request.user).values_list('group', flat=True)
        group_posts = Post.objects.filter(group__in=user_groups)

        user_posts = Post.objects.filter(user=request.user)

        # Combine the querysets and order
        posts = following_posts.union(group_posts, user_posts).order_by('-created_at')

    groups = Group.objects.all()

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
                group.save()
                return redirect('groups')
        else:
            post_form = PostForm()
            group_form = GroupForm()

        isguest = False
        user = request.user
        user_email = user.email        
        user_first_name = user.first_name
        user_pdp = user.utilisateur.profile_picture

        all_users = utilisateur.objects.all()
        for util in all_users:
            if request.user == util.user:
                pass
            else:
                full_name = f"{util.user.first_name} {util.user.last_name}"
                online = util.online_status
                pdp = util.profile_picture
                
                obj = {
                    'full_name':full_name,
                    "online":'online' if online else 'offline',
                    'profile_picture': pdp
                }
                # print(obj)
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
                'eventform': EventForm()
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


 
def post_view(request):
    context = {}  
    return render(request,'HTML/userProfile/post.html', context)


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
    members_count = UserGroup.objects.filter(group=group).count()
    context = {'group': group, 'members_count': members_count, 'is_member': is_member, 'is_admin': is_admin, 'user': request.user, 'visiteur': isguest, 'target': target}
    return render(request, 'HTML/home/group-about.html', context)

def group_posts(request, group_name):
    isguest = not request.user.is_authenticated
    group = Group.objects.filter(group_name=group_name).first()
    posts = Post.objects.filter(group=group).order_by('-created_at')
    is_member = group.is_member(request.user)
    is_admin = group.is_admin(request.user)
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
    context = {'group': group, 'is_member': is_member, 'post_form': post_form, 'posts': posts, 'is_admin': is_admin, 'user': request.user, 'visiteur': isguest}
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
        form = PostClassroomForm(request.POST,request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.uid = uid
            post.author = models.Professor.objects.filter(utilisateur=request.user.utilisateur).first()
            post.save()
            classroom = ClassRoom.objects.get(UniqueinvitationCode=uid)
    return redirect('Course', UniqueinvitationCode=uid)



def course_view(request, uid):
    if request.user.is_authenticated:
        context = {
            'userdata':request.user,
            'classroomDetails': ClassRoom.objects.get(UniqueinvitationCode=uid),
            'form':PostClassroomForm()
            }  
        return render(request, 'HTML/classroom/course.html', context)
    


def chat(request):
    context = {}  
    return render(request,'HTML/Messaging/messages-page.html', context)

