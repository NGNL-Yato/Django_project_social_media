from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import User


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
    professors = models.ManyToManyField(Professor, related_name='researches')
    #
    recherche_referrence = models.CharField(max_length=100,blank=True, null=True) # public id or referrence
    description = models.TextField(blank=True, null=True)
    recherche_document = models.FileField(upload_to='research_documents/', blank=True, null=True)
    #
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

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
   
#
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
class Event(models.Model):
    entreprise = models.ForeignKey(Enterprise, on_delete=models.CASCADE)
    #
    background_image = models.ImageField(upload_to='event_images/', blank=True)
    head_title = models.CharField(max_length=100)
    event_time = models.DateTimeField()
    description = models.TextField(blank=True, null=True)
    file = models.FileField(upload_to='event_files/', blank=True)
    #
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  

    def __str__(self):
        return 'Event:'+self.head_title
 
#    
# 
class follow(models.Model):
    follower = models.ForeignKey(utilisateur, related_name='following', on_delete=models.CASCADE)
    followed = models.ForeignKey(utilisateur, related_name='followers', on_delete=models.CASCADE)

    def __str__(self):
        return self.follower.user.first_name+' '+self.follower.user.last_name+"  -->  "+self.followed.user.first_name+' '+self.followed.user.last_name

#
#
class Group(models.Model):
    group_name = models.CharField(max_length=100)
    members = models.ManyToManyField(User)

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
#
#
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
