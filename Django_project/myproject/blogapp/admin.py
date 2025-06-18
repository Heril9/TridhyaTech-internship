from django.contrib import admin
from .models import Author, Post, Tag

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    """
    Admin interface configuration for the Author model.
    Provides list display, search, and filtering capabilities for user management.
    """
    list_display = ('username', 'email', 'is_superuser', 'is_staff')
    search_fields = ('username', 'email')
    list_filter = ('is_superuser', 'is_staff')

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """
    Admin interface configuration for the Tag model.
    Provides list display, search, and filtering capabilities for tag management.
    """
    list_display = ('name', 'created_by')
    search_fields = ('name',)
    list_filter = ('created_by',)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """
    Admin interface configuration for the Post model.
    Provides list display, search, and filtering capabilities for blog post management.
    """
    list_display = ('title', 'author', 'timestamp')
    search_fields = ('title', 'content')
    list_filter = ('author', 'timestamp')

