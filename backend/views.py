from django.shortcuts import render , redirect
from backend import models
from django.contrib.auth import login , logout


# Create your views here.
def login_in(request):
    if request.method == 'POST':
        # login(request)
        pass
    context = {} 
    return render(request,'HTML/login.html', context)

def signup(request):
    if request.method == 'POST':
        models.User.save
    context = {} 
    return render(request,'HTML/login.html', context)


def login_out(request):
        logout(request)  # Logout the user
        return redirect('login')
