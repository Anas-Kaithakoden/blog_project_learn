from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from app import crud
from typing import Optional

app = FastAPI(title="Blog API")

class UserCreate(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None

class UserUpdate(BaseModel):
    name: str

class PostCreate(BaseModel):
    title: str = Field(min_length=3)
    content: str = Field(min_length=3)
    published: bool

class PostUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=3)
    content: Optional[str] = Field(default=None, min_length=3)

class CommentCreate(BaseModel):
    comment: str

class CommentUpdate(BaseModel):
    comment: str

@app.get("/")
def home():
    return {
        "message": "Welcome to Blog API"
    }

@app.post("/users")
def create_user(user: UserCreate):

    created_user = crud.create_user(user.name,user.email)

    if not created_user:
        raise HTTPException(
            status_code=409,
            detail="Email already exists"
        )
    return created_user

@app.get("/users")
def list_users():
    return crud.list_users()

@app.get("/users/{user_id}")
def view_user(user_id: int):
    user = crud.view_user(user_id)
    
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    return user

@app.put("/users/{user_id}")
def update_user(user_id: int, user: UserUpdate):
    updated_user = crud.update_user(user_id, user.name)

    if not updated_user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    return updated_user

@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    user = crud.delete_user(user_id)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    return user  


# posts

@app.post("/posts/{user_id}")
def create_post(user_id: int, post: PostCreate):

    created_post = crud.create_post(user_id , post.title, post.content, post.published)

    if not created_post:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    
    return created_post

@app.get("/posts")
def list_posts():
    return crud.list_posts()

@app.get("/posts/{post_id}")
def view_post(post_id: int):
    post = crud.view_post(post_id)
    
    if not post:
        raise HTTPException(
            status_code=404,
            detail="Post not found"
        )
    return post

@app.patch("/posts/{post_id}")
def update_post(post_id: int, post: PostUpdate):
    updated_post = crud.update_post(post_id, post.title, post.content)

    if not updated_post:
        raise HTTPException(
            status_code=404,
            detail="Post not found"
        )
    return updated_post

@app.delete("/posts/{post_id}")
def delete_post(post_id: int):
    post = crud.delete_post(post_id)

    if not post:
        raise HTTPException(
            status_code=404,
            detail="Post not found"
        )
    return post 

# comments
@app.post("/users/{user_id}/posts/{post_id}/comments")
def add_comment(user_id: int, post_id: int, comment: CommentCreate):
    created_comment = crud.add_comment(user_id, post_id, comment.comment)

    if not created_comment:
        raise HTTPException(
            status_code=404,
            detail="Post not found"
        )
    return created_comment 

@app.get("/comments")
def list_comments():
    return crud.list_comments()

@app.get("/posts/{post_id}/comments") # get comments of a post
def view_comments(post_id: int):
    post = crud.view_comments(post_id)
    
    if not post:
        raise HTTPException(
            status_code=404,
            detail="Post not found"
        )
    return post

@app.patch("/comments/{comment_id}")
def update_comment(comment_id: int, comment: CommentUpdate):
    updated_comment = crud.update_comment(comment_id, comment.comment)

    if not updated_comment:
        raise HTTPException(
            status_code=404,
            detail="Comment not found"
        )
    return updated_comment

@app.delete("/comments/{comment_id}")
def delete_comment(comment_id: int):
    comment = crud.delete_comment(comment_id)

    if not comment:
        raise HTTPException(
            status_code=404,
            detail="Comment not found"
        )
    return comment 