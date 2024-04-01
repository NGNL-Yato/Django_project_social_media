from django.shortcuts import render , redirect
from backend.models import User,utilisateur,Post, Group, UserGroup,ClassRoom, Event, Skills, Languages, Certification, Education, Experience, Research, UserGroup, Group, UserGroup, ClassRoom, Task, Etudiant,TaskResponse, PostClassroom
from backend.forms import PostForm, GroupForm, EventForm , ClassRoomForm,PostClassroomForm,TaskForm , QcmForm ,QuestionForm, AnswerForm,TaskResponseForm
from django.core.mail import send_mail
from django.conf import settings
from backend import models
from django.db.models import QuerySet
from django.http import JsonResponse
from django.urls import reverse
from django.db.models import Count
from random import choice
from django.db.models import Q

import random
import string

def home_view(request):
    all_users_names = []
    post_form = None
    group_form = None
    posts_visitor = Post.objects.all()
    posts = []
    latest_event = Event.objects.order_by('-created_at').first()
    random_group = choice(Group.objects.annotate(member_count=Count('user')).order_by('-member_count'))

    if request.user.is_authenticated:
        all_my_followings = request.user.utilisateur.following.all()
        following_users = [f.followed.user for f in all_my_followings]
        following_posts = Post.objects.filter(user__in=following_users)
        user_groups = UserGroup.objects.filter(user=request.user).values_list('group', flat=True)
        group_posts = Post.objects.filter(group__in=user_groups)
        user_posts = Post.objects.filter(user=request.user)
        posts = following_posts.union(group_posts, user_posts).order_by('-created_at')
        groups = Group.objects.filter(usergroup__user=request.user)
    else:
        groups = None
        group_posts = Post.objects.filter(group__target='public')
        user_posts = Post.objects.filter(group=None)
        posts = group_posts.union(user_posts).order_by('-created_at')
    if request.user.is_authenticated and request.user.is_superuser :
        return redirect('admin_panel')

    #
    if request.user.is_authenticated:
        if request.method == 'POST':
            post_form = PostForm(request.POST, request.FILES)
            group_form = GroupForm(request.POST, request.FILES)
            if post_form.is_valid():
                post = post_form.save(commit=False)
                post.user = request.user
                post.save()
                return redirect('home')
            elif group_form.is_valid():
                group = group_form.save(commit=False)
                group.user = request.user
                try:
                    group.save()
                    return JsonResponse({'status': 'redirect', 'location': reverse('group_posts', kwargs={'group_name': group.group_name})})                
                except ValueError:
                    return JsonResponse({'status': 'error', 'message': 'A group with this name already exists.'})
            else:
                print("Error found!")
                for field, errors in group_form.errors.items():
                    for error in errors:
                        print(f"{field}: {error}")        
        else:
            post_form = PostForm()
            group_form = GroupForm()

        isguest = False
        user = request.user
        user_email = user.email        
        user_first_name = user.first_name
        user_pdp = user.utilisateur.profile_picture

        friends = set()
        for f in user.utilisateur.following.all():
            if f.followed.followers.filter(follower=user.utilisateur).exists():
                friends.add(f.followed)
        friends = {friend for friend in friends if friend.following.filter(followed=user.utilisateur).exists()}

        for friend in friends:
            if len(all_users_names) >= 6:
                break
            full_name = f"{friend.user.first_name} {friend.user.last_name}"
            online = friend.online_status
            pdp = friend.profile_picture

            obj = {
                'full_name': full_name,
                "online": 'online' if online else 'offline',
                'profile_picture': pdp
            }
            all_users_names.append(obj)

    else:
        isguest = True
        user_email = "Guest@g.uae.ac.ma"       
        user_first_name = "visiteur"
        user_pdp = 'Images/us2.png'
        allUsers = ''
    
    context = {'visiteur':isguest,
               'user_email':user_email,
               'user_first_name':user_first_name,
               'usersobj':all_users_names,
               'user_pdp':user_pdp,
                'post_form':post_form,
                'group_form':group_form,
                'posts':posts,
                'posts_visitor':posts_visitor,
                'groups':groups,
                'isHomePage':True,
                'eventform': EventForm(),
                'latest_event': latest_event,
                'random_group': random_group,
               }
    
    return render(request, 'HTML/home/home.html', context)

