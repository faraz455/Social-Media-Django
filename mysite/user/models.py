from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

# Create your models here.
class CustomUserManager(BaseUserManager):
    # funtion that create users and email is neccesary
    def _create_user(self,email, password, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        # User created
        user = self.model(email=email, **extra_fields)
        # Password hashing
        user.set_password(password)
        # User gets saved
        user.save()
        return user

    # Function that create super user with some mendatory default fields
    # After neccesary checks it calls _create_user function
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('name', "admin")

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Super user must have is_staff equal to True")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Super user must have is_superuser equal to True")

        return self._create_user(email, password, **extra_fields)

# Class used to create custom user with objec having custome user manager
class CustomUser(AbstractBaseUser, PermissionsMixin):
    # field required for a user
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=25)
    created_at = models.DateTimeField(auto_now_add = True)  
    updated_at = models.DateTimeField(auto_now = True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = "email"
    objects = CustomUserManager() 

    def __str__(self) :
        return self.email

class Follower(models.Model):
    user_obj = models.ForeignKey(CustomUser,on_delete=models.CASCADE, related_name='userObj')
    follower_obj = models.ForeignKey(CustomUser,on_delete=models.CASCADE, related_name='followerObj')
    created_at = models.DateTimeField(auto_now_add = True)  
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.user_obj.name

class Posts(models.Model):
    image_url = models.URLField(max_length=100, blank=True)
    message = models.CharField(max_length=200, blank=True)
    # likes = models.PositiveBigIntegerField()
    post_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='posts')
    created_at = models.DateTimeField(auto_now_add = True)  
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.message


