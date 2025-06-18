"""
Views for the blog application.

This module contains the view classes that handle HTTP requests and responses:
- AuthorViewSet: Handles user registration and profile management
- TagViewSet: Manages tag creation and listing
- PostViewSet: Handles blog post operations
- CustomTokenObtainPairView: Custom JWT token generation
"""

from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework import viewsets, status, permissions
from rest_framework_simplejwt.views import TokenObtainPairView
from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.conf import settings

from .models import Author, Post, Tag
from .serializers import (
    AuthorSerializer, PostSerializer, TagSerializer, 
    CustomTokenObtainPairSerializer, AuthorListSerializer, 
    PostListSerializer, TagDetailSerializer
)
from .permissions import ( IsSuperuserOrReadOnly, IsPostAuthor)     
from rest_framework.permissions import IsAuthenticated


class AuthorViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Author model.
    Handles user registration, profile management, and authentication.
    
    Endpoints:
    - POST /api/authors/: Register a new user
    - GET /api/authors/: List all authors (usernames only)
    - GET /api/authors/{id}/: Get author details
    - PUT /api/authors/{id}/: Update author profile
    - DELETE /api/authors/{id}/: Delete author account
    
    Permissions:
    - Registration: Public access
    - Other operations: Requires authentication
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

    def get_permissions(self):
        """
        Override get_permissions to make create (register) public
        while keeping other actions authenticated.
        """
        if self.action == 'create':
            permission_classes = []  # No authentication needed for registration
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        """
        Use different serializer for list action to show simplified data.
        """
        if self.action == 'list':
            return AuthorListSerializer
        return AuthorSerializer

    def get_queryset(self):
        """
        For list action, show all authors' usernames.
        For other actions, only show authenticated user's data.
        """
        if self.action == 'list':
            return Author.objects.all()
        elif self.request.user.is_authenticated:
            return Author.objects.filter(id=self.request.user.id)
        return Author.objects.none()

    def update(self, request, *args, **kwargs):
        """
        Allow authors to update only their own data.
        Handles password updates securely.
        """
        try:
            instance = self.get_object()
            
            # Check if the user is trying to update their own data
            if instance.id != request.user.id:
                return Response(
                    {'detail': 'You can only update your own data'},
                    status=status.HTTP_403_FORBIDDEN
                )
            
            # Remove password from request data if not provided
            if 'password' not in request.data:
                request.data.pop('password', None)
            
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            
            return Response(serializer.data)
            
        except Exception as e:
            return Response(
                {'detail': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    def destroy(self, request, *args, **kwargs):
        """
        Perform hard delete of the author.
        Only allowed for the author's own account.
        """
        try:
            instance = self.get_object()
            instance.delete()
            return Response("User deleted successfully", status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response(
                {'detail': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    def create(self, request, *args, **kwargs):
        """
        Create a new author (user registration).
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            try:
                user = serializer.save()
                return Response({
                    'message': 'User registered successfully',
                    'user': AuthorSerializer(user).data
                }, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({
                    'detail': str(e)
                }, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TagViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Tag model.
    Handles tag creation, management, and listing.
    
    Endpoints:
    - GET /api/tags/: List all tags
    - POST /api/tags/: Create a new tag
    - GET /api/tags/{id}/: Get tag details
    - PUT /api/tags/{id}/: Update tag
    - DELETE /api/tags/{id}/: Delete tag
    
    Permissions:
    - Read operations: Requires authentication
    - Write operations: Requires superuser status
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated, IsSuperuserOrReadOnly]

    @method_decorator(cache_page(settings.CACHE_TTL))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_serializer_class(self):
        """
        Use different serializer for list action to show simplified data.
        """
        if self.action == 'list':
            return TagDetailSerializer
        return TagSerializer

    def perform_create(self, serializer):
        """
        Automatically set the creator when creating a new tag.
        """
        serializer.save(created_by=self.request.user)
        # Clear cache when new tag is created
        cache.clear()

    def get_queryset(self):
        """
        For list view, show all tags to authenticated users.
        For detail view, show all tags to superusers, 
        otherwise only show tags created by the user.
        """
        if self.action == 'list':
            return Tag.objects.all()
        if self.request.user.is_superuser:
            return Tag.objects.all()
        return Tag.objects.filter(created_by=self.request.user)


class PostViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Post model.
    Handles post creation, management, and listing.
    
    Endpoints:
    - GET /api/posts/: List all posts
    - POST /api/posts/: Create a new post
    - GET /api/posts/{id}/: Get post details
    - PUT /api/posts/{id}/: Update post
    - DELETE /api/posts/{id}/: Delete post
    
    Permissions:
    - Read operations: Requires authentication
    - Write operations: Requires post author status
    """
    queryset = Post.objects.select_related('author').prefetch_related('tags').all()
    serializer_class = PostSerializer
    permission_classes = [IsPostAuthor]

    def get_queryset(self):
        """
        Show all posts to authenticated users.
        Let the permission class handle access control.
        """
        if self.request.user.is_authenticated:
            return Post.objects.select_related('author').prefetch_related('tags').all()
        return Post.objects.none()

    def get_serializer_class(self):
        """
        Use different serializer for list action to show simplified data.
        """
        if self.action == 'list':
            return PostListSerializer
        return PostSerializer

    def perform_create(self, serializer):
        """
        Automatically set the author when creating a new post.
        """
        serializer.save(author=self.request.user)
        # Clear cache when new post is created
        cache.clear()

    def list(self, request, *args, **kwargs):
        """
        List all posts with caching.
        """
        cache_key = 'post_list'
        cached_data = cache.get(cache_key)
        
        if cached_data is None:
            response = super().list(request, *args, **kwargs)
            cache.set(cache_key, response.data, settings.CACHE_TTL)
            return response
            
        return Response(cached_data)


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Custom view for JWT token generation.
    Uses CustomTokenObtainPairSerializer to include additional user information.
    
    Endpoint:
    - POST /api/token/: Generate JWT tokens
    
    Response includes:
    - access_token: Short-lived token for API access
    - refresh_token: Long-lived token for getting new access tokens
    - username: User's username
    - email: User's email
    - user_id: User's ID
    """
    serializer_class = CustomTokenObtainPairSerializer

