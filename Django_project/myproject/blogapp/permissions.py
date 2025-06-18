"""
Custom permission classes for the blog application.

This module defines custom permission classes that control access to different resources:
- IsPostAuthor: Controls access to post operations
- IsSuperuserOrReadOnly: Controls access to tag operations
"""

from rest_framework import permissions

class IsPostAuthor(permissions.BasePermission):
    """
    Custom permission class for post operations.
    Ensures that:
    - List endpoint (/api/posts/) is accessible to all authenticated users
    - Detail endpoint (/api/posts/{id}/) is accessible only to the post author
    
    Methods:
    - has_permission: Checks if user is authenticated
    - has_object_permission: Checks if user has permission for specific post
    """
    def has_permission(self, request, view):
        """
        Check if the user is authenticated for all operations.
        This is a global check that applies to all requests.
        """
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """
        Check if the user has permission to access the post.
        - For list endpoint: Allow all authenticated users
        - For detail endpoint: Allow only the post author
        """
        # If it's a list action or retrieve action, allow all authenticated users
        if view.action in ['list', 'retrieve']:
            return True
            
        # For other actions (update, delete), only allow the author of the post
        return obj.author == request.user

class IsSuperuserOrReadOnly(permissions.BasePermission):
    """
    Custom permission class for tag operations.
    Ensures that:
    - Read-only access is allowed for authenticated users
    - Only superusers can create or delete tags
    
    Methods:
    - has_permission: Checks if user has permission for tag operations
    """
    def has_permission(self, request, view):
        """
        Check if the user has permission to perform tag operations.
        - Read-only access for authenticated users
        - Write access for superusers only
        """
        # Allow read-only access for authenticated users
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        
        # Allow write access only to superusers
        return request.user and request.user.is_superuser


