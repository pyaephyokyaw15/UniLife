from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    profile_picture = models.ImageField(null=True, upload_to='profile_pictures',  default='profile_pictures/default_user.png')
    university = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.username




