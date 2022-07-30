from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinLengthValidator
from django.conf import settings

# Create your models here.
class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="posts")
    image = models.ImageField(null=True)   # , upload_to='banner'
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_date = models.DateTimeField(default=timezone.now, editable=False)
    saved_by = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="saved_posts", blank=True)
    liked_by = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="liked_posts", blank=True)

    class Meta:
        ordering = ["-created_date"]

    @property
    def like_counts(self):
        return self.liked_by.count


class Comment(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comments")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    comment = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-created_date"]

