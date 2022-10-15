from socialapp.models import User, Relationship, Post, Like, Comment
from socialapp.api.serializers import RegisterSerializer, RelationshipSerializer, UserProfileSerializer, PostSerializer, PostCreateSerializer, LikeSerializer, CommentSerializer, AllPostsSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError

class Register(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    
    def perform_create(self, serializer):
        if serializer.is_valid():
            user = User(username=self.request.data['username'], email=self.request.data['email'])
            user.set_password(self.request.data['password'])
            user.save()
            return user
        raise ValidationError("User data is invalid")

class Follow(generics.CreateAPIView):
    queryset = Relationship.objects.all()
    serializer_class = RelationshipSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        if self.kwargs['pk']==self.request.user.id :
            raise ValidationError("You cannot follow yourself")
        try:
            following = User.objects.get(pk=self.kwargs['pk'])
        except:
            raise ValidationError("User to be followed is not found")
        
        follower = self.request.user
        try:
            relationship = Relationship.objects.get(follower=follower, following=following)
        except:
            serializer.save(follower=follower, following=following, is_active=True)
            return
        
        if relationship.is_active==True:
            raise ValidationError("You already follow this user")
        relationship.is_active = True
        relationship.save()

class Unfollow(generics.CreateAPIView):
    queryset = Relationship.objects.all()
    serializer_class = RelationshipSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        if self.kwargs['pk']==self.request.user.id:
            raise ValidationError("You cannot unfollow yourself")
        try:
            following = User.objects.get(pk=self.kwargs['pk'])
        except:
            raise ValidationError("User to be unfollowed is not found")
        
        follower = self.request.user
        
        try:
            relationship = Relationship.objects.get(follower=follower, following=following)
        except:
            raise ValidationError("You already unfollow the user")
        
        if relationship.is_active==False:
            raise ValidationError("You already unfollow the user")
        
        relationship.is_active = False
        relationship.save()

class UserProfile(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return self.request.user

class PostCreate(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        author = self.request.user
        serializer.save(author=author)

class PostView(generics.RetrieveDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_destroy(self, serializer):
        if serializer.author == self.request.user:
            serializer.delete()
        else:
            raise ValidationError("You are not allowed to delete this post")

class LikeView(generics.CreateAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        try:
            post = Post.objects.get(pk=self.kwargs['pk'])
        except:
            raise ValidationError("Post not found")
        
        liked_by = self.request.user
        
        try:
            like = Like.objects.get(post=post, liked_by=liked_by)
        except:
            serializer.save(post=post, liked_by=liked_by, is_active=True)
            return

        if like.is_active==True:
            raise ValidationError("You've already liked this post")
        like.is_active = True
        like.save()

class UnlikeView(generics.CreateAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        try:
            post = Post.objects.get(pk=self.kwargs['pk'])
        except:
            raise ValidationError("Post not found")
        
        liked_by = self.request.user
        
        try:
            like = Like.objects.get(post=post, liked_by=liked_by)
        except:
            raise ValidationError("You've already unliked the post")
        
        if like.is_active==False:
            raise ValidationError("You already unliked the post")
        
        like.is_active = False
        like.save()

class CommentView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        try:
            post = Post.objects.get(pk=self.kwargs['pk'])
        except:
            raise ValidationError("Post not found")
        
        commented_by = self.request.user
        serializer.save(post=post, commented_by=commented_by)

class AllPostsView(generics.ListAPIView):
    serializer_class = AllPostsSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Post.objects.filter(author=self.request.user).order_by('-created_time')