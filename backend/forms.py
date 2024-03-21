from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms
from .models import utilisateur
from .models import Post

class CreationdUser(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('password2')  # Remove the password2 field

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
        exclude = ['user','role']  # Exclude the 'user' field from the form
        fields = '__all__'

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['contenue', 'file']