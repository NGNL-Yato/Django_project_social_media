from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms
from .models import utilisateur ,Etudiant,Professor, Research , Skills , Languages ,Enterprise ,Experience, Event , Certification, Education
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


class EtudiantForm(ModelForm):
    class Meta:
        model = Etudiant
        exclude = ['utilisateur']
        fields = '__all__'
        widgets={
            'date_inscription':forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
        }

class ProfesseurForm(ModelForm):
    class Meta:
        model = Professor
        exclude = ['utilisateur']
        fields = '__all__'
        widgets={
            'date_integration':forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
            'poste_administratif':forms.TextInput(attrs={'placeholder':'Exemple : Professeur Chercheur a l\'universite abdelmalek essadi'}),
        }


class ResearchForm(ModelForm):
    class Meta:
        model = Research
        exclude = ['utilisateur']
        fields = '__all__'
        


class SkillForm(ModelForm):
    class Meta:
        model = Skills
        exclude = ['utilisateur']
        fields = '__all__'
        labels = {
            'SkillName': 'Add New Skill', 
        }
        widgets = {
            'SkillName':forms.TextInput(attrs={'placeholder':'Vos Skills'}),
        }


class languagesForm(ModelForm):
    class Meta:
        model = Languages
        exclude = ['utilisateur']
        fields = '__all__'
        labels = {
            'Language': 'Add New Language', 
        }   
        widgets = {
            'Language':forms.TextInput(attrs={'placeholder':'Language que vous metrisez'}),
        }


class EntrepriseForm(ModelForm):
    class Meta:
        model = Enterprise
        exclude = ['utilisateur']
        fields = '__all__'


class CertificationForm(ModelForm):
    class Meta:
        model = Certification
        exclude = ['utilisateur']
        fields = '__all__'
        widgets={
            'date_obtention':forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
         }

class EducationForm(ModelForm):
    class Meta:
        model = Education
        exclude = ['utilisateur']
        fields = '__all__'
        widgets={
            'date_fin':forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
            'date_debut':forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
            }
        labels= {
            'UniversityName':'University Name',
            'FiledOfStudy':'Filed Of Study',

         }

class ExperienceForm(ModelForm):
    class Meta:
        model = Experience
        exclude = ['utilisateur']
        fields = '__all__'
        widgets={
            'date_fin':forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
            'date_debut':forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
            }

class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = '__all__'


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['contenue', 'file']