def index_view(request):
    context = {}  

    return render(request,'HTML/index/index.html',context)

def admin_panel(request):
    context = {}  

    return render(request,'HTML/admin_panel/admin_panel.html', context)

def group_view(request):
    context = {}  

    return render(request,'HTML/home/groupe_page.html', context)

def login_view(request):
    context = {}  

    return render(request,'HTML/home/login.html', context)

# seeing my profile
def profile(request):
    context = {
            'userdata':request.user,
            'user_pdp':request.user.utilisateur.profile_picture,
            'utilisateurdata':request.user.utilisateur,
            'skills':models.Skills.objects.filter(utilisateur=request.user.utilisateur),
            'languages':models.Languages.objects.filter(utilisateur=request.user.utilisateur),
            'certificates':models.Certification.objects.filter(utilisateur=request.user.utilisateur),
            'Educations':models.Education.objects.filter(utilisateur=request.user.utilisateur),
            'Experiences':models.Experience.objects.filter(utilisateur=request.user.utilisateur),
            'Reaserches':models.Research.objects.filter(utilisateur=request.user.utilisateur),
            'myprofile':True,
               }  

    return render(request,'HTML/userProfile/profile.html', context)

# seeing others profiles
def view_profile(request,first_name, last_name):
    
    user = User.objects.get(first_name=first_name, last_name=last_name)
    if user is not None:    
        u = utilisateur.objects.get(user_id = user.id)
        if u is not None:
            context = {'userdata':user,
                       'user_pdp': u.profile_picture,
                        'first_name':first_name,
                        'last_name':last_name,
                        'utilisateurdata':u,
            'skills':models.Skills.objects.filter(utilisateur=u),
            'languages':models.Languages.objects.filter(utilisateur=u),
            'certificates':models.Certification.objects.filter(utilisateur=u),
            'Educations':models.Education.objects.filter(utilisateur=u),
            'Experiences':models.Experience.objects.filter(utilisateur=u),
            'Reaserches':models.Research.objects.filter(utilisateur=u),
                        'myprofile':False,
               }  
            return render(request, 'HTML/userProfile/profile.html', context)
        
    return redirect('home')
        
def classroomJoin(request,uid):
    if request.user.is_authenticated:
        classroom = models.ClassRoom.objects.filter(UniqueinvitationCode=uid).first()
        prof = models.Professor.objects.filter(utilisateur=request.user.utilisateur).first()
        # here making sure that if you are a prof and trying to join a cours , you shall not join your own cours
        if prof is not None:
            if (classroom is not None ) and (classroom.Admin_Professor.utilisateur.id is not prof.utilisateur.id):
                if not models.classroomparticipants.objects.filter(Classroom=classroom , Participant = request.user.utilisateur).exists():
                    p = models.classroomparticipants.objects.create(Classroom=classroom , Participant=request.user.utilisateur )
                    p.save()
        else:# else you can join any cours 
            if classroom is not None and ( not models.classroomparticipants.objects.filter(Classroom=classroom , Participant=request.user.utilisateur).exists() ):
                p = models.classroomparticipants.objects.create(Classroom=classroom , Participant=request.user.utilisateur )
                p.save()
            
    return redirect('Classroom')  

def welcome_view(request):
    context = {}  

    return render(request,'HTML/welcome/welcome.html',context)

