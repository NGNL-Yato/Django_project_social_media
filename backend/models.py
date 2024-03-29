from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.conf import settings

class utilisateur(models.Model):
    user = models.OneToOneField(User,null=False,on_delete=models.CASCADE)
    role = models.IntegerField(blank=True, null=True)
    phone_number = models.PositiveIntegerField(blank=True, null=True)
    #
    online_status = models.BooleanField(default=False)
    profile_picture = models.ImageField(default='profile_pictures/us2.png',upload_to='profile_pictures/', blank=True)
    CV = models.FileField(upload_to='cv_files/', blank=True)
    BIO = models.TextField(blank=True)
    AboutME = models.TextField(blank=True , null=True)
    public_email = models.EmailField(blank=True)
    public_phone_number = models.PositiveIntegerField(blank=True, null=True)
    #
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name
        
    def set_first_name(self, value):
        self.first_name = value

    def get_first_name(self):
        return self.first_name

    def set_last_name(self, value):
        self.last_name = value

    def get_last_name(self):
        return self.last_name

    def set_cv(self, value):
        self.cv = value

    def get_cv(self):
        return self.cv

    def set_description(self, value):
        self.description = value

    def get_description(self):
        return self.description

    def set_profile_picture(self, value):
        self.profile_picture = value

    def get_profile_picture(self):
        return self.profile_picture

    def set_phone_number(self, value):
        self.phone_number = value

    def get_phone_number(self):
        return self.phone_number

    def set_personal_email(self, value):
        self.personal_email = value

    def get_personal_email(self):
        return self.personal_email

    def set_in_profile_phone_number(self, value):
        self.in_profile_phone_number = value

    def get_in_profile_phone_number(self):
        return self.in_profile_phone_number

    def set_role(self, value):
        self.role = value

    def get_role(self):
        return self.role
    

#
# 
class Etudiant(models.Model):
    utilisateur = models.OneToOneField(utilisateur, on_delete=models.CASCADE)
    #
    filiere = models.CharField(max_length=100,blank=True, null=True)
    date_inscription = models.DateField(blank=True,null=True)
    #
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    
    def __str__(self):
        return 'Etudiant :'+self.utilisateur.user.first_name +' '+self.utilisateur.user.last_name


#
# Prof
class Professor(models.Model):
    utilisateur = models.OneToOneField(utilisateur, on_delete=models.CASCADE)
    # 
    poste_administratif = models.CharField(max_length=100,blank=True, null=True) # !!!!
    date_integration = models.DateField(null=True)
    #
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return 'Professeur :'+self.utilisateur.user.first_name +' '+self.utilisateur.user.last_name
#
#   Recherche des Doctorants (carrer de prof)
class Research(models.Model):
    utilisateur = models.ForeignKey(utilisateur, on_delete=models.CASCADE) # this is a referrance for who posted the research 
    #
    recherche_referrence = models.CharField(max_length=100,blank=True, null=True) # public id or referrence
    description = models.TextField(blank=True, null=True)
    recherche_document = models.FileField(upload_to='research_documents/', blank=True, null=True)
    #
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

# thos will be all professors that has a relation with the researches posted
class research_profs(models.Model):
    professor = models.ForeignKey(Professor, related_name='Professor', on_delete=models.CASCADE)
    research = models.ForeignKey(Research, related_name='Research', on_delete=models.CASCADE)

#    
#
class Experience(models.Model):
    utilisateur = models.ForeignKey(utilisateur, on_delete=models.CASCADE)
    #
    titre =  models.CharField(max_length=100)
    entreprise = models.CharField(max_length=100, default='Self Employed')
    description = models.TextField(blank=True, null=True)
    date_debut = models.DateField()
    date_fin = models.DateField()
    picture = models.ImageField(default='profile_pictures/jobs.png',upload_to='Experiences_images/', blank=True)
    #
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
#
#
class Education(models.Model):
    utilisateur = models.ForeignKey(utilisateur, on_delete=models.CASCADE)
    #
    UniversityName =  models.CharField(max_length=100)
    FiledOfStudy = models.CharField(max_length=100)
    date_debut = models.DateField()
    date_fin = models.DateField(null=True,blank=True)
    picture = models.ImageField(default='profile_pictures/jobs.png',upload_to='University_images/', blank=True)
    #
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

class Skills(models.Model):
    utilisateur = models.ForeignKey(utilisateur, on_delete=models.CASCADE)
    #
    SkillName =  models.CharField(max_length=100,blank=True)
    #
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.utilisateur.user.first_name+' '+self.utilisateur.user.last_name+'knows : '+ self.SkillName
#
#
class Languages(models.Model):
    utilisateur = models.ForeignKey(utilisateur, on_delete=models.CASCADE)
    #
    Language =  models.CharField(max_length=100,blank=True)
    #
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
#
#
class Certification(models.Model):
    utilisateur = models.ForeignKey(utilisateur, on_delete=models.CASCADE)
    #
    Nom_Certificat =  models.CharField(max_length=100)
    date_obtention = models.DateField()
    description = models.TextField()
    picture = models.ImageField(default='profile_pictures/jobs.png',upload_to='Certificates_images/', blank=True)
    #
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
   

