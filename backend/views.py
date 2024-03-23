from django.shortcuts import render , redirect
from backend import models
from django.contrib.auth import authenticate, login , logout
from django.contrib.auth.models import auth
from .forms import CreationdUser , UtilisateurForm , EntrepriseForm , EtudiantForm , ProfesseurForm , SkillForm, languagesForm ,CertificationForm , EducationForm , ExperienceForm
from django.contrib import messages
from django.shortcuts import get_object_or_404
from .Post import delete_post
from .Like import like_post



# remove follower , i no longer want this person to be following me.
def remove_follower(request, first_name, last_name):
    # Find the follower user
    follower_user = models.User.objects.get(first_name=first_name, last_name=last_name)
    follower_user = follower_user.utilisateur
    # Find the follow relationship between the current user and the follower
    follow_relationship = models.follow.objects.filter(followed=request.user.utilisateur, follower=follower_user).first()
    
    # Check if the follow relationship exists
    if follow_relationship:
        # Delete the follow relationship
        follow_relationship.delete()
    
    # Redirect to the profile page of the follower
    return redirect('myfollowers')


# unfollow_user
def unfollow_user(request, first_name, last_name):
    if not request.user.is_authenticated:
        return redirect('home')
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

    return redirect('myfollowings')

# follow 
def follow_user(request, first_name, last_name):

    if not request.user.is_authenticated:
        return redirect('home')
 
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
    

# login
def login_in(request):

    # dont show login page if already logged
    if request.user.is_authenticated:
        return redirect('home')
    
    # check for login detail if its a post request
    if request.method == 'POST':
        # Username = request.POST.get('Username')
        email = request.POST.get('email')
        Login_password = request.POST.get('Password')

        try:
            Usr = models.User.objects.get(email=email) 
        except models.User.DoesNotExist:
            return redirect('login')

        user = authenticate(request,username=Usr.username ,password=Login_password)
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

#
#
def signup(request):

    if request.method == 'POST':
        
        emailusedtosignup = request.POST.get('email')

        emailusedtosignups = emailusedtosignup.split('@')[1]

        Entreprisechoice = request.POST.get('choice-radio')

        if Entreprisechoice == 'Oui':
            Sform = CreationdUser(request.POST)

            if Sform.is_valid():
                usr = Sform.save()
                utilisateuur = models.utilisateur.objects.create( user=usr )
                utilisateuur.role = 3 ###
                utilisateuur.save()
                # creat instance of the entreprise
                models.Enterprise.objects.create(utilisateur=utilisateuur)

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

        elif Entreprisechoice == 'Non':

            if emailusedtosignups != 'uae.ac.ma' and emailusedtosignups != 'etu.uae.ac.ma':
                return redirect('login')
            
            Sform = CreationdUser(request.POST)

            if Sform.is_valid():
                usr = Sform.save()
                utilisateuur = models.utilisateur.objects.create( user=usr )

                if emailusedtosignups == 'uae.ac.ma':
                    utilisateuur.role = 1
                    utilisateuur.save()
                    models.Professor.objects.create( utilisateur=utilisateuur )

                elif emailusedtosignups == 'etu.uae.ac.ma':
                    utilisateuur.role = 2
                    utilisateuur.save()
                    models.Etudiant.objects.create( utilisateur=utilisateuur )
                        
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
        userform = CreationdUser(instance=userinstance.user)
        utilisateurform = UtilisateurForm(instance=userinstance)
        context = {
                   'utilisateurform': utilisateurform,
                   'userform':userform
                   }
        return render(request, 'HTML/tmp/test.html', context)
    
    return redirect('home')

# deleteEducation
def deleteEducation(request, id):
    c = models.Education.objects.filter(id=id).first()
    if c is not None:
        c.delete()
        return redirect('settings')

    return redirect('settings')

# deleteExperiences
def deleteExperiences(request, id):
    c = models.Experience.objects.filter(id=id).first()
    if c is not None:
        c.delete()
        return redirect('settings')

    return redirect('settings')



# deletecertificates
def deletecertificates(request, id):
    c = models.Certification.objects.filter(id=id).first()
    if c is not None:
        c.delete()
        return redirect('settings')

    return redirect('settings')

# removeSkill
def removeSkill(request, id):
    skill = models.Skills.objects.filter(id=id).first()
    if skill is not None:
        skill.delete()
        return redirect('settings')

    return redirect('settings')


# remove languague
def removeLanguage(request,id):
    L = models.Languages.objects.filter(id=id).first()
    if L is not None:
        L.delete()
        return redirect('settings')
    return redirect('settings')

