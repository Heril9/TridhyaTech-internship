# Django Blogging API

A robust RESTful API for a blogging platform built with Django and Django REST Framework.

## Features

- **User Authentication**
  - JWT-based authentication
  - User registration and profile management
  - Role-based access control

- **Blog Management**
  - Create, read, update, and delete blog posts
  - Tag-based categorization
  - Rich text content support

- **Performance Optimizations**
  - Query optimization with select_related and prefetch_related
  - Caching for frequently accessed endpoints
  - Efficient serializer usage

- **Security**
  - Custom permission classes
  - Secure password handling
  - Protected endpoints

## Tech Stack

- Python 3.x
- Django 4.x
- Django REST Framework
- JWT Authentication
- SQLite (Development)
- PostgreSQL (Production-ready)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd myproject
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. Run migrations:
```bash
python manage.py migrate
```

6. Create superuser:
```bash
python manage.py createsuperuser
```

7. Run development server:
```bash
python manage.py runserver
```

## API Endpoints

### Authentication
- `POST /api/token/` - Get JWT tokens
- `POST /api/token/refresh/` - Refresh JWT token

#### Example Response (Token Generation)
```json
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### Authors
- `POST /api/authors/` - Register new author
- `GET /api/authors/` - List all authors
- `GET /api/authors/{id}/` - Get author details
- `PUT /api/authors/{id}/` - Update author profile
- `DELETE /api/authors/{id}/` - Delete author account

#### Example Request (Author Registration)
```json
{
    "username": "johndoe",
    "email": "john@example.com",
    "password": "securepassword123"
}
```

#### Example Response (Author Details)
```json
{
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "date_joined": "2024-04-29T10:00:00Z",
    "is_active": true
}
```

### Posts
- `GET /api/posts/` - List all posts
- `POST /api/posts/` - Create new post
- `GET /api/posts/{id}/` - Get post details
- `PUT /api/posts/{id}/` - Update post
- `DELETE /api/posts/{id}/` - Delete post

#### Example Request (Create Post)
```json
{
    "title": "My First Blog Post",
    "content": "This is the content of my first blog post...",
    "tag_ids": [1, 2]
}
```

#### Example Response (Post Details)
```json
{
    "id": 1,
    "title": "My First Blog Post",
    "content": "This is the content of my first blog post...",
    "author": {
        "id": 1,
        "username": "johndoe"
    },
    "tags": [
        {
            "id": 1,
            "name": "Technology"
        },
        {
            "id": 2,
            "name": "Programming"
        }
    ],
    "timestamp": "2024-04-29T10:30:00Z"
}
```

### Tags
- `GET /api/tags/` - List all tags
- `POST /api/tags/` - Create new tag (superuser only)
- `GET /api/tags/{id}/` - Get tag details
- `PUT /api/tags/{id}/` - Update tag
- `DELETE /api/tags/{id}/` - Delete tag

#### Example Request (Create Tag)
```json
{
    "name": "Technology"
}
```

#### Example Response (Tag Details)
```json
{
    "id": 1,
    "name": "Technology",
    "created_by": {
        "id": 1,
        "username": "johndoe"
    }
}
```

## Error Responses

### 400 Bad Request
```json
{
    "error": "Invalid input",
    "details": {
        "title": ["This field is required"],
        "content": ["This field is required"]
    }
}
```

### 401 Unauthorized
```json
{
    "detail": "Authentication credentials were not provided."
}
```

### 403 Forbidden
```json
{
    "detail": "You do not have permission to perform this action."
}
```

### 404 Not Found
```json
{
    "detail": "Not found."
}
```

## Authentication

The API uses JWT (JSON Web Tokens) for authentication. To authenticate:

1. Get access token:
```bash
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "your_username", "password": "your_password"}'
```

2. Use the token in subsequent requests:
```bash
curl -H "Authorization: Bearer your_token" http://localhost:8000/api/posts/
```

## Permissions

- **IsPostAuthor**: Controls post operations
  - Allows read access to all authenticated users
  - Allows write access (create, update, delete) only to post authors
  - Used for managing blog posts

- **IsSuperuserOrReadOnly**: Controls tag operations
  - Allows read access to all authenticated users
  - Allows write access (create, update, delete) only to superusers
  - Used for managing tags

## Testing

Run the test suite:
```bash
python manage.py test blogapp.tests
```

The test suite includes:
- Model tests
- View tests
- Permission tests
- Authentication tests

## Performance Optimizations

1. **Query Optimization**
   - Uses `select_related` for foreign key relationships
   - Uses `prefetch_related` for many-to-many relationships
   - Optimized database queries

2. **Caching**
   - Implemented for frequently accessed endpoints
   - Cache timeout configurable in settings
   - Automatic cache invalidation on updates

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Django REST Framework for providing the robust API framework
- Simple JWT for implementing secure token-based authentication
- Django Cache Framework for optimizing API performance 