# 
def homeClass_view(request):
    if request.user.is_authenticated:
        #
        mycourses = []
        allcources = []
        courceswhereiparticipate = models.classroomparticipants.objects.filter(Participant=request.user.utilisateur)

        if request.user.utilisateur.role == 1:
            prof = models.Professor.objects.filter(utilisateur=request.user.utilisateur).first()
            mycourses =models.ClassRoom.objects.filter(Admin_Professor=prof )
        #
        for classr in courceswhereiparticipate:
            allcources.append(classr.Classroom)
        #
        for cours in mycourses:
            allcources.append(cours)
        #
        context = {
            'userdata':request.user,
            'classrooms':allcources,
            'ClassRoomform':ClassRoomForm()
            }  
        return render(request,'HTML/classroom/home.html',context)
    else:
        return redirect('login')

def todo_view(request):
    context = {}  

    return render(request,'HTML/classroom/Todo.html',context)


def chat_app_view(request):
    return render(request, 'HTML/userProfile/chatApp.html')


def contact_view(request):
    return render(request, 'HTML/userProfile/contactInfo.html')

 
def post_view(request,first_name, last_name):

#     if user:
# ~        posts = Post.objects.filter(user=user)
#         context = {'posts': posts, 'user': user}
#     else:
#         context = {'error': 'User not found'}
    
    user = User.objects.get(first_name=first_name, last_name=last_name)
    posts = Post.objects.filter(user=user)

    if user is not None:    
        u = utilisateur.objects.get(user_id = user.id)
        if u is not None:
            context = { 'posts': posts,
                        'user': user,
                        'userdata':user,
                        'user_pdp': u.profile_picture,
                        'first_name':first_name,
                        'last_name':last_name,
                        'utilisateurdata':u,
                        'skills':models.Skills.objects.filter(utilisateur=u),
                        'languages':models.Languages.objects.filter(utilisateur=u),
                        'certificates':models.Certification.objects.filter(utilisateur=u),
                        'Educations':models.Education.objects.filter(utilisateur=u),
                        'Experiences':models.Experience.objects.filter(utilisateur=u),
                        'Reaserches':models.Research.objects.filter(utilisateur=u),
                        'myprofile':False,
                        'postview':True,
               }  
    else: 
        context = {     'error': 'User not found',
                        'userdata':user,
                        'user_pdp': u.profile_picture,
                        'first_name':first_name,
                        'last_name':last_name,
                        'utilisateurdata':u,
                        'skills':models.Skills.objects.filter(utilisateur=u),
                        'languages':models.Languages.objects.filter(utilisateur=u),
                        'certificates':models.Certification.objects.filter(utilisateur=u),
                        'Educations':models.Education.objects.filter(utilisateur=u),
                        'Experiences':models.Experience.objects.filter(utilisateur=u),
                        'Reaserches':models.Research.objects.filter(utilisateur=u),
                        'myprofile':False,
                        'postview':True,
               }  
        
    return render(request,'HTML/userProfile/post.html', context)


 
# def post_view(request):
#     context = {}  
#     return render(request,'HTML/userProfile/post.html', context)


def generate_random_code(length=8):
    characters = string.ascii_letters + string.digits  # includes both uppercase and lowercase letters and digits
    return ''.join(random.choice(characters) for _ in range(length))


#
def create_Classroom(request):
    if request.user.is_authenticated and request.method == 'POST':
        form = ClassRoomForm(request.POST,request.FILES)
        if form.is_valid():
            
            unique_code = generate_random_code()
            while models.ClassRoom.objects.filter(UniqueinvitationCode=unique_code).exists():
                unique_code = generate_random_code() 

            f = form.save(commit=False)
            f.Admin_Professor = models.Professor.objects.filter(utilisateur=request.user.utilisateur).first()
            f.UniqueinvitationCode = unique_code
            f.save()

    return redirect('Classroom')

#
def create_event(request):
    if request.user.is_authenticated and request.method == 'POST':
        form = EventForm(request.POST,request.FILES)
        print(request.POST)
        if form.is_valid():
            f = form.save(commit=False)
            f.utilisateur = models.utilisateur.objects.get(user_id=request.user.id)
            f.save()

    return redirect('all_events')


def view_event(request,id):   
    if request.user.is_authenticated:
        visiteur =False
    else:
        visiteur = True
    context={
        'eventContent':models.Event.objects.filter(id=id).first(),
        'user':request.user,
        'visiteur':visiteur,
    }
    return render(request,'HTML/Events/event.html',context)