#   Entreprise
class Enterprise(models.Model):
    utilisateur = models.OneToOneField(utilisateur, on_delete=models.CASCADE)
    #
    localisation = models.CharField(max_length=100,blank=True, null=True)
    fax = models.PositiveIntegerField(blank=True, null=True)
    #
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    
    def __str__(self):
        return 'Entreprise :'+self.utilisateur.user.first_name +' '+self.utilisateur.user.last_name

#    
# 
class follow(models.Model):
    follower = models.ForeignKey(utilisateur, related_name='following', on_delete=models.CASCADE)
    followed = models.ForeignKey(utilisateur, related_name='followers', on_delete=models.CASCADE)

    def __str__(self):
        return self.follower.user.first_name+' '+self.follower.user.last_name+"  -->  "+self.followed.user.first_name+' '+self.followed.user.last_name
#
#

def get_default_user():
    return settings.DEFAULT_USER_ID

class Group(models.Model):
    group_name = models.CharField(max_length=100)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='admin_groups')
    profile_banner = models.ImageField(default='profile_pictures/img_banniere.png',upload_to='profile_pictures/', blank=True)
    description = models.TextField(default = "Add a description to this group here...")
    target = models.CharField(max_length=100, default='Public')
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    def is_member(self, user):
        return self.usergroup_set.filter(user=user).exists()
    def save(self, *args, **kwargs):
        # Check if this is a new instance
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new:
            UserGroup.objects.create(user=self.user, group=self, is_admin=True, invitation_on=True)
    def is_admin(self, user):
        return self.usergroup_set.filter(user=user, is_admin=True).exists()

#
#
class Event(models.Model):
    utilisateur = models.ForeignKey(utilisateur, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE,blank=True,null=True)
    #
    backgroundimage = models.ImageField(upload_to='event_images/')
    head_title = models.CharField(max_length=100)
    event_time = models.DateField()
    description = models.TextField(blank=True, null=True)
    file = models.FileField(upload_to='event_files/', blank=True)
    #
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  

    def __str__(self):
        return 'Event:'+self.head_title
 
#
# a classroom is made by one professsor , but other proffessors can be invited to join too 
#
class ClassRoom(models.Model):
    Admin_Professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    #
    ClassRoomtitle = models.CharField(max_length=100)
    UniqueinvitationCode = models.CharField(max_length=20,unique=True)
    ClassRoomimage = models.FileField(upload_to='classroom_course_images/')
    description = models.TextField(blank=True, null=True)
    #
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  

#
# a pivot table between utilisateurs and classroom , (many to many)
#
class classroomparticipants(models.Model):
    Classroom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE)
    Participant = models.ForeignKey(utilisateur , on_delete=models.CASCADE)

#
#  qcm belongs to a class room , classroom can have many qcms (one to many)
#
class QCM(models.Model):
    Classroom = models.ForeignKey(ClassRoom, default=None ,on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    delai =  models.DateTimeField()
    description = models.TextField(blank=True, null=True)


#
#  a qcm contain many questions (one to many)
#
class Question(models.Model):
    qcm = models.ForeignKey(QCM, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)

#
# one question can have many answers (one to many)
#
class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

#
# pivot table between students and questions  (many to many)
#
class Studentquestion(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

#
# pivot table between students and responce (refer to the answer student selected)  (many to many)
#
class Studentselectedreponse(models.Model):
    studentquestion = models.ForeignKey(Studentquestion, on_delete=models.CASCADE)
    selectedanswer = models.ForeignKey(Answer, on_delete=models.CASCADE)


#  
#
class UserGroup(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    is_admin = models.BooleanField(default=False)
    invitation_on = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
#
#
class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, blank=True)
    #
    contenue = models.TextField()
    file = models.FileField(upload_to='post_files/', null=True, blank=True)
    #
    created_at = models.DateTimeField(auto_now_add=True)

    def like_post(self, user):
        like, created = Like.objects.get_or_create(user=user, post=self)
        if not created:
            like.delete()
            return False
        return True
    
    def count_likes(self):
        return Like.objects.filter(post=self).count()
    
    def get_user_profile_picture(self):
        return self.user.utilisateur.profile_picture
#
#
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
#
#
class Conversation(models.Model):
    title = models.CharField(max_length=200, null=True, blank=True)
    Conversation_picture = models.ImageField(default='profile_pictures/img_banniere.png',upload_to='profile_pictures/', blank=True)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
#
#
class Participant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    group_id = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True)
#
#
class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
#
#
class MessageFile(models.Model):
    message = models.ForeignKey(Message, related_name='files', on_delete=models.CASCADE)
    file = models.FileField(upload_to='messages_files/', null=True, blank=True)