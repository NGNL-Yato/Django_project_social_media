from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import User


class utilisateur(models.Model):
    # username = models.CharField(max_length=255)
    # password = models.CharField(max_length=255)
    # email = models.EmailField()
    # first_name = models.CharField(max_length=255, blank=True)
    # last_name = models.CharField(max_length=255, blank=True)
    #
    user = models.OneToOneField(User,null=False,on_delete=models.CASCADE)
    role = models.IntegerField(blank=True, null=True)
    phone_number = models.PositiveIntegerField(blank=True, null=True)
    #
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True)
    CV = models.FileField(upload_to='cv_files/', blank=True)
    BIO = models.TextField(blank=True)
    public_email = models.EmailField(blank=True)
    public_phone_number = models.PositiveIntegerField(blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    # @classmethod
    # def signup(cls, username, password, email):
    #     hashed_password = make_password(password)
    #     return cls.objects.create(
    #         username=username,
    #         password=hashed_password,
    #         email=email
    #     )

    # @classmethod
    # def login(cls, username, password):
    #     try:
    #         user = cls.objects.get(username=username)
    #     except cls.DoesNotExist:
    #         return None

    #     if check_password(password, user.password):
    #         return user
    #     else:
    #         return None
        
        
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
