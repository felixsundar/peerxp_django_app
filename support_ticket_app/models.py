from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin

# Create your models here.
# class MyUser(AbstractBaseUser, PermissionsMixin):
#     userId = models.BigAutoField(primary_key=True, unique=True)
#     email = models.EmailField(verbose_name='Email', max_length=255, unique=True, blank=False, null=False)
#     firstname = models.CharField(verbose_name='Full Name', max_length=255, blank=False, null=False)
#     lastname = models.CharField(verbose_name='Full Name', max_length=255, blank=False, null=False)
    
#     USERNAME_FIELD = 'email'
#     EMAIL_FIELD = 'email'
#     REQUIRED_FIELDS = ['firstname', 'lastname']

class APIToken(models.Model):
    tokenID = models.CharField(primary_key=True, max_length=255)
    accessToken = models.CharField(max_length=255)
    refreshToken = models.CharField(max_length=255)
    clientID = models.CharField(max_length=255)
    clientSecret = models.CharField(max_length=255)
    scope = models.CharField(max_length=255)
    lastUpdatedTime = models.DateTimeField()
    expiresIn = models.IntegerField()
