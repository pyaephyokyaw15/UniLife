from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    profile_picture = models.ImageField(null=True)
    university = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.username




