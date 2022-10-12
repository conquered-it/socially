from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    email= models.EmailField(max_length=100, unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username',]
    
    def __str__(self):
        return str(self.email)

class Relationship(models.Model):
    follower = models.ForeignKey(User, related_name="followings", on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name="followers", on_delete=models.CASCADE)
    is_active = models.BooleanField(default=False)

class Post(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    author = models.ForeignKey(User, related_name="posts", on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)

class Like(models.Model):
    post = models.ForeignKey(Post, related_name="likes", on_delete=models.CASCADE)
    liked_by = models.ForeignKey(User, related_name="likes", on_delete=models.CASCADE)
    is_active = models.BooleanField(default=False)

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    commented_by = models.ForeignKey(User, related_name="comments", on_delete=models.CASCADE)
    comment_body = models.TextField()