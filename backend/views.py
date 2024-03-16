from django.shortcuts import render , redirect
from backend import models
from django.contrib.auth import authenticate, login , logout
from django.contrib.auth.models import auth
from .forms import CreationdUser
from django.contrib import messages


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
            return redirect('home')
    # if not above , creat signup form is user want to signup 
    Signupform = CreationdUser()
    context = {'signUpform':Signupform} 
    return render(request,'HTML/login.html', context)

def signup(request):
    if request.method == 'POST':
        Sform = CreationdUser(request.POST)
        if Sform.is_valid():
            Sform.save()
            return redirect('home')
        else:
            return redirect('login')

    return redirect('login')


def login_out(request):
        logout(request)  # Logout the user
        return redirect('login')
