from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms
from .models import utilisateur

class CreationdUser(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','first_name','last_name']

        widgets = {
            'username':forms.TextInput(attrs={'placeholder':'Username'}),
            'email':forms.EmailInput(attrs={'placeholder':'Email'}),
            'first_name':forms.TextInput(attrs={'placeholder':'First Name'}),
            'last_name':forms.TextInput(attrs={'placeholder':'Last Name'}),
        }

class UtilisateurForm(ModelForm):
    class Meta:
        model = utilisateur
        fields = '__all__'