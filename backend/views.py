from django.shortcuts import render , redirect
from backend import models
from django.contrib.auth import authenticate, login , logout
from django.contrib.auth.models import auth
from .forms import CreationdUser , UtilisateurForm , EntrepriseForm , EtudiantForm , ProfesseurForm , SkillForm, languagesForm ,CertificationForm ,ResearchForm, EducationForm , ExperienceForm, GroupForm
from django.contrib import messages
from django.shortcuts import get_object_or_404
from .Post import delete_post
from .Like import like_post
from django.http import JsonResponse
from django.core import serializers
from .models import User, UserGroup, Group, follow, Conversation, Participant, Message, MessageFile,Post
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from django.urls import reverse



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

#
#
def unfollow_user_profile(request, first_name, last_name):
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

    return redirect('hisprofile',first_name=first_name, last_name=last_name)

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
    
    return redirect('hisprofile', first_name=first_name, last_name=last_name)

def deleteResearches(request,id):
    # deleteResearches

    Researche = models.Research.objects.filter(id=id).first()
    if Researche is not None:
        Researche.delete()
        return redirect('settings')

    return redirect('settings')

#    
def Researches(request):
    r = []
    userinstance = models.utilisateur.objects.get(user_id=request.user.id)

    if request.method == 'POST':
        f = ResearchForm(request.POST,request.FILES)
        if f.is_valid():
            x = f.save(commit=False)
            x.utilisateur = userinstance
            x.save()

    if request.user.is_authenticated:
        userinstance = models.utilisateur.objects.get(user_id=request.user.id)
        r = models.Research.objects.filter(utilisateur=userinstance)

    context = {
        'ResearchesSetttings':True,
        'Researchesform':ResearchForm(),
        'Researches':r
    }

    return render(request, 'HTML/userProfile/settings.html', context)


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
    epeForm = None
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

#my groups 
def groupsSettings(request):
    if request.user.is_authenticated:
        groups = Group.objects.filter(user=request.user)    
        context ={'groups':groups}
    return render(request, 'HTML/userProfile/settings.html', context)

#delete groups
def deleteGroup(request, id):
    if request.user.is_authenticated:
        group = Group.objects.filter(id=id).first()
        if group:
            print("deleting ...")
            UserGroup.objects.filter(group=group).delete()
            Participant.objects.filter(group_id=group).delete()
            group.delete()
    return redirect('settings')

#mes posts
def postsSettings(request):
    if request.user.is_authenticated:
        posts = Post.objects.filter(user=request.user)  
        context ={'posts':posts}
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

def create_group(request):
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            group = form.save(commit=False)
            group.user = request.user
            group.save()
            return redirect('some-view')
    else:
        form = GroupForm()

    return render(request, 'group_creation.html', {'form': form})

# def settings_posts (request):
#     if request.method == 'POST':
#         userinstance = models.utilisateur.objects.get(user_id=request.user.id)
#         form = UtilisateurForm(request.POST,request.FILES, instance=userinstance)
#         if form.is_valid():
#             form.save()
#             return redirect('home')
#     elif request.user.is_authenticated:
#         userinstance = models.utilisateur.objects.get(user_id=request.user.id)
#         # userinstance = get_object_or_404(models.user, user=request.user)
#         userform = CreationdUser(instance=userinstance.user)
#         utilisateurform = UtilisateurForm(instance=userinstance)
#         context = {
#                    'utilisateurform': utilisateurform,
#                    'userform':userform
#                    }
#         return render(request, 'HTML/userProfile/mes-posts.html', context)
    
#     return redirect('home')


def search_people(request):
    query = request.GET.get('query')
    people = User.objects.filter(Q(first_name__icontains=query) | Q(last_name__icontains=query))
    person = UserGroup.objects.filter(Q(user__first_name__icontains=query) | Q(user__last_name__icontains=query))
    data = [{'first_name': person.first_name, 'last_name': person.last_name, 'username': person.username} for person in people]
    return JsonResponse(data, safe=False)

@csrf_exempt
def invite_user(request):
    username = request.POST.get('username')
    group_name = request.POST.get('group_name')

    # Print the username and group_name
    print(f"Username: {username}, Group Name: {group_name}")

    try:
        user = get_user_model().objects.get(username=username)
        group = Group.objects.get(group_name=group_name)  # Use group_name instead of name
        UserGroup.objects.create(user=user, group=group, is_admin=False, invitation_on=False)
        return JsonResponse({'message': 'Invitation sent.'})
    except ObjectDoesNotExist:
        return JsonResponse({'message': 'User or group does not exist.'}, status=400)
    
