from django.contrib import admin
from socialapp.models import User, Relationship, Post, Like, Comment
# Register your models here.
admin.site.register(User)
admin.site.register(Relationship)
admin.site.register(Post)
admin.site.register(Like)
admin.site.register(Comment)