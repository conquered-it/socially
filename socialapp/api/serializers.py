from rest_framework.exceptions import ValidationError
from rest_framework import serializers
from socialapp.models import User, Relationship, Post, Like, Comment

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class RelationshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Relationship
        fields = []

class UserProfileSerializer(serializers.ModelSerializer):
    followers = serializers.SerializerMethodField(read_only=True)
    followings = serializers.SerializerMethodField(read_only=True)
    
    def get_followers(self, obj):
        return self.context["request"].user.followers.filter(is_active=True).count()
    
    def get_followings(self, obj):
        return self.context["request"].user.followings.filter(is_active=True).count()

    class Meta:
        model = User
        fields = ['username', 'followers', 'followings']


class PostCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['commented_by','comment_body',]
  
class PostSerializer(serializers.ModelSerializer):
    
    likes = serializers.SerializerMethodField(read_only=True)
    comments = PostCommentSerializer(many=True, read_only=True)
    
    def get_likes(self, obj):
        return obj.likes.filter(is_active=True).count()

    class Meta:
        model = Post
        fields = "__all__"

class PostCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        exclude = ['author']

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = []

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        exclude = ["post", "commented_by"]

class AllPostsSerializer(serializers.ModelSerializer):
    
    likes = serializers.SerializerMethodField(read_only=True)
    comments = PostCommentSerializer(many=True, read_only=True)
    
    def get_likes(self, obj):
        return obj.likes.filter(is_active=True).count()

    class Meta:
        model = Post
        exclude = ['author']