# settings
def profile_settings(request):

    if request.method == 'POST':
        userinstance = models.utilisateur.objects.get(user_id=request.user.id)
        form = UtilisateurForm(request.POST,request.FILES, instance=userinstance)
        skillform = SkillForm(request.POST)
        languagesform = languagesForm(request.POST)

        if form.is_valid():
            form.save()

        if languagesform.is_valid() and request.POST.get('Language', '').strip() != '' :
            lang = languagesform.cleaned_data['Language']
            models.Languages.objects.create(utilisateur=userinstance,Language=lang)
            
        if skillform.is_valid() and request.POST.get('SkillName', '').strip() != '' :
            skill = skillform.cleaned_data['SkillName']  # Accessing cleaned data
            models.Skills.objects.create(utilisateur=userinstance, SkillName=skill)
   

        if userinstance.role == 1:
            userinstance = models.Professor.objects.get(utilisateur=userinstance)
            epeForm = ProfesseurForm(request.POST,request.FILES,instance=userinstance) 
        elif userinstance.role == 2:
            userinstance = models.Etudiant.objects.get(utilisateur=userinstance)
            epeForm = EtudiantForm(request.POST,request.FILES,instance=userinstance) 
        elif userinstance.role == 3 :
            userinstance = models.Enterprise.objects.get(utilisateur=userinstance)
            epeForm = EntrepriseForm(request.POST,request.FILES,instance=userinstance) 

        if epeForm.is_valid():
            epeForm.save()

   

        return redirect('settings')
        

    elif request.user.is_authenticated:
        userinstance = models.utilisateur.objects.get(user_id=request.user.id)
        utilisateurform = UtilisateurForm(instance=userinstance)
       
        if userinstance.role == 1:
            userinstance = models.Professor.objects.get(utilisateur=userinstance)
            epeForm = ProfesseurForm(instance=userinstance) 
        elif userinstance.role == 2:
            userinstance = models.Etudiant.objects.get(utilisateur=userinstance)
            epeForm = EtudiantForm(instance=userinstance) 
        elif userinstance.role == 3 :
            userinstance = models.Enterprise.objects.get(utilisateur=userinstance)
            epeForm = EntrepriseForm(instance=userinstance) 

        context = {
                   'utilisateurform': utilisateurform,
                   'userdata':request.user,
                   'utilisateurdata':request.user.utilisateur,
                   'skillform' : SkillForm(instance=userinstance),
                   'skills':models.Skills.objects.filter(utilisateur=request.user.utilisateur),
                   'languageForm':languagesForm(instance=userinstance),
                   'languages':models.Languages.objects.filter(utilisateur=request.user.utilisateur),
                   'settings_page':True,
                   'epeForm':epeForm,
                   }
        
        return render(request, 'HTML/userProfile/settings.html', context)
    
    return redirect('home')



# certificates Settings
def certificatesSettings(request):
    
    if request.method == 'POST':
        # c = models.Certification.objects.create()
        userinstance = models.utilisateur.objects.get(user_id=request.user.id)
        c = CertificationForm(request.POST, request.FILES)
        if c.is_valid():
            certification_instance = c.save(commit=False)  # Create Certification instance from form data without saving to the database
            certification_instance.utilisateur = userinstance  # Associate the utilisateur instance with the Certification instance
            certification_instance.save()   
                    

    if request.user.is_authenticated:
        userinstance = models.utilisateur.objects.get(user_id=request.user.id)
    
    context = {
        'Certificationssettings':True,
        "Certificationsforum":CertificationForm(),
        'certificates':models.Certification.objects.filter(utilisateur=userinstance)
    }

    return render(request, 'HTML/userProfile/settings.html', context)


# ExperiencesSettings
def ExperiencesSettings(request):


    if request.method == 'POST':
        # c = models.Certification.objects.create()
        userinstance = models.utilisateur.objects.get(user_id=request.user.id)
        c = ExperienceForm(request.POST, request.FILES)
        if c.is_valid():
            certification_instance = c.save(commit=False)  # Create Certification instance from form data without saving to the database
            certification_instance.utilisateur = userinstance  # Associate the utilisateur instance with the Certification instance
            certification_instance.save()   
                    

    if request.user.is_authenticated:
        userinstance = models.utilisateur.objects.get(user_id=request.user.id)
    

    context = {
        'ExperiencesSettings':True,
        "Experiencesform":ExperienceForm(),
        'allmyExperiences':models.Experience.objects.filter(utilisateur=userinstance)
    }

    return render(request, 'HTML/userProfile/settings.html', context)



# educationsSettings
def educationsSettings(request):
    if request.method == 'POST':
        userinstance = models.utilisateur.objects.get(user_id=request.user.id)
        edu = EducationForm(request.POST, request.FILES)
        if edu.is_valid():
            eduins = edu.save(commit=False)  # Create Certification instance from form data without saving to the database
            eduins.utilisateur = userinstance  # Associate the utilisateur instance with the Certification instance
            eduins.save()   
           
    if request.user.is_authenticated:
        userinstance = models.utilisateur.objects.get(user_id=request.user.id)

    context ={
        'educationssetings':True,
        'educations':models.Education.objects.all(),
        'Educationform':EducationForm(),
    }
    return render(request, 'HTML/userProfile/settings.html', context)

# my followers
def myfollowers(request):
    if request.user.is_authenticated:
            userinstance = models.utilisateur.objects.get(user_id=request.user.id)
            # userinstance = get_object_or_404(models.user, user=request.user)
            # userform = CreationdUser(instance=userinstance.user)
            utilisateurform = UtilisateurForm(instance=userinstance)
            context = {
                    'utilisateurform': utilisateurform,
                    'userdata':request.user,
                    'utilisateurdata':request.user.utilisateur,
                    'myfollowers':True,
                    'all_myfollowers':request.user.utilisateur.followers.all(),
                    }
            return render(request, 'HTML/userProfile/settings.html', context)
        
    return redirect('home')    

def myfollowings(request):

    if request.user.is_authenticated:
        userinstance = models.utilisateur.objects.get(user_id=request.user.id)
        # userinstance = get_object_or_404(models.user, user=request.user)
        # userform = CreationdUser(instance=userinstance.user)
        utilisateurform = UtilisateurForm(instance=userinstance)
        context = {
                   'utilisateurform': utilisateurform,
                   'userdata':request.user,
                   'utilisateurdata':request.user.utilisateur,
                   'myfollowings':True,
                   'all_myfollowings':request.user.utilisateur.following.all(),
                   }
        return render(request, 'HTML/userProfile/settings.html', context)
    
    return redirect('home')


