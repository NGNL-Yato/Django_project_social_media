from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms
from .models import utilisateur ,Etudiant,Professor , Skills , Languages ,Enterprise ,Experience, Event , Certification, Education ,Research, Group, ClassRoom,PostClassroom
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
        exclude = ['user','role']  
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
        exclude = ['utilisateur','group']
        fields = '__all__'
        widgets={
            'event_time':forms.DateInput(format="%Y-%m-%d", attrs={"type": "date",'style':'height:60px;'}),
            'head_title':forms.TextInput(attrs={'placeholder':'Event Title','style':'height:60px;'}),
            'description':forms.Textarea(attrs={'placeholder':'Event Description','style':'width:100%;','class':'your-css-class'}),
            'backgroundimage':forms.FileInput(attrs={'class':'your-css-class','style':'display:none;'}),
            'file':forms.FileInput(attrs={'class':'id_file2','style':'display:none;'}),

            }

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['contenue', 'file']

TARGET_CHOICES = [
    ('public', 'Public'),
    ('private', 'Private'),
]

class GroupForm(forms.ModelForm):
    description = forms.CharField(required=False)
    target = forms.ChoiceField(choices=TARGET_CHOICES, widget=forms.Select(attrs={'class': 'your-css-class'}))
    class Meta:
        model = Group
        fields = ['group_name', 'description', 'target', 'profile_banner']


class ClassRoomForm(forms.ModelForm):
     class Meta:
        model = ClassRoom
        exclude = ['Admin_Professor','UniqueinvitationCode']
        fields = '__all__'
        widgets ={
            'description':forms.Textarea(attrs={'style':'max-width: 100%;width: 100%;padding: 10px;background-color: #eeeeee;'}),
            'ClassRoomtitle': forms.TextInput(attrs={'style':'max-width: 100%;width: 100%;padding: 10px;background-color: #eeeeee;'}),
            'ClassRoomimage':forms.FileInput(attrs={'style':'display:none;'}),
        }

class PostClassroomForm(forms.ModelForm):
    class Meta:
        model = PostClassroom
        exclude=['author','classroom']
        fields = '__all__'
        widgets={
            'contentPost':forms.TextInput(attrs={'style':"background: transparent;height: 95%;margin-left: 25px;width: 95%;","placeholder":'Post Contenue'}),
             'filePost':forms.FileInput(attrs={'style':'display:none'}),
        }
