from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
import os

# Create your models here.

def get_default_profile_pic():
    return 'profile_pic/default.jpg'

class CustomerSignUp(models.Model):
    user = models.OneToOneField(
        User, unique=True, on_delete=models.CASCADE, related_name='customer')
    first_name = models.CharField(max_length=250, blank=True, null=True)
    last_name = models.CharField(max_length=250, blank=True, null=True)
    email = models.EmailField(max_length=100, blank=True, null=True)
    address = models.CharField(
        max_length=250, default='Manila, Philippines', blank=True, null=True)
    profile_picture = models.ImageField(
        upload_to='profile_pic', default=get_default_profile_pic, null=True, blank=True)
    designation = models.CharField(max_length=100, blank=True, null=True)
    phone = models.IntegerField(blank=True, null=True)
    information = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.username

    def get_profile_picture_url(self):
        if self.profile_picture and hasattr(self.profile_picture, 'url'):
            try:
                return self.profile_picture.url
            except:
                return '/static/images/default-profile.png'
        return '/static/images/default-profile.png'

# class CustomerLogin(models.Model):
#     username = models.CharField(max_length=250, blank=False, null=False)
#     password = models.PasswordField(max_length=100, blank=False)
