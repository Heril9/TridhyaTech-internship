from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from ..models import Post, Tag
from ..serializers import (
    AuthorSerializer, PostSerializer, TagSerializer,
    PostListSerializer, TagDetailSerializer
)

class SerializerTests(TestCase):
    def setUp(self):
        """Set up test data"""
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
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

    def test_author_serializer(self):
        """Test author serializer"""
        serializer = AuthorSerializer(self.user)
        data = serializer.data
        self.assertEqual(data['username'], 'testuser')
        self.assertEqual(data['email'], 'test@example.com')
        self.assertNotIn('password', data)

    def test_tag_serializer(self):
        """Test tag serializer"""
        serializer = TagSerializer(self.tag)
        data = serializer.data
        self.assertEqual(data['name'], 'Test Tag')
        self.assertEqual(data['created_by']['username'], 'testuser')
        self.assertNotIn('created_by_id', data)

    def test_post_serializer(self):
        """Test post serializer"""
        serializer = PostSerializer(self.post)
        data = serializer.data
        self.assertEqual(data['title'], 'Test Post')
        self.assertEqual(data['content'], 'Test Content')
        self.assertEqual(data['author']['username'], 'testuser')
        self.assertEqual(len(data['tags']), 1)
        self.assertEqual(data['tags'][0]['name'], 'Test Tag')

    def test_post_list_serializer(self):
        """Test post list serializer"""
        serializer = PostListSerializer(self.post)
        data = serializer.data
        self.assertEqual(data['title'], 'Test Post')
        self.assertEqual(data['author'], 'testuser')
        self.assertEqual(len(data['tags']), 1)
        self.assertEqual(data['tags'][0]['name'], 'Test Tag')

    def test_tag_detail_serializer(self):
        """Test tag detail serializer"""
        serializer = TagDetailSerializer(self.tag)
        data = serializer.data
        self.assertEqual(data['name'], 'Test Tag')
        self.assertNotIn('created_by', data)

    def test_author_serializer_validation(self):
        """Test author serializer validation"""
        data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'password': 'newpass123'
        }
        serializer = AuthorSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_tag_serializer_validation(self):
        """Test tag serializer validation"""
        data = {
            'name': 'New Tag',
            'created_by_id': self.user.id
        }
        serializer = TagSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        
        # Test invalid created_by_id
        invalid_data = {
            'name': 'New Tag',
            'created_by_id': 999  # Non-existent user ID
        }
        serializer = TagSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('created_by_id', serializer.errors) 