from django.shortcuts import render

def home_view(request):
    #
    if request.user.is_authenticated:
        isguest = False
        user = request.user
        user_email = user.email        
        user_first_name = user.first_name
    else:
        isguest = True
        user_email = "Guest@g.uae.ac.ma"       
        user_first_name = "visiteur"
    
    context = {'visiteur':isguest,
               'user_email':user_email,
               'user_first_name':user_first_name
               }
    
    return render(request, 'HTML/home.html', context)

def index_view(request):
    context = {}  # You can pass context data to the template if needed
    return render(request,'HTML/index/index.html',context)

def admin_panel(request):
    context = {}  # You can pass context data to the template if needed
    return render(request,'HTML/admin_panel/admin_panel.html', context)

def group_view(request):
    context = {}  # You can pass context data to the template if needed
    return render(request,'HTML/groupe_page.html', context)

def login_view(request):
    context = {}  # You can pass context data to the template if needed
    return render(request,'HTML/login.html', context)
def profile(request):
    context = {}  # You can pass context data to the template if needed
    return render(request,'HTML/userProfile/profile.html', context)

def welcome_view(request):
    context = {}  # You can pass context data to the template if needed
    return render(request,'HTML/welcome/welcome.html',context)
def homeClass_view(request):
    context = {}  # You can pass context data to the template if needed
    return render(request,'HTML/classroom/home.html',context)


def chat_app_view(request):
    return render(request, 'HTML/userProfile/chatApp.html')