# delete event
def deleteEvent(request, id):
    ev = models.Event.objects.filter(id=id).first()
    if ev is not None:
        ev.delete()
        return redirect('all_events')

    return redirect('home')
#
#
def all_events(request):
    
    if request.user.is_authenticated:
        isGuest = False
        groups = Group.objects.filter(usergroup__user=request.user) 
        user = request.user
        user_first_name = user.first_name
        user_pdp = user.utilisateur.profile_picture
    else:
        isGuest = True
        user_first_name = "visiteur"
        user_pdp = 'Images/us2.png'
        groups = None

    context = {'visiteur':isGuest,
               'user_first_name':user_first_name,
               'user_pdp':user_pdp,
                'isHomePage':False,
                'isEventsPage':True,
                'all_events':models.Event.objects.all(),
                'groups':groups
               }
    print(context)
    return render(request,'HTML/home/home.html',context)
#
#
def group_about(request, group_name):
    group = Group.objects.filter(group_name=group_name).first()
    isguest = not request.user.is_authenticated
    target = group.target
    members_count = UserGroup.objects.filter(group=group,invitation_on=True).count()
    if not isguest:
        is_member = group.is_member(request.user)
        is_admin = group.is_admin(request.user)
        context = {'group': group, 'members_count': members_count, 'is_member': is_member, 'is_admin': is_admin, 'user': request.user, 'visiteur': isguest, 'target': target}
    else :
        context = {'group': group, 'members_count': members_count, 'visiteur': isguest, 'target': target}
    
    return render(request, 'HTML/home/group-about.html', context)
#
#
def group_posts(request, group_name):
    isguest = not request.user.is_authenticated
    group = Group.objects.filter(group_name=group_name).first()
    posts = Post.objects.filter(group=group).order_by('-created_at')
    target = group.target
    if not isguest : 
        is_member = group.is_member(request.user)
        is_admin = group.is_admin(request.user)
        if request.method == 'POST':
            post_form = PostForm(request.POST, request.FILES)
            if post_form.is_valid():
                post = post_form.save(commit=False)
                post.user = request.user
                post.group = group
                post.save()
                return redirect('group_posts', group_name=group.group_name)
        else:
            post_form = PostForm()
        context = {'group': group, 'is_member': is_member, 'post_form': post_form, 'posts': posts, 'is_admin': is_admin, 'user': request.user, 'visiteur': isguest, 'target': target}
        print(context)
    elif group.target == 'public':
        context = {'group': group, 'posts': posts, 'user': request.user, 'visiteur': isguest, 'target': target}
    else:
        return redirect('home')
    
    return render(request, 'HTML/home/groupe_page.html', context)

def group_events(request, group_name):
    group = Group.objects.filter(group_name=group_name).first()
    isguest = not request.user.is_authenticated
    is_member = group.is_member(request.user)
    is_admin = group.is_admin(request.user)
    context = {'group': group, 'is_member': is_member, 'is_admin': is_admin, 'user': request.user, 'visiteur': isguest}
    return render(request, 'HTML/home/group_events.html', context)
#
def createQCM(request,uid):
    if request.user.is_authenticated and request.method == 'POST':
        classroom = models.ClassRoom.objects.get(UniqueinvitationCode=uid)
        if classroom is not None:
            qcmform = QcmForm(request.POST)
            if qcmform.is_valid():
                qcm = qcmform.save(commit=False)
                qcm.QCMClassroom = classroom
                qcm.save()

    return redirect('Course', uid=uid)