@login_required
def get_pending_invitations(request):
    pending_invitations = UserGroup.objects.filter(user=request.user, invitation_on=False)
    data = [{'group_name': invitation.group.group_name} for invitation in pending_invitations]
    return JsonResponse(data, safe=False)

@require_POST
@login_required
def accept_invitation(request):
    group_name = request.POST.get('group_name')
    print(f"Accepted invitation for group: {group_name}")
    user_group = UserGroup.objects.filter(user=request.user, group__group_name=group_name).first()
    if user_group:
        user_group.invitation_on = True
        user_group.save()
        conversation = Conversation.objects.filter(title=group_name).first()
        if conversation:
            Participant.objects.create(user=request.user, conversation=conversation, group_id=user_group.group)
        return JsonResponse({'message': 'Invitation accepted.'})
    else:
        return JsonResponse({'message': 'Group not found.'})

@require_POST
@login_required
def reject_invitation(request):
    group_name = request.POST.get('group_name')
    print(f"Rejected invitation for group: {group_name}")
    user_group = UserGroup.objects.filter(user=request.user, group__group_name=group_name).first()
    if user_group:
        conversation = Conversation.objects.filter(title=group_name).first()
        if conversation:
            Participant.objects.filter(user=request.user, conversation=conversation, group_id=user_group.group).delete()
        user_group.delete()
        return JsonResponse({'message': 'Invitation rejected.'})
    else:
        return JsonResponse({'message': 'Group not found.'})

@require_POST
@login_required
def join_group(request):
    group_name = request.POST.get('group_name')
    group = Group.objects.get(group_name=group_name)
    UserGroup.objects.create(user=request.user, group=group, invitation_on=True)
    conversation = Conversation.objects.filter(title=group_name).first()
    if conversation:
        Participant.objects.create(user=request.user, conversation=conversation, group_id=group)
    return JsonResponse({'message': 'Group joined.'})

@require_POST
@login_required
def leave_group(request):
    group_name = request.POST.get('group_name')
    user_group = UserGroup.objects.filter(user=request.user, group__group_name=group_name).first()
    if user_group:
        conversation = Conversation.objects.filter(title=group_name).first()
        if conversation:
            Participant.objects.filter(user=request.user, conversation=conversation, group_id=user_group.group).delete()
        user_group.delete()
        return JsonResponse({'message': 'Group left.'})
    else:
        return JsonResponse({'message': 'Group not found.'})

@login_required   
def group_settings(request, group_name):
    group = Group.objects.filter(group_name=group_name).first()
    admins = UserGroup.objects.filter(group=group, is_admin=True)
    All_admins_id =[]
    for admin in admins :
        All_admins_id.append(admin.user.id)
    search = request.GET.get('search', '')
    users_list = group.usergroup_set.exclude(user=group.user).filter(Q(user__first_name__icontains=search) | Q(user__last_name__icontains=search), invitation_on=True)
    paginator = Paginator(users_list, 7)
    page_number = request.GET.get('page')
    users = paginator.get_page(page_number)
    invitation_search = request.GET.get('invitation_search', '')
    invitation_users_list = group.usergroup_set.filter(Q(user__first_name__icontains=invitation_search) | Q(user__last_name__icontains=invitation_search), invitation_on=False)
    invitation_users = Paginator(invitation_users_list, 7).get_page(request.GET.get('invitation_page'))
    if (request.user.id not in All_admins_id) and (request.user != group.user):
        return redirect('group_posts', group_name=group_name)
    if request.method == 'POST':
        group_name = request.POST.get('group_name')
        description = request.POST.get('description')
        target = request.POST.get('target')
        profile_banner = request.FILES.get('profile_banner')
        if group_name:
            group.group_name = group_name
        if description:
            group.description = description
        if target:
            group.target = target
        if profile_banner:
            group.profile_banner = profile_banner
        group.save()
    return render(request, 'HTML/home/group_settings.html', {'group': group, 'users': users, 'invitation_users': invitation_users})

@require_POST
@login_required
def toggle_admin(request):
    user_id = request.POST.get('user_id')
    group_name = request.POST.get('group_name')
    user_group = UserGroup.objects.get(user__id=user_id, group__group_name=group_name)
    user_group.is_admin = not user_group.is_admin
    user_group.save()
    if user_group.is_admin:
        return JsonResponse({'message': 'User made admin.'})
    else:
        return JsonResponse({'message': 'Admin removed.'})

@require_POST
@login_required
def kick_user(request):
    user_id = request.POST.get('user_id')
    group_name = request.POST.get('group_name')
    rows_deleted = UserGroup.objects.filter(user__id=user_id, group__group_name=group_name).delete()
    if rows_deleted[0] > 0:
        return JsonResponse({'message': 'User kicked.'})
    else:
        return JsonResponse({'message': 'Failed to kick user.'})

