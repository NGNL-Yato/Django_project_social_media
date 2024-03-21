from django.shortcuts import render , redirect
from backend.models import User,utilisateur,Post,Like
from backend.forms import PostForm
from django.core.mail import send_mail
from django.conf import settings


def home_view(request):
    all_users_names = []
    form = None
    posts = Post.objects.all()

    if request.user.is_authenticated and request.user.is_superuser :
        return redirect('admin_panel')

    #
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = PostForm(request.POST, request.FILES)
            if form.is_valid():
                post = form.save(commit=False)
                post.user = request.user
                post.save()
                return redirect('home')
        else:
            form = PostForm()

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
                'form':form,
                'posts':posts,
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

def profile(request):
    context = {}  # You can pass context data to the template if needed
    return render(request,'HTML/userProfile/profile.html', context)


def view_profile(request,first_name, last_name):
    
    user = User.objects.get(first_name=first_name, last_name=last_name)
    if user is not None:    
        u = utilisateur.objects.get(user_id = user.id)
        if u is not None:
            context = {'utilisateur_data':u,
               'first_name':first_name,
                'last_name':last_name,
               }  
            return render(request, 'HTML/userProfile/profile.html', context)
        
    return redirect('home')
        
   

def welcome_view(request):
    context = {}  # You can pass context data to the template if needed
    return render(request,'HTML/welcome/welcome.html',context)
def homeClass_view(request):
    context = {}  # You can pass context data to the template if needed
    return render(request,'HTML/classroom/home.html',context)

def todo_view(request):
    context = {}  # You can pass context data to the template if needed
    return render(request,'HTML/classroom/Todo.html',context)


def chat_app_view(request):
    return render(request, 'HTML/userProfile/chatApp.html')


def contact_view(request):
    return render(request, 'HTML/userProfile/contactInfo.html')


def course_view(request):
    return render( request, 'HTML/classroom/course.html')  

 


