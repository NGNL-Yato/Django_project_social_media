from django.shortcuts import render , redirect
from backend import models
from django.contrib.auth import authenticate, login , logout
from django.contrib.auth.models import auth
from .forms import CreationdUser , UtilisateurForm
from django.contrib import messages
from django.shortcuts import get_object_or_404
from .Post import delete_post
# unfollow_user
def unfollow_user(request, first_name, last_name):
    #
    user_to_unfollow = models.User.objects.filter(first_name=first_name, last_name=last_name).first()
    
    if user_to_unfollow is None:
        return redirect('home')  

    user_to_unfollow = user_to_unfollow.utilisateur    
    current_user = request.user.utilisateur
    
    # Check if the authenticated user is trying to unfollow themselves
    if current_user == user_to_unfollow:
        return redirect('home')  

    
    # Check if the follow relationship exists
    follow_instance = models.follow.objects.filter(follower=current_user, followed=user_to_unfollow).first()
    
    if follow_instance is None:
        return redirect('home')  
    
    follow_instance.delete()

    return redirect('profile', first_name=first_name, last_name=last_name)

# follow 
def follow_user(request, first_name, last_name):

    user_to_follow = models.User.objects.filter(first_name=first_name, last_name=last_name).first()

    if user_to_follow is None:
        return redirect('home')  

    user_to_follow = user_to_follow.utilisateur
    current_user = request.user.utilisateur

    # to Check if the authenticated user is trying to follow themselves or they already following them
    if current_user == user_to_follow or models.follow.objects.filter(follower=current_user, followed=user_to_follow).exists():
        return redirect('home')  
    
    models.follow.objects.create(follower=current_user, followed=user_to_follow)
    
    return redirect('profile', first_name=first_name, last_name=last_name)
    

# Create your views here.
def login_in(request):

    # dont show login page if already logged
    if request.user.is_authenticated:
        return redirect('home')
    
    # check for login detail if its a post request
    if request.method == 'POST':
        Username = request.POST.get('Username')
        Login_password = request.POST.get('Password')
        user = authenticate(request,username=Username,password=Login_password)
        # if user details matches details in DB , log him in 
        if user is not None:
            login(request,user)
            if not user.is_superuser :
                u = models.utilisateur.objects.get(user_id = request.user.id)
                u.online_status = True
                u.save()
            return redirect('home')
    # if not above , creat signup form is user want to signup 
    if request.session.get('invalid_signup') == "True":
        Signupform = CreationdUser()
        context = {'signUpform':Signupform,
                'invalid_signup_session': True
               } 
    else :
        Signupform = CreationdUser()
        context = {'signUpform':Signupform,
                'invalid_signup_session': False
               } 
    
    return render(request,'HTML/home/login.html', context)

def signup(request):

    if request.method == 'POST':
        Sform = CreationdUser(request.POST)
        if Sform.is_valid():
            usr = Sform.save()
            models.utilisateur.objects.create( user=usr )
            # then log him here 
            Username = request.POST.get('username')
            Login_password = request.POST.get('password1')
            user = authenticate(request,username=Username,password=Login_password)
            # if user details matches details in DB , log him in 
            if user is not None:
                login(request,user)
                u = models.utilisateur.objects.get(user_id = request.user.id)
                u.online_status = True
                u.save()
                #
                return redirect('home')
            #
        else:
            request.session['invalid_signup'] = "True"
            return redirect('login')

    return redirect('login')


def login_out(request):
        if request.user.is_superuser :
            logout(request)  # Logout the user
            return redirect('login')
        else:
            user = models.utilisateur.objects.get(user_id = request.user.id)
            user.online_status = False
            user.save()
            logout(request)  # Logout the user
            return redirect('login')

def test(request):
    if request.method == 'POST':
        userinstance = models.utilisateur.objects.get(user_id=request.user.id)
        form = UtilisateurForm(request.POST,request.FILES, instance=userinstance)
        if form.is_valid(): ###
            form.save()
            # print(userinstance.role)
            return redirect('home')

    elif request.user.is_authenticated:
        userinstance = models.utilisateur.objects.get(user_id=request.user.id)
        # userinstance = get_object_or_404(models.user, user=request.user)
        userform = UtilisateurForm(instance=userinstance)
        context = {'userform': userform}
        return render(request, 'HTML/tmp/test.html', context)
    
    return redirect('home')


def profile_settings(request):
    return render(request, 'HTML/userProfile/settings.html')
