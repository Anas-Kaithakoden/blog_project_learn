from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel, Field, EmailStr
from app import crud, security
from typing import Optional, Email
from datetime import datetime
from sqlalchemy.orm import Session
from dependencies import get_db, get_current_user
from datetime import timedelta
from app.models import User

app = FastAPI(title="Blog API")

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class UserCreate(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None
    password: str

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

class UserBasic(BaseModel):
    id: int
    name: str

    model_config = {
        "from_attributes": True
    }

class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    published: bool
    created_at: datetime
    category: str | None
    user_id: int

    user: UserBasic

    model_config = {
        "from_attributes": True
    }


@app.get("/")
def home():
    return {
        "message": "Welcome to Blog API"
    }

@app.post("/login")
def login(request= LoginRequest, db: Session = Depends(get_db)):
    user = crud.authenticate_user(email=request.email, password=request.password, session=db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect Email or password")
    
    token = security.create_access_token(data={"sub":str(user.id)}, expires_delta=timedelta(minutes=45))

    return {
        "access_token": token,
        "token_type": "bearer"
    }


@app.post("/users")
def create_user(user: UserCreate, db: Session = Depends(get_db)):

    created_user = crud.create_user(name=user.name, email=user.email, password=user.password, phone=user.phone, session=db)

    if not created_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already exists"
        )
    return created_user

@app.get("/users")
def list_users(db: Session = Depends(get_db)):
    return crud.list_users(session=db)

@app.get("/users/{user_id}")
def view_user(user_id: int,  db: Session = Depends(get_db)):
    user = crud.view_user(user_id, session=db)
    
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    return user

@app.put("/users")
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    updated_user = crud.update_user(current_user.id, user.name, session=db)

    if not updated_user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    return updated_user

@app.delete("/users")
def delete_user(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user = crud.delete_user(current_user.id, session=db)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    return user  


# posts

@app.post("/posts")
def create_post(post: PostCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):

    created_post = crud.create_post(current_user.id , post.title, post.content, post.published, session=db)

    if not created_post:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    
    return created_post

@app.get("/posts")
def list_posts(db: Session = Depends(get_db)):
    return crud.list_posts(session=db)

@app.get("/posts/latest")
def show_latest_posts(page:int = 1, per_page:int = 5, db: Session = Depends(get_db)):
    return crud.show_latest_posts(page, per_page, session=db)

@app.get("/posts/{post_id}")
def view_post(post_id: int, db: Session = Depends(get_db)):
    post = crud.view_post(post_id, session=db)
    
    if not post:
        raise HTTPException(
            status_code=404,
            detail="Post not found"
        )
    return post

@app.patch("/posts/{post_id}")
def update_post(post_id: int, post: PostUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    updated_post = crud.update_post(current_user.id, post_id,  post.title, post.content, session=db)

    if not updated_post:
        raise HTTPException(
            status_code=404,
            detail="Post not found or no permission to update"
        )
    return updated_post

@app.delete("/posts/{post_id}")
def delete_post(post_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    post = crud.delete_post(current_user.id, post_id, session=db)

    if not post:
        raise HTTPException(
            status_code=404,
            detail="Post not found or no permission to delete"
        )
    return post 

# comments
@app.post("/users/posts/{post_id}/comments")
def add_comment(post_id: int, comment: CommentCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    created_comment = crud.add_comment(current_user.id, post_id, comment.comment, session=db)

    if not created_comment:
        raise HTTPException(
            status_code=404,
            detail="Post not found"
        )
    return created_comment 

@app.get("/posts/{post_id}/comments") # get comments of a post
def view_comments(post_id: int, db: Session = Depends(get_db)):
    post = crud.view_comments(post_id, session=db)
    
    if not post:
        raise HTTPException(
            status_code=404,
            detail="Post not found"
        )
    return post

@app.patch("/comments/{comment_id}")
def update_comment(comment_id: int, comment: CommentUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    updated_comment = crud.update_comment(current_user.id, comment_id, comment.comment, session=db)

    if not updated_comment:
        raise HTTPException(
            status_code=404,
            detail="Comment not found or no permission to update"
        )
    return updated_comment

@app.delete("/comments/{comment_id}")
def delete_comment(comment_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    comment = crud.delete_comment(current_user.id, comment_id, session=db)

    if not comment:
        raise HTTPException(
            status_code=404,
            detail="Comment not found or no permission to delete"
        )
    return comment 

# special

@app.get("/users/{user_id}/posts", response_model=list[PostResponse])
def show_posts_by_user(user_id: int, db: Session = Depends(get_db)):
    return crud.show_posts_by_user(user_id, session=db)

@app.get("/analytics/users/posts")
def count_posts_written_by_every_user(db: Session = Depends(get_db)):
    return crud.count_posts_written_by_every_user(session=db)

@app.get("/analytics/posts/comments")
def count_comments_for_every_post(db: Session = Depends(get_db)):
    return crud.count_comments_for_every_post(session=db)

