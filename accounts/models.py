from django.db import models
from django.contrib.auth.models import AbstractUser



# Create your models here.
class User(AbstractUser):
    profile_picture = models.ImageField(null=True, upload_to='profile_pictures')
    university = models.CharField(max_length=200, blank=True)
    followers = models.ManyToManyField('self', blank=True, symmetrical=False)

    def __str__(self):
        return self.username

    @property
    def following(self):
        return User.objects.filter(followers=self)






