"""
Serializers for the blog application.

This module contains the serializer classes that handle data serialization and deserialization:
- CustomTokenObtainPairSerializer: Custom JWT token serializer
- AuthorSerializer: Handles user registration and profile management
- TagSerializer: Manages tag data
- PostSerializer: Handles blog post data
"""

from rest_framework import serializers
from .models import Author, Post, Tag
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom JWT token serializer that includes additional user information
    in the token response.
    
    Extends TokenObtainPairSerializer to include:
    - username
    - email
    - user_id
    
    Methods:
    - validate: Adds additional user information to the token response
    """
    def validate(self, attrs):
        data = super().validate(attrs)
        data['username'] = self.user.username
        data['email'] = self.user.email
        data['user_id'] = self.user.id
        return data


class AuthorSerializer(serializers.ModelSerializer):
    """
    Serializer for Author model.
    Handles user registration, updates, and profile management.
    
    Fields:
    - id: User's unique identifier
    - username: User's username
    - email: User's email address
    - password: User's password (write-only)
    
    Methods:
    - validate: Checks for existing users during registration
    - create: Creates a new user
    - update: Updates user information
    """
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Author
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True},
            'username': {'required': False},
            'email': {'required': False}
        }

    def validate(self, attrs):
        """
        Validate user data during registration.
        Checks for existing users with same credentials.
        """
        username = attrs.get('username')
        email = attrs.get('email')
        
        # For update operations, we don't need to check existing users
        if self.instance is None:
            # Check if user with same credentials exists
            existing_user = Author.objects.filter(
                username=username,
                email=email
            ).first()
            
            if existing_user:
                raise serializers.ValidationError({
                    'detail': 'User with these credentials already exists'
                })
            
        return attrs

    def create(self, validated_data):
        """
        Create a new user with the validated data.
        """
        user = Author.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

    def update(self, instance, validated_data):
        """
        Update an existing user's information.
        Handles password updates separately for security.
        """
        # Update password if provided
        if 'password' in validated_data:
            instance.set_password(validated_data.pop('password'))
        
        # Update other fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        return instance


class TagSerializer(serializers.ModelSerializer):
    """
    Serializer for Tag model with full details including creator information.
    Used for tag creation and detailed views.
    
    Fields:
    - id: Tag's unique identifier
    - name: Tag's name
    - created_by: Author who created the tag (read-only)
    - created_by_id: ID of the author who created the tag (write-only)
    """
    created_by = AuthorSerializer(read_only=True)
    created_by_id = serializers.PrimaryKeyRelatedField(
        queryset=Author.objects.all(), 
        write_only=True, 
        source='created_by'
    )

    class Meta:
        model = Tag
        fields = ['id', 'name', 'created_by', 'created_by_id']


class TagDetailSerializer(serializers.ModelSerializer):
    """
    Simplified serializer for Tag model.
    Used in list views and nested serializations.
    
    Fields:
    - id: Tag's unique identifier
    - name: Tag's name
    """
    class Meta:
        model = Tag
        fields = ['id', 'name']


class PostSerializer(serializers.ModelSerializer):
    """
    Serializer for Post model with full details.
    Handles post creation, updates, and detailed views.
    
    Fields:
    - id: Post's unique identifier
    - title: Post's title
    - content: Post's content
    - author: Author details (read-only)
    - tags: Tag details (read-only)
    - tag_ids: Tag IDs (write-only)
    
    Methods:
    - create: Creates a new post and establishes tag relationships
    """
    author = AuthorSerializer(read_only=True)
    tags = TagDetailSerializer(many=True, read_only=True)
    tag_ids = serializers.PrimaryKeyRelatedField(
        many=True, 
        queryset=Tag.objects.all(), 
        write_only=True, 
        source='tags',
        required=False
    )

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'author', 'tags', 'tag_ids']
        read_only_fields = ['author']

    def create(self, validated_data):
        """
        Create a new post and establish tag relationships.
        """
        tag_ids = validated_data.pop('tags', [])
        post = Post.objects.create(**validated_data)
        from django.core.exceptions import ObjectDoesNotExist
        try:
            post.tags.add(*tag_ids)
        except ObjectDoesNotExist:
            raise serializers.ValidationError("One or more tags do not exist.")
        
        return post


class AuthorListSerializer(serializers.ModelSerializer):
    """
    Simplified serializer for Author model.
    Used in list views to show basic author information.
    
    Fields:
    - username: Author's username
    """
    class Meta:
        model = Author
        fields = ['username']


class PostListSerializer(serializers.ModelSerializer):
    """
    Simplified serializer for Post model.
    Used in list views to show basic post information.
    
    Fields:
    - id: Post's unique identifier
    - title: Post's title
    - content: Post's content
    - author: Author's username
    - tags: Tag names
    """
    author = serializers.CharField(source='author.username')
    tags = TagDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'author', 'tags']
        read_only_fields = ['author', 'tags']


