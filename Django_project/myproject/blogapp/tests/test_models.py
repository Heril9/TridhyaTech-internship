from django.test import TestCase
from django.contrib.auth import get_user_model
from ..models import Post, Tag

class ModelTests(TestCase):
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

    def test_author_creation(self):
        """Test author model creation"""
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertTrue(self.user.check_password('testpass123'))

    def test_tag_creation(self):
        """Test tag model creation"""
        self.assertEqual(self.tag.name, 'Test Tag')
        self.assertEqual(self.tag.created_by, self.user)

    def test_post_creation(self):
        """Test post model creation"""
        self.assertEqual(self.post.title, 'Test Post')
        self.assertEqual(self.post.content, 'Test Content')
        self.assertEqual(self.post.author, self.user)

    def test_post_tag_relationship(self):
        """Test post-tag relationship"""
        self.post.tags.add(self.tag)
        self.assertIn(self.tag, self.post.tags.all())
        self.assertIn(self.post, self.tag.posts.all())

    def test_post_str_representation(self):
        """Test post string representation"""
        self.assertEqual(str(self.post), 'Test Post')

    def test_tag_str_representation(self):
        """Test tag string representation"""
        self.assertEqual(str(self.tag), 'Test Tag') 