#
#
# def add_questions(request, qcm_id):
#     if request.method == 'POST':
#         form = QuestionForm(request.POST)
#         if form.is_valid():
#             qcm = models.QCM.objects.get(id=qcm_id)
#             question_text = form.cleaned_data['qst']
#             question = models.Question.objects.create(qcm=qcm, text=question_text)
#             answers = form.cleaned_data['answers']
#             correct_answers = form.cleaned_data['correct_answers']
#             for answer_text in answers:
#                 answer = models.Answer.objects.create(question=question, text=answer_text)
#                 if answer_text in correct_answers:
#                     answer.is_correct = True
#                     answer.save()
#             return redirect('qcm_detail', qcm_id=qcm_id)
#     else:
#         questionform = QuestionForm()
    
#     context = {
#         'questionform': form,
#         'qcm_id': qcm_id
#     }

#     return render( request, 'HTML/classroom/qcm.html',context) 

#
#
def addquestiontoqcm(request):
    qcm_id = int(request.POST.get('qcm_id'))
    if (request.user.is_authenticated ) and (request.user.utilisateur.role == 1 ) and ( request.method == 'POST' ):
        qcm = models.QCM.objects.filter(id=qcm_id).first()
        question_text = request.POST.get('Question')
        question = models.Question.objects.create(qcm=qcm, text=question_text)
        answers = request.POST.getlist('answers[]')
        correct_answers = request.POST.getlist('correct_answers[]')
        
        for index, answer_text in enumerate(answers, start=1):
            if answer_text.strip():  # Check if answer_text is not empty or contains only whitespace
                answer = models.Answer.objects.create(question=question, text=answer_text)
                if str(index) in correct_answers:
                    answer.is_correct = True
                answer.save()
        
        return redirect('qcm', qcmID=qcm_id)
    return redirect('Classroom')
#
#
def qcm_view(request,qcmID):
    if request.user.is_authenticated:
        qcm = models.QCM.objects.filter(id=qcmID).first()
        uid = qcm.QCMClassroom.UniqueinvitationCode

        if ClassRoom.objects.filter(UniqueinvitationCode=uid).exists():
            classroom = ClassRoom.objects.get(UniqueinvitationCode=uid)
        
        # if prof show all questions
        if request.user.utilisateur.role == 1:
            context = {
                        'userdata':request.user,
                        'classroomDetails': classroom,
                        'questionForm':QuestionForm(),
                        'allQuestions':models.Question.objects.filter(qcm=qcm),
                        'qcm_id':qcmID,
                        }  
            return render( request, 'HTML/classroom/qcm.html',context) 
            

        # if student show one question at a time
        elif request.user.utilisateur.role == 2:
            stdent = models.utilisateur.objects.filter(id=request.user.utilisateur.id).first()
            ha = models.studentQcmfinished.objects.filter(student=stdent,qcm=qcm).first()
            # if that student already passed that qcm , he wont need to pass it again 
            if ha:
                return redirect('Classroom')

            qr = models.Question.objects.filter(qcm=qcm).order_by('id')
            querysetsize = qr.count()
            curr = request.POST.get('currentIndex')
            
            if curr is not None:
                nextqstindex = int(curr)+1

                #
                # here save the posted answers 
                #
                question_id =request.POST.get('qstID')
                studentAnswers = request.POST.getlist('answers[]')
                # stdent = models.utilisateur.objects.filter(id=request.user.utilisateur.id).first()
                question = models.Question.objects.filter(id=question_id).first()

                stdqst = models.Studentquestion.objects.create(student=stdent ,question=question )
                for answer_id in studentAnswers:
                    answer = models.Answer.objects.filter(id=answer_id).first()
                    if answer:
                        models.Studentselectedreponse.objects.create(studentquestion=stdqst ,selectedanswer=answer )

                # then i check if there is a next question to show
                # if not this will redirect to Classroom
                if nextqstindex > querysetsize:
                # but i have to save him as completed the qcm , to prevent him to re-pass
                    models.studentQcmfinished.objects.create(student=stdent ,qcm=qcm)
                    # go back to classroom 
                    return redirect('Classroom')
                
                # if there is a next qst , show him next qst
                else : 
                    x = [] 
                    x.append(qr[nextqstindex-1])
                    context = {
                                'userdata':request.user,
                                'classroomDetails': classroom,
                                'allQuestions':x,
                                'curr' : nextqstindex,
                                'islastone': True if nextqstindex == qr.count() else False,
                                'qcm_id':qcmID,
                            }  
                    return render( request, 'HTML/classroom/qcm.html',context) 
                
            # if could not  find the current qst index , mean this is the first time will take a look on the qcm , so show the frst qst        
            else :
                 if qr.count() == 0:
                    return redirect('Classroom')
                 
                 startfromzero = 0
                 x = [] 
                 x.append(qr[startfromzero])
                 context = {
                                'userdata':request.user,
                                'classroomDetails': classroom,
                                'allQuestions':x,
                                'curr' : 1,
                                'islastone': True if 1 == qr.count() else False,
                                'qcm_id':qcmID,
                            }  

            return render( request, 'HTML/classroom/qcm.html',context) 
        
    return redirect('Classroom')
