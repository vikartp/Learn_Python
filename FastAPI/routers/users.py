from fastapi import APIRouter, HTTPException, status
from typing import List
from datetime import datetime

from models import User, UserCreate, UserUpdate, Post, PostCreate, PostUpdate
from database import db

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

# Nested router for user posts
posts_router = APIRouter()


@router.get("/", response_model=List[User])
def get_users(skip: int = 0, limit: int = 100):
    """Get all users with pagination"""
    users = list(db.users.values())[skip:skip + limit]
    return users


@router.get("/{user_id}", response_model=User)
def get_user(user_id: int):
    """Get a specific user by ID"""
    if user_id not in db.users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )
    return db.users[user_id]


@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate):
    """Create a new user"""
    # Check if username already exists
    for existing_user in db.users.values():
        if existing_user["username"] == user.username:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already registered"
            )
        if existing_user["email"] == user.email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
    
    user_id = db.user_id_counter
    db.user_id_counter += 1
    
    now = datetime.now()
    user_dict = {
        "id": user_id,
        "username": user.username,
        "email": user.email,
        "full_name": user.full_name,
        "password": f"hashed_{user.password}",  # In real app, hash the password
        "is_active": True,
        "created_at": now,
        "updated_at": now
    }
    
    db.users[user_id] = user_dict
    return user_dict


@router.put("/{user_id}", response_model=User)
def update_user(user_id: int, user_update: UserUpdate):
    """Update a user"""
    if user_id not in db.users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )
    
    user = db.users[user_id]
    update_data = user_update.model_dump(exclude_unset=True)
    
    # Check for duplicate username/email if being updated
    if "username" in update_data:
        for uid, u in db.users.items():
            if uid != user_id and u["username"] == update_data["username"]:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Username already taken"
                )
    
    if "email" in update_data:
        for uid, u in db.users.items():
            if uid != user_id and u["email"] == update_data["email"]:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already taken"
                )
    
    if "password" in update_data:
        update_data["password"] = f"hashed_{update_data['password']}"
    
    user.update(update_data)
    user["updated_at"] = datetime.now()
    
    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int):
    """Delete a user"""
    if user_id not in db.users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )
    
    # Delete all posts by this user
    posts_to_delete = [pid for pid, post in db.posts.items() if post["user_id"] == user_id]
    for pid in posts_to_delete:
        del db.posts[pid]
    
    del db.users[user_id]
    return None


# Nested routes for user posts
@router.get("/{user_id}/posts", response_model=List[Post], tags=["posts"])
def get_user_posts(user_id: int):
    """Get all posts by a specific user"""
    if user_id not in db.users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )
    
    posts = [post for post in db.posts.values() if post["user_id"] == user_id]
    return posts


@router.post("/{user_id}/posts", response_model=Post, status_code=status.HTTP_201_CREATED, tags=["posts"])
def create_user_post(user_id: int, post: PostCreate):
    """Create a new post for a user"""
    if user_id not in db.users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )
    
    post_id = db.post_id_counter
    db.post_id_counter += 1
    
    now = datetime.now()
    post_dict = {
        "id": post_id,
        "user_id": user_id,
        "title": post.title,
        "content": post.content,
        "created_at": now,
        "updated_at": now
    }
    
    db.posts[post_id] = post_dict
    return post_dict


@router.get("/{user_id}/posts/{post_id}", response_model=Post, tags=["posts"])
def get_user_post(user_id: int, post_id: int):
    """Get a specific post by a user"""
    if user_id not in db.users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )
    
    if post_id not in db.posts:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {post_id} not found"
        )
    
    post = db.posts[post_id]
    if post["user_id"] != user_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post {post_id} does not belong to user {user_id}"
        )
    
    return post


@router.put("/{user_id}/posts/{post_id}", response_model=Post, tags=["posts"])
def update_user_post(user_id: int, post_id: int, post_update: PostUpdate):
    """Update a user's post"""
    if user_id not in db.users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )
    
    if post_id not in db.posts:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {post_id} not found"
        )
    
    post = db.posts[post_id]
    if post["user_id"] != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Post {post_id} does not belong to user {user_id}"
        )
    
    update_data = post_update.model_dump(exclude_unset=True)
    post.update(update_data)
    post["updated_at"] = datetime.now()
    
    return post


@router.delete("/{user_id}/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["posts"])
def delete_user_post(user_id: int, post_id: int):
    """Delete a user's post"""
    if user_id not in db.users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )
    
    if post_id not in db.posts:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {post_id} not found"
        )
    
    post = db.posts[post_id]
    if post["user_id"] != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Post {post_id} does not belong to user {user_id}"
        )
    
    del db.posts[post_id]
    return None
