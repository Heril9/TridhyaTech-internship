"""
Models for the blog application.

This module defines the core data models for the blog application:
- Author: Custom user model for authentication and author management
- Tag: Model for categorizing posts
- Post: Main blog post model
"""

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password


# Create your models here.
    

class Author(AbstractUser):
    """
    Custom user model that extends Django's AbstractUser.
    Used for authentication and author management in the blog application.
    
    Fields inherited from AbstractUser:
    - username: Unique identifier for the author
    - email: Author's email address
    - password: Hashed password for authentication
    
    Additional methods:
    - __str__: Returns the username for string representation
    """
    
    class Meta:
        db_table = 'blog_author'
        verbose_name = 'Author'
        verbose_name_plural = 'Authors'

    def __str__(self):
        return self.username


class Tag(models.Model):
    """
    Model representing tags that can be associated with posts.
    
    Fields:
    - name: Unique name of the tag (CharField, max_length=50)
    - created_by: ForeignKey to Author who created the tag (optional)
    
    Methods:
    - __str__: Returns the tag name for string representation
    """
    name = models.CharField(max_length=50, unique=True)
    created_by = models.ForeignKey(
        Author, 
        on_delete=models.CASCADE, 
        related_name="created_tags", 
        null=True, 
        blank=True
    )

    class Meta:
        db_table = 'blog_tag'
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    def __str__(self):
        return self.name


class Post(models.Model):
    """
    Model representing blog posts.
    
    Fields:
    - title: Title of the post (CharField, max_length=200)
    - content: Main content of the post (TextField)
    - timestamp: When the post was created (DateTimeField, auto_now_add=True)
    - author: ForeignKey to Author who created the post
    - tags: ManyToMany relationship with Tag
    
    Methods:
    - __str__: Returns the post title for string representation
    """
    title = models.CharField(max_length=200)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        Author, 
        on_delete=models.CASCADE, 
        related_name="posts"
    )
    tags = models.ManyToManyField(
        Tag, 
        blank=True,
        related_name="posts"
    )

    class Meta:
        db_table = 'blog_post'
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    def __str__(self):
        return self.title