#
#
def create_Classroom_post(request, uid):
    if request.user.is_authenticated and request.method == 'POST':
        classroom = models.ClassRoom.objects.get(UniqueinvitationCode=uid)
        print(classroom)
        if classroom is not None:
            form = PostClassroomForm(request.POST,request.FILES)
            print(form.is_valid())
            if form.is_valid():
                post = form.save(commit=False)
                post.classroom = classroom
                post.author = models.Professor.objects.filter(utilisateur=request.user.utilisateur).first()
                post.save()

    return redirect('Course', uid=uid)

#
#
def kickparticipant(request, id):
    if request.user.is_authenticated:
        m = models.classroomparticipants.objects.filter(id=id).first()
        if m is not None:
            uid = m.Classroom.UniqueinvitationCode
            m.delete()
        
    return redirect('Classroom')
#
#

def course_view(request, uid):
    if request.user.is_authenticated:
        
        if ClassRoom.objects.filter(UniqueinvitationCode=uid).exists():
            classroom = ClassRoom.objects.get(UniqueinvitationCode=uid)
            classroomqcms = models.QCM.objects.filter(QCMClassroom=classroom).order_by('-QCMdelai')
            classroomtasks = Task.objects.filter(classroom=classroom).order_by('-created_at')
            classroomposts = models.PostClassroom.objects.filter(classroom=classroom).order_by('-created_at')
            me = models.utilisateur.objects.filter(id=request.user.utilisateur.id).first()
            meqcm = models.studentQcmfinished.objects.filter(student=me)

            finishedqcmsbyme = []
            for finishedqcmbyme in meqcm:
               finishedqcmsbyme.append(finishedqcmbyme.qcm.id)

            print(finishedqcmsbyme)

            context = {
                'userdata':request.user,
                'classroomDetails': classroom,
                #
                'form':PostClassroomForm(),
                'classroom_posts':classroomposts,
                #
                'classroomparticipants':classroom.participants.all(),
                'finishedqcmsbyme':finishedqcmsbyme,
                #
                'Qcmform': QcmForm(),
                'classroomQCMs':classroomqcms,
                #
                'Taskform':TaskForm(),
                'classroom_tasks':classroomtasks,
                }  
            
            return render(request, 'HTML/classroom/course.html', context)
    
    return redirect('Classroom')
    


def chat(request):
    context = {}  
    return render(request,'HTML/Messaging/messages-page.html', context)

def delete_Classroom(request, uid):
    classroom = models.ClassRoom.objects.filter(UniqueinvitationCode=uid).first()
    if classroom is not None:
        classroom.delete()
        return redirect('Classroom')
#
#
def deletequestion(request,qstid):
    qst = models.Question.objects.filter(id=qstid).first()
    qcmid = qst.qcm.id
    if qst is not None:
        qst.delete()
    return redirect('qcm', qcmID=qcmid)

#
def delete_ClassroomPost(request, id):
    post = models.PostClassroom.objects.filter(id=id).first()
    if post is not None:
        uid = post.classroom.UniqueinvitationCode
        post.delete()
    
    return redirect('Course',uid=uid)
