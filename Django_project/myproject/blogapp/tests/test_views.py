from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient, force_authenticate
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from ..models import Post, Tag

class APITests(APITestCase):
    def setUp(self):
        """Set up test data and authentication"""
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.superuser = get_user_model().objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpass123'
        )
        self.tag = Tag.objects.create(
            name='Test Tag',
            created_by=self.user
        )
        self.post = Post.objects.create(
            title='Test Post',
            content='Test Content',
            author=self.user
        )
        self.post.tags.add(self.tag)

        # Get JWT token for authentication
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    def test_author_registration(self):
        """Test author registration endpoint"""
        url = '/api/authors/'
        data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'password': 'newpass123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(get_user_model().objects.count(), 3)

    def test_get_posts_list(self):
        """Test getting list of posts"""
        url = '/api/posts/'
        force_authenticate(self.client, user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_post(self):
        """Test creating a new post"""
        url = '/api/posts/'
        force_authenticate(self.client, user=self.user)
        data = {
            'title': 'New Post',
            'content': 'New Content',
            'tag_ids': [self.tag.id]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 2)
        new_post = Post.objects.latest('id')
        self.assertEqual(new_post.tags.count(), 1)
        self.assertEqual(new_post.tags.first(), self.tag)

    def test_update_post(self):
        """Test updating a post"""
        url = f'/api/posts/{self.post.id}/'
        force_authenticate(self.client, user=self.user)
        data = {
            'title': 'Updated Post',
            'content': 'Updated Content'
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, 'Updated Post')

    def test_delete_post(self):
        """Test deleting a post"""
        url = f'/api/posts/{self.post.id}/'
        force_authenticate(self.client, user=self.user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Post.objects.count(), 0)

    def test_get_tags_list(self):
        """Test getting list of tags"""
        url = '/api/tags/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_tag_as_superuser(self):
        """Test creating a new tag as superuser"""
        # Use superuser credentials for tag creation
        refresh = RefreshToken.for_user(self.superuser)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        
        url = '/api/tags/'
        data = {
            'name': 'New Tag',
            'created_by_id': self.superuser.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Tag.objects.count(), 2)

    def test_create_tag_as_regular_user(self):
        """Test creating a tag as regular user (should fail)"""
        url = '/api/tags/'
        data = {
            'name': 'New Tag',
            'created_by_id': self.user.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthorized_access(self):
        """Test unauthorized access to protected endpoints"""
        self.client.credentials()  # Remove authentication
        url = '/api/posts/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_permission_restrictions(self):
        """Test permission restrictions"""
        # Create another user
        other_user = get_user_model().objects.create_user(
            username='otheruser',
            email='other@example.com',
            password='otherpass123'
        )
        
        # Create a post for the other user
        other_post = Post.objects.create(
            title='Other Post',
            content='Other Content',
            author=other_user
        )
        
        # Try to access the post with the original user's credentials
        force_authenticate(self.client, user=self.user)
        
        # Test read access (should be allowed)
        detail_url = f'/api/posts/{other_post.id}/'
        get_response = self.client.get(detail_url)
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)
        
        # Test write access (should be forbidden)
        data = {'title': 'Unauthorized Update'}
        patch_response = self.client.patch(detail_url, data, format='json')
        self.assertEqual(patch_response.status_code, status.HTTP_403_FORBIDDEN)
        
        # Test delete access (should be forbidden)
        delete_response = self.client.delete(detail_url)
        self.assertEqual(delete_response.status_code, status.HTTP_403_FORBIDDEN) 