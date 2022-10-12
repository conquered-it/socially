"""jobify URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from socialapp.api.views import Register, Follow, Unfollow, UserProfile, PostCreate, PostView, LikeView, UnlikeView, CommentView, AllPostsView

urlpatterns = [
    path("authenticate", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh", TokenRefreshView.as_view(), name="token_refresh"),
    path("register",  Register.as_view(), name="register"),
    path("follow/<int:pk>", Follow.as_view(), name="follow"),
    path("unfollow/<int:pk>", Unfollow.as_view(), name="unfollow"),
    path("user", UserProfile.as_view(), name="user"),
    path("posts/", PostCreate.as_view(), name="posts"),
    path("posts/<int:pk>", PostView.as_view(), name="posts"),
    path("like/<int:pk>", LikeView.as_view(), name="like"),
    path("unlike/<int:pk>", UnlikeView.as_view(), name="unlike"),
    path("comment/<int:pk>", CommentView.as_view(), name="comment"),
    path("all_posts", AllPostsView.as_view(), name="all_posts"),
]
