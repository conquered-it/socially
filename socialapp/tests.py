from socialapp.models import User, Relationship, Post, Like, Comment
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status 
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
import json

# Create your tests here.

class AuthenticateTestCase(APITestCase):
    
    def setUp(self):
        self.user = User.objects.create(username="dummy", email="dummy@gmail.com")
        self.user.set_password("password")
        self.user.save()
    
    def test_autheticate(self):
        data = {
            "email": "dummy@gmail.com",
            "password": "password"
        }
        response = self.client.post(reverse('token_obtain_pair'),data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(json.loads(response.content).get('refresh'))
        self.assertIsNotNone(json.loads(response.content).get('access'))
    
    def test_autheticate_wrong_credentials(self):
        data = {
            "email": "dummy@gmail.com",
            "password": "xyzpassword"
        }
        response = self.client.post(reverse('token_obtain_pair'),data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIsNone(json.loads(response.content).get('refresh'))
        self.assertIsNone(json.loads(response.content).get('access'))
    
    def test_autheticate_fields_missing(self):
        data1 = {
            "password":"password"
        }
        response1 = self.client.post(reverse('token_obtain_pair'),data1)
        self.assertEqual(response1.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIsNone(json.loads(response1.content).get('refresh'))
        self.assertIsNone(json.loads(response1.content).get('access'))
        
        data2 = {
            "email":"dummy@gmail.com"
        }
        response2 = self.client.post(reverse('token_obtain_pair'),data1)
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIsNone(json.loads(response2.content).get('refresh'))
        self.assertIsNone(json.loads(response2.content).get('access'))

class FollowTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username="dummy", password="password", email="dummy@gmail.com")
        self.client = APIClient()
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        self.following_user = User.objects.create(username="dummy2", email="dummy2@gmail.com", password="password")
    
    def test_follow(self):
        response = self.client.post(reverse('follow', args=(self.following_user.id,)))
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Relationship.objects.filter(follower=self.user, following=self.following_user, is_active=True).exists())
        self.assertTrue(self.user.followings.filter(following=self.following_user, is_active=True).exists())
    
    def test_self_follow(self):
        response = self.client.post(reverse('follow', args=(self.user.id,)))
        number_of_followers = self.user.followers.filter(is_active=True).count()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(number_of_followers, self.user.followers.filter(is_active=True).count())

class UnfollowTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username="dummy", password="password", email="dummy@gmail.com")
        self.client = APIClient()
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        self.following_user = User.objects.create(username="dummy2", email="dummy2@gmail.com", password="password")
        
    def test_unfollow(self):
        Relationship.objects.create(follower = self.user, following = self.following_user, is_active = True)
        response = self.client.post(reverse('unfollow', args=(self.following_user.id,)))
        self.assertEqual(response.status_code, 201)
        self.assertEqual(self.user.followings.filter(is_active=True).count(), 0)

class UserProfileTestCase(APITestCase):
    def setUp(self):
        self.user_1 = User.objects.create(username="dummy", password="password", email="dummy@gmail.com")
        self.client_1 = APIClient()
        refresh_1 = RefreshToken.for_user(self.user_1)
        self.client_1.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh_1.access_token}')
        
        self.user_2 = User.objects.create(username="dummy2", password="password", email="dummy2@gmail.com")
        self.client_2 = APIClient()
        refresh_2 = RefreshToken.for_user(self.user_2)
        self.client_2.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh_2.access_token}')
    
    def test_user_profile(self):
        response_1 = self.client_1.get(reverse('user'))
        response_2 = self.client_2.get(reverse('user'))
        self.assertEqual(json.loads(response_1.content)['username'],"dummy")
        self.assertEqual(json.loads(response_2.content)['username'],"dummy2")

class PostCreateTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username="dummy", password="password", email="dummy@gmail.com")
        self.client = APIClient()
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    
    def test_post_create(self):
        data = {
            "title": "Test title",
            "description": "Test description"
        }
        response = self.client.post(reverse('posts'), data)
        self.assertEqual(response.status_code, 201)
        post = json.loads(response.content)
        db_post = Post.objects.get(id=post.get('id'))
        self.assertEqual(post.get('title'), 'Test title')
        self.assertEqual(post.get('title'),db_post.title)
        self.assertEqual(post.get('description'),db_post.description)
    
    def test_post_missing_field(self):
        number_of_posts = Post.objects.all().count()
        data = {
            "description": "Test description"
        }
        response = self.client.post(reverse('posts'), data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content)['title'], ["This field is required."])
        self.assertEqual(number_of_posts, Post.objects.all().count())
    