#
def all_groups(request):
    query = request.GET.get('q')
    if query:
        groups = models.Group.objects.filter(target='public', group_name__icontains=query)
    else:
        groups = models.Group.objects.filter(target='public')
    context = {'groups': groups}
    return render(request, 'HTML/components/groups.html', context)

from django.db.models import Q

def all_utilisateurs(request):
    query = request.GET.get('q')
    skills_query = request.GET.get('skills')
    experiences_query = request.GET.get('experiences')
    languages_query = request.GET.get('languages')
    certifications_query = request.GET.get('certifications')
    educations_query = request.GET.get('educations')
    researches_query = request.GET.get('researches')

    users = models.User.objects.filter(is_superuser=False)
    if query or skills_query or experiences_query or languages_query or certifications_query or educations_query or researches_query:
        if query:
            users = users.filter(Q(first_name__icontains=query) | Q(last_name__icontains=query))
        if skills_query:
            users = users.filter(utilisateur__skills__SkillName__icontains=skills_query)
        if experiences_query:
            users = users.filter(Q(utilisateur__experience__titre__icontains=experiences_query) | Q(utilisateur__experience__entreprise__icontains=experiences_query))
        if languages_query:
            users = users.filter(utilisateur__languages__Language__icontains=languages_query)
        if certifications_query:
            users = users.filter(utilisateur__certification__Nom_Certificat__icontains=certifications_query)
        if educations_query:
            users = users.filter(Q(utilisateur__education__UniversityName__icontains=educations_query) | Q(utilisateur__education__FiledOfStudy__icontains=educations_query))
        if researches_query:
            users = users.filter(utilisateur__research__recherche_referrence__icontains=researches_query)

        skills = Skills.objects.filter(SkillName__icontains=skills_query) if skills_query else Skills.objects.none()
        experiences = Experience.objects.filter(Q(titre__icontains=experiences_query) | Q(entreprise__icontains=experiences_query)) if experiences_query else Experience.objects.none()
        languages = Languages.objects.filter(Language__icontains=languages_query) if languages_query else Languages.objects.none()
        certifications = Certification.objects.filter(Nom_Certificat__icontains=certifications_query) if certifications_query else Certification.objects.none()
        educations = Education.objects.filter(Q(UniversityName__icontains=educations_query) | Q(FiledOfStudy__icontains=educations_query)) if educations_query else Education.objects.none()
        researches = Research.objects.filter(recherche_referrence__icontains=researches_query) if researches_query else Research.objects.none()

        etudiants = [user.utilisateur for user in users if hasattr(user, 'utilisateur') and hasattr(user.utilisateur, 'etudiant')]
        professors = list(set([user.utilisateur for user in users if hasattr(user, 'utilisateur') and hasattr(user.utilisateur, 'professor')]))
        enterprises = [user.utilisateur for user in users if hasattr(user, 'utilisateur') and hasattr(user.utilisateur, 'enterprise')]

        context = {'etudiants': etudiants, 'professors': professors, 'enterprises': enterprises, 'skills': skills, 'experiences': experiences, 'languages': languages, 'certifications': certifications, 'educations': educations, 'researches': researches}
    
    else:
        users = models.User.objects.filter(is_superuser=False)[:20]
        context = {'users': users}

    return render(request, 'HTML/components/users.html', context)

def get_student_answers(student_id, qcm_id):
    student = utilisateur.objects.get(id=student_id)
    qcm = models.QCM.objects.get(id=qcm_id)
    howmanyanswers = models.Answer.objects.count()
    # Get all questions belonging to the specified QCM
    questions = qcm.question_set.all()

    student_answers = []
    for question in questions:
        # Check if the student has answered this question
        student_question = models.Studentquestion.objects.filter(student=student, question=question).first()
        if student_question:
            # Retrieve the selected answer for this question
            selected_answer = models.Studentselectedreponse.objects.filter(studentquestion=student_question).first()
            
            if selected_answer:
                student_answers.append(selected_answer.selectedanswer.id)
            # print(student_answers)
    return student_answers

