
from app.database import SessionLocal
from app.models import User, Post, Comment
from sqlalchemy import select, func
from sqlalchemy.orm import joinedload, selectinload


def create_user(name, email):
    with SessionLocal() as session:

        existing_email = session.scalar(select(User).where(User.email == email))
        if existing_email:
            return None
        user = User(name=name, email=email)
        session.add(user)
        session.commit()
        session.refresh(user)
        return user
        
def list_users():
    with SessionLocal() as session:
        return session.scalars(select(User)).all()

def view_user(email):
    with SessionLocal() as session:
        return session.scalar(select(User).where(User.email == email))
    
def update_user(email, name):
    with SessionLocal() as session:
        existing_user = session.scalar(select(User).where(User.email == email))
        if existing_user:
            existing_user.name = name
            session.commit()
            session.refresh(existing_user)
            return existing_user
        else:
            return None   
        
def delete_user(email):
    with SessionLocal() as session:
        existing_user = session.scalar(select(User).where(User.email == email))
        if existing_user:
            session.delete(existing_user)
            session.commit()
            return existing_user
        else:
            return None   
        
def create_post(user_id, title, content, published):
    with SessionLocal() as session:
        user = session.scalar(select(User).where(User.id == user_id))
        if not user:
            return None
        
        post = Post(title=title, content=content, published=published, user=user)
        session.add(post)
        session.commit()
        session.refresh(post)

        print(post.user.name) # avoid lazy loading
        return post

def list_posts():
        with SessionLocal() as session:
            return session.scalars(select(Post).options(joinedload(Post.user))).all() # joinedload

def view_post(post_id):
        with SessionLocal() as session:
            return session.scalar(select(Post).options(joinedload(Post.user)).where(Post.id == post_id))
        
def update_post(post_id, new_title=None, new_content=None):
        with SessionLocal() as session:
            post = session.scalar(select(Post).where(Post.id == post_id))
            if not post:
                 return None
            if new_title is not None:
                post.title = new_title
            if new_content is not None:
                 post.content = new_content

            session.commit()
            session.refresh(post)
            return post
        
def delete_post(post_id):
    with SessionLocal() as session:
        existing_post = session.scalar(select(Post).where(Post.id == post_id))
        if existing_post:
            session.delete(existing_post)
            session.commit()
            return existing_post
        else:
            return None  
        
def add_comment(user_id, post_id, comment):
    with SessionLocal() as session:
        user = session.scalar(select(User).where(User.id == user_id))
        if not user:
            return None
        post = session.scalar(select(Post).where(Post.id == post_id))
        if not post:
            return None 
        
        comment = Comment(content=comment, user_id=user_id, post_id=post_id)
        session.add(comment)
        session.commit()
        session.refresh(comment)

        return comment

def view_comments(post_id):
    with SessionLocal() as session: 
        return session.scalars(select(Comment).where(Comment.post_id == post_id).options(joinedload(Comment.user), joinedload(Comment.post))).all()

def upodate_comment(comment_id, new_comment):
    with SessionLocal() as session:
        comment = session.scalar(select(Comment).where(Comment.id == comment_id)) 
        if not comment:
            return None

        comment.content = new_comment
        session.commit()
        session.refresh(comment)

        return comment

def delete_comment(comment_id):
    with SessionLocal() as session:
        existing_comment = session.scalar(select(Comment).where(Comment.id == comment_id))
        if existing_comment:
            session.delete(existing_comment)
            session.commit()
            return existing_comment
        else:
            return None  
        
def show_posts_by_user(user_id):
    with SessionLocal() as session:
        return session.scalars(select(Post).where(Post.user_id == user_id).options(joinedload(Post.user))).all()
    
def show_comments_of_post(post_id):
    with SessionLocal() as session:
        return session.scalars(select(Comment).where(Comment.post_id == post_id).options(joinedload(Comment.user), joinedload(Comment.post))).all()

def count_posts_written_by_every_user():
        with SessionLocal() as session:
            return session.execute(select(User.name, func.count(Post.id)).outerjoin(Post).group_by(User.name)).all()