@csrf_exempt
def cancel_invitation(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        user_group = UserGroup.objects.get(user__id=user_id)
        user_group.invitation_on = True  # Or whatever you do to cancel the invitation
        user_group.save()
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False})

@login_required
def get_friends(request):
    user = request.user
    utilisateur = user.utilisateur
    friends = set()
    Conversations = Conversation.objects.filter(participant__user=user)
    group_conversations = [conversation for conversation in Conversations if conversation.is_group_conversation()]
    friend_conversations = [conversation for conversation in Conversations if conversation.is_friend_conversation()]
    group_conversations_info = [{'title': conversation.title,'picture':conversation.Conversation_picture.url if conversation.Conversation_picture else None} for conversation in group_conversations]
    friend_conversations_info = [{'title': conversation.title,'picture':conversation.Conversation_picture.url if conversation.Conversation_picture else None} for conversation in friend_conversations]
    for f in utilisateur.following.all():
        if f.followed.followers.filter(follower=utilisateur).exists():
            friends.add(f.followed)
    friends = {friend for friend in friends if friend.following.filter(followed=utilisateur).exists()}
    friends_info = [{'first_name': friend.user.first_name,'username':friend.user.username ,'last_name': friend.user.last_name, 'profile_picture': friend.profile_picture.url if friend.profile_picture else None} for friend in friends]    
    data = {
        'friends': friends_info,
        'group_conversations': group_conversations_info,
        'friend_conversations': friend_conversations_info,
        'user_picture': utilisateur.profile_picture.url,
    }
    print(data)
    return JsonResponse(data, safe=False)

@csrf_exempt
def get_or_create_conversation(request):
    print(request.POST)
    if request.method == 'POST':
        identifier = request.POST.get('username')
        user = request.user
        friend = None  # Define friend here
        try:
            group = Group.objects.get(group_name=identifier)
            print(group)
            participant = Participant.objects.filter(user=user, group_id=group).first()
            print(participant)
            conversation = participant.conversation
            print(conversation)
        except Group.DoesNotExist:
            # If identifier is not a group name, handle it as a friend's username
            try:
                friend = get_user_model().objects.get(username=identifier)
                conversation = Conversation.objects.filter(participant__user=user).filter(participant__user=friend).first()
                if not conversation:
                    conversation = Conversation.objects.create()
                    Participant.objects.create(user=user, conversation=conversation)
                    Participant.objects.create(user=friend, conversation=conversation)
            except get_user_model().DoesNotExist:
                return JsonResponse({'error': 'User not found'}, status=404)

        messages = Message.objects.filter(conversation=conversation).order_by('timestamp')
        messages_data = []
        for message in messages:
            is_user_sender = message.sender.username == request.user.username
            file_urls = [message_file.file.url for message_file in message.files.all()]
            messages_data.append({
                'sender': message.sender.username,
                'sender_picture': message.sender.utilisateur.profile_picture.url,  # Add this line
                'content': message.content,
                'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                'is_user_sender': is_user_sender,
                'file_url': file_urls
            })
        user_picture = user.utilisateur.profile_picture.url
        friend_picture = friend.utilisateur.profile_picture.url if friend else None
        print(conversation.id)
        print(messages_data)
        return JsonResponse({'conversation': conversation.id, 'messages': messages_data,'user_picture':user_picture,'friend_picture':friend_picture})
    
@csrf_exempt
def send_message(request):
    if request.method == 'POST':
        message_content = request.POST.get('message')
        conversation_id = request.POST.get('conversation')
        file = request.FILES.get('file')
        user = request.user
        conversation = Conversation.objects.get(id=conversation_id)
        message = Message.objects.create(sender=user, conversation=conversation, content=message_content)
        if file:
            MessageFile.objects.create(message=message, file=file)
        return JsonResponse({'message': 'Message sent successfully'})


def search(request):
    search_text = request.GET.get('search_text', '')
    users = get_user_model().objects.filter(Q(first_name__icontains=search_text) | Q(last_name__icontains=search_text),is_superuser=False)
    groups = Group.objects.filter(Q(group_name__icontains=search_text) & Q(target='public'))
    user_results = list(users.values('username', 'first_name', 'last_name'))
    for user in user_results:
        user['type'] = 'user'
        user['url'] = reverse('hisprofile', kwargs={'first_name': user['first_name'], 'last_name': user['last_name']})
        if(len(user['first_name']) > 5):
            break
    group_results = list(groups.values('group_name'))
    for group in group_results:
        group['type'] = 'group'
        group['url'] = reverse('group_posts', kwargs={'group_name': group['group_name']})
        if(len(group['group_name']) > 5):
            break
    results = user_results + group_results
    print (results)
    
    return JsonResponse(results, safe=False)