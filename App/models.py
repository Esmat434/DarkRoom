from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin
import uuid as uid
# Create your models here.

class CustomUserManager(BaseUserManager):
    def create_user(self,email,password=None,**extrafields):
        if not email:
            raise ValueError("the Email Field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email,**extrafields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self,email,password=None,**extrafields):
        extrafields.setdefault('is_staff',True)
        extrafields.setdefault('is_superuser',True)
        
        return self.create_user(email,password,**extrafields)
    
class CustomUser(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50,unique=True)
    first_name = models.CharField(max_length=50,blank=True)
    last_name = models.CharField(max_length=50,blank=True)
    avatar = models.ImageField(upload_to='images/',blank=True)
    phone_number = models.CharField(max_length=12,unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joind = models.DateTimeField(auto_now_add=True)
    uuid  = models.UUIDField(default=uid.uuid4,editable=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','phone_number']

    def __str__(self) -> str:
        return self.username
    
class ChatData(models.Model):
    sender = models.CharField(max_length=200,default='')
    receiver = models.CharField(max_length=200,default='')
    message = models.TextField(blank=True)
    hidden = models.BooleanField(default=False)
    created_time = models.DateTimeField(auto_now_add=True)

class PersonalToken(models.Model):
    sender = models.CharField(max_length=100)
    receiver = models.CharField(max_length=100)
    Token= models.UUIDField(default=uid.uuid4,editable=False)
    created_time = models.TimeField(auto_now_add=True)

class GroupToken(models.Model):
    admin = models.CharField(max_length=100,default='')
    groupname = models.CharField(max_length=100,unique=True)
    picture = models.ImageField(upload_to='',blank=True)
    group_uuid = models.UUIDField(default=uid.uuid4,editable=False)
    created_time = models.TimeField(auto_now=True)

    def __str__(self) -> str:
        return self.groupname

class UserGroup(models.Model):
    admin = models.CharField(max_length=100,default='')
    groupname = models.CharField(max_length=100,unique=True)
    picture = models.ImageField(upload_to='',blank=True)
    group_uuid = models.CharField(max_length=255)
    created_time = models.TimeField(auto_now=True)

    def __str__(self) -> str:
        return self.admin

class Users(models.Model):
    username = models.CharField(max_length=100)
    uuid_name= models.CharField(max_length=100)
    uuid_id = models.CharField(max_length=255,unique=True)
    uuid = models.CharField(max_length=255)
    created_time = models.DateTimeField(auto_now_add=True)

class GroupData(models.Model):
    username = models.CharField(max_length=100)
    message = models.TextField()
    is_enable = models.BooleanField(default=True)
    created_time = models.DateTimeField(auto_now=True)  