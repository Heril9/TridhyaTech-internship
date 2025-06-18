"""
URL configuration for myproject project.

This module defines the URL patterns for the entire project:
- Admin interface URLs
- API endpoints for blog functionality
- JWT authentication endpoints

The `urlpatterns` list routes URLs to views. For more information please see:
https://docs.djangoproject.com/en/5.2/topics/http/urls/
"""

from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from blogapp.views import (
    AuthorViewSet, 
    PostViewSet, 
    TagViewSet, 
    CustomTokenObtainPairView
)


# =====================
# API Router Configuration
# =====================

# Initialize the DefaultRouter for API endpoints
router = DefaultRouter()

# Register API endpoints with the router
# Each endpoint corresponds to a specific model and its operations
router.register(r'authors', AuthorViewSet)      # User management endpoints
router.register(r'posts', PostViewSet)          # Blog post management endpoints
router.register(r'tags', TagViewSet)            # Tag management endpoints


# =====================
# URL Patterns
# =====================

urlpatterns = [
    # Django admin interface
    path('admin/', admin.site.urls),
    
    # API endpoints
    path('api/', include(router.urls)),
    
    # JWT Authentication endpoints
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