class PostViewTestCase(APITestCase):
    def setUp(self):
        self.user_1 = User.objects.create(username="dummy", password="password", email="dummy@gmail.com")
        self.client_1 = APIClient()
        refresh_1 = RefreshToken.for_user(self.user_1)
        self.client_1.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh_1.access_token}')
        
        self.user_2 = User.objects.create(username="dummy2", password="password", email="dummy2@gmail.com")
        self.client_2 = APIClient()
        refresh_2 = RefreshToken.for_user(self.user_2)
        self.client_2.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh_2.access_token}')
        
        self.post = Post.objects.create(title="title", description="description", author=self.user_1)
    
    def test_post_get(self):
        response = self.client_1.get(reverse('post_view', args=(self.post.id,)))
        self.assertEqual(response.status_code, 200)
        post = json.loads(response.content)
        db_post = Post.objects.get(id=post.get('id'))
        self.assertEqual(post.get('title'),db_post.title)
        self.assertEqual(post.get('description'),db_post.description)
    
    def test_post_delete(self):
        response_1 = self.client_1.delete(reverse('post_view', args=(self.post.id,)))
        self.assertEqual(response_1.status_code, 204)
        self.assertEqual(Post.objects.all().count(), 0)
    
    def test_post_delete_by_other_user(self):
        response_2 = self.client_2.delete(reverse('post_view', args=(self.post.id,)))
        self.assertEqual(response_2.status_code, 400)
        self.assertEqual(Post.objects.all().count(), 1)

class LikeTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username="dummy", password="password", email="dummy@gmail.com")
        self.client = APIClient()
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        
        self.post = Post.objects.create(title="title", description="description", author=self.user)
    
    def test_like(self):
        response = self.client.post(reverse('like', args=(self.post.id,)))
        self.assertEqual(response.status_code, 201)
        self.assertEqual(self.post.likes.filter(is_active=True).count(), 1)

class UnlikeTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username="dummy", password="password", email="dummy@gmail.com")
        self.client = APIClient()
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        
        self.post = Post.objects.create(title="title", description="description", author=self.user)
    
    def test_unlike(self):
        Like.objects.create(post = self.post, liked_by = self.user, is_active = True)
        response = self.client.post(reverse('unlike', args=(self.post.id,)))
        self.assertEqual(response.status_code, 201)
        self.assertEqual(self.post.likes.filter(is_active=False).count(), 1)

class CommentTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username="dummy", password="password", email="dummy@gmail.com")
        self.client = APIClient()
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        
        self.post = Post.objects.create(title="title", description="description", author=self.user)
    
    def test_comment(self):
            data = {
                "comment_body": "This is a comment"
            }
            response = self.client.post(reverse('comment', args =(self.post.id,)), data)
            
            self.assertEqual(response.status_code, 201)
            self.assertEqual(self.post.comments.all().count(), 1)
            comment = json.loads(response.content)
            db_comment = Comment.objects.get(id=comment.get('id'))
            self.assertEqual(comment['comment_body'], db_comment.comment_body)

class AllPostsTestCase(APITestCase):
    def setUp(self):
        self.user_1 = User.objects.create(username="dummy", password="password", email="dummy@gmail.com")
        self.user_2 = User.objects.create(username="dummy2", password="password", email="dummy2@gmail.com")
        self.client = APIClient()
        refresh = RefreshToken.for_user(self.user_1)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        
        self.post = Post.objects.create(title="title", description="description", author=self.user_1)
        self.post_2 = Post.objects.create(title="title", description="description", author=self.user_2)
        self.post_3 = Post.objects.create(title="title", description="description", author=self.user_1)
    
    def test_all_posts(self):
        response = self.client.get(reverse('all_posts'))
        self.assertEqual(response.status_code, 200)
        posts = json.loads(response.content)
        self.assertEqual(len(posts), 2)