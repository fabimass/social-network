from django.contrib.auth.models import AbstractUser
from django.db import models
from .settings import NEW_POST_LENGTH


class User(AbstractUser):
    pass

class Post(models.Model):
    content = models.CharField(max_length=NEW_POST_LENGTH)
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings_owned")
    liked_by = models.ManyToManyField(User, blank=True, related_name="posts_liked")
    date_posted = models.DateTimeField()

    def __str__(self):
        return f"{self.id}: {self.posted_by} on {self.date_posted}"
    
    def is_liked_by(self, user):
        return self.liked_by.filter(id=user.id).exists()
