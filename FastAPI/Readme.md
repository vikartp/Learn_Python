# FastAPI Users CRUD API

A RESTful API built with FastAPI demonstrating CRUD operations with nested routes. This project includes a users endpoint with nested posts functionality, showcasing proper API design patterns.

## Features

- ✨ Full CRUD operations for Users
- 📝 Nested CRUD operations for User Posts
- 🔄 RESTful API design with proper HTTP methods
- 📚 Auto-generated API documentation (Swagger UI & ReDoc)
- 🐳 Docker support
- ✅ Input validation with Pydantic
- 🎯 Mock in-memory database (for demonstration)

## Project Structure

```
FastAPI/
├── main.py              # Application entry point
├── models.py            # Pydantic models
├── database.py          # Mock database implementation
├── routers/
│   ├── __init__.py
│   └── users.py         # User and post routes
├── requirements.txt     # Python dependencies
├── Dockerfile          # Docker configuration
├── .dockerignore       # Docker ignore file
└── Readme.md           # This file
```

## API Endpoints

### Users
- `GET /api/v1/users/` - Get all users (with pagination)
- `GET /api/v1/users/{user_id}` - Get a specific user
- `POST /api/v1/users/` - Create a new user
- `PUT /api/v1/users/{user_id}` - Update a user
- `DELETE /api/v1/users/{user_id}` - Delete a user

### User Posts (Nested Routes)
- `GET /api/v1/users/{user_id}/posts` - Get all posts by a user
- `POST /api/v1/users/{user_id}/posts` - Create a post for a user
- `GET /api/v1/users/{user_id}/posts/{post_id}` - Get a specific post
- `PUT /api/v1/users/{user_id}/posts/{post_id}` - Update a post
- `DELETE /api/v1/users/{user_id}/posts/{post_id}` - Delete a post

### Utility
- `GET /` - Root endpoint
- `GET /health` - Health check

## Running Locally

### Prerequisites
- Python 3.11 or higher
- pip

### Setup

1. **Create a virtual environment:**
   ```bash
   python -m venv venv
   ```

2. **Activate the virtual environment:**
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - Linux/Mac:
     ```bash
     source venv/bin/activate
     ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```bash
   python main.py
   ```
   
   Or use uvicorn directly:
   ```bash
   uvicorn main:app --reload
   ```

5. **Access the API:**
   - API: http://localhost:8000
   - Interactive docs (Swagger UI): http://localhost:8000/docs
   - Alternative docs (ReDoc): http://localhost:8000/redoc

## Running with Docker

### Build the Docker image:
```bash
docker build -t fastapi-users-api .
```

### Run the container:
```bash
docker run -d -p 8000:8000 --name fastapi-app fastapi-users-api
```

### Access the API:
- API: http://localhost:8000
- Docs: http://localhost:8000/docs

### Stop the container:
```bash
docker stop fastapi-app
docker rm fastapi-app
```

## Example Usage

### Create a User
```bash
curl -X POST "http://localhost:8000/api/v1/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "newuser",
    "email": "newuser@example.com",
    "full_name": "New User",
    "password": "securepass123"
  }'
```

### Get All Users
```bash
curl "http://localhost:8000/api/v1/users/"
```

### Create a Post for User
```bash
curl -X POST "http://localhost:8000/api/v1/users/1/posts" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My New Post",
    "content": "This is the content of my post"
  }'
```

### Get User's Posts
```bash
curl "http://localhost:8000/api/v1/users/1/posts"
```

## Mock Data

The application comes pre-seeded with sample data:

**Users:**
- ID 1: johndoe (john@example.com)
- ID 2: janedoe (jane@example.com)

**Posts:**
- ID 1: "My First Post" by johndoe
- ID 2: "Another Post" by johndoe

## Development

### Code Structure
- **models.py**: Pydantic models for request/response validation
- **database.py**: In-memory mock database (replace with real DB in production)
- **routers/users.py**: API endpoints and business logic
- **main.py**: Application initialization and configuration

### Next Steps for Production
- Replace mock database with PostgreSQL/MySQL
- Add authentication and authorization
- Implement password hashing (bcrypt)
- Add database migrations (Alembic)
- Add comprehensive error handling
- Add logging
- Add unit and integration tests
- Add rate limiting
- Environment-based configuration

## License

This is a learning project for educational purposes.