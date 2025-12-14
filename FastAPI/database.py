from datetime import datetime
from typing import Dict, List, Optional
from models import User, Post


class MockDatabase:
    """Mock in-memory database for demonstration purposes"""
    
    def __init__(self):
        self.users: Dict[int, dict] = {}
        self.posts: Dict[int, dict] = {}
        self.user_id_counter = 1
        self.post_id_counter = 1
        self._seed_data()
    
    def _seed_data(self):
        """Add some initial data"""
        self.users[1] = {
            "id": 1,
            "username": "johndoe",
            "email": "john@example.com",
            "full_name": "John Doe",
            "password": "hashed_password_123",
            "is_active": True,
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }
        self.users[2] = {
            "id": 2,
            "username": "janedoe",
            "email": "jane@example.com",
            "full_name": "Jane Doe",
            "password": "hashed_password_456",
            "is_active": True,
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }
        self.user_id_counter = 3
        
        self.posts[1] = {
            "id": 1,
            "user_id": 1,
            "title": "My First Post",
            "content": "This is my first post content",
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }
        self.posts[2] = {
            "id": 2,
            "user_id": 1,
            "title": "Another Post",
            "content": "More content here",
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }
        self.post_id_counter = 3


# Global database instance
db = MockDatabase()