def QCMReponces(request , qcmid , studentid ):
    if request.user.is_authenticated:
        qcm = models.QCM.objects.filter(id=qcmid).first()
        questions = qcm.question_set.all()
        uid = qcm.QCMClassroom.UniqueinvitationCode

        if ClassRoom.objects.filter(UniqueinvitationCode=uid).exists():
            classroom = ClassRoom.objects.get(UniqueinvitationCode=uid)
        
        # if prof show all questions
        # if request.user.utilisateur.role == 1:
        context = {
                    'userdata':request.user,
                    'etudiantdata': utilisateur.objects.filter(id=studentid).first(),
                    'reponcesetudiant':get_student_answers(studentid,qcmid),
                    'classroomDetails': classroom,
                    'questionForm':QuestionForm(),
                    'allQuestions':models.Question.objects.filter(qcm=qcm),
                    'qcm_id':qcmid,
                    'qcm':qcm,
                    }  
        return render( request, 'HTML/classroom/reponcesetudiantsqcm.html',context) 

    return redirect('Classroom')
#
def allresponces(request , QCMID):
    if request.user.is_authenticated:
        
        if models.QCM.objects.filter(id=QCMID).exists() :
            qcm = models.QCM.objects.get(id=QCMID)
            if models.studentQcmfinished.objects.filter(qcm=qcm).exists():
                studentsqcmfinished = models.studentQcmfinished.objects.filter(qcm=qcm)
                x = []
                for stdqcm in studentsqcmfinished:
                    x.append(models.utilisateur.objects.filter(id=stdqcm.student.id).first() )
                context = {
                            'userdata':request.user,
                            'qcm': qcm,
                            'studentspassedtheqcm':x # utilisateur instance
                          }
            return render(request, 'HTML/classroom/etudiantsreponce.html', context)
    return redirect('Classroom')
#
def taskDetails(request,id):
    if request.user.is_authenticated:
        
        task = models.Task.objects.filter(id=id).first()
        uid = task.classroom.UniqueinvitationCode
        classroom = models.ClassRoom.objects.get(UniqueinvitationCode=uid)


        if ClassRoom.objects.filter(UniqueinvitationCode=uid).exists():
            classroom = ClassRoom.objects.get(UniqueinvitationCode=uid)
            context = {
                'userdata':request.user,
                'taskResponseform':TaskResponseForm(),

                'task': task,
                'classroom': classroom
             }
            return render(request, 'HTML/classroom/taskDetails.html', context)
#
def create_Task(request, uid):
    if request.user.is_authenticated and request.method == 'POST':
        classroom = models.ClassRoom.objects.get(UniqueinvitationCode=uid)
        # print(classroom)
        if classroom is not None:
            Taskform = TaskForm(request.POST,request.FILES)
            # print(Taskform.is_valid())
            if Taskform.is_valid():
                task = Taskform.save(commit=False)
                task.classroom = classroom
                task.creator = models.Professor.objects.filter(utilisateur=request.user.utilisateur).first()
                task.save()

    return redirect('Course', uid=uid)
#
def create_TaskResponse(request, id):
    if request.user.is_authenticated and request.method == 'POST':
        task = models.Task.objects.get(id=id)
    

        if task:
            print(task)
            taskResponseform = TaskResponseForm(request.POST, request.FILES)
            if taskResponseform.is_valid():
                taskResponse = taskResponseform.save(commit=False)
                taskResponse.task = task
                taskResponse.student = Etudiant.objects.filter(utilisateur=request.user.utilisateur).first()
                taskResponse.save()
                return redirect('Course', id=id)
#        
def deleteTask(request, id):
    task = models.Task.objects.filter(id=id).first()
    if task is not None:
        uid = task.classroom.UniqueinvitationCode
        task.delete()
    
    return redirect('Course',uid=uid)

def deleteQCM(request,QCMID):
    if request.user.is_authenticated:
        m = models.QCM.objects.filter(id=QCMID).first()
        if m is not None:
            m.delete()        
    return redirect('Classroom') 