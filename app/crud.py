
from app.database import SessionLocal
from app.models import User, Post, Comment
from sqlalchemy import select, func
from sqlalchemy.orm import joinedload, selectinload, Session
from app.security import hash_password, verify_password


def authenticate_user(email: str, password: str, session: Session):
    existing_user = session.scalar(select(User).where(User.email == email))
    if not existing_user:
        return None
    
    verified = verify_password(password, existing_user.hashed_password)
    if not verified:
        return None
    return existing_user


def create_user(name, email, password, phone, session: Session):
    existing_user = session.scalar(select(User).where(User.email == email))
    if existing_user:
        return None
    hashed_password = hash_password(password)
    user = User(name=name, email=email, phone=phone, hashed_password=hashed_password)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user
        
def list_users(session: Session):
    return session.scalars(select(User)).all()

def view_user(id, session: Session):
    return session.scalar(select(User).where(User.id == id))
    
def update_user(id, name, session: Session):
    existing_user = session.scalar(select(User).where(User.id == id))
    if existing_user:
        existing_user.name = name
        session.commit()
        session.refresh(existing_user)
        return existing_user
    else:
        return None   
        
def delete_user(id, session: Session):
    existing_user = session.scalar(select(User).where(User.id == id))
    if existing_user:
        session.delete(existing_user)
        session.commit()
        return existing_user
    else:
        return None   
        
def create_post(user_id, title, content, published, session: Session):
    user = session.scalar(select(User).where(User.id == user_id))
    if not user:
        return None
    
    post = Post(title=title, content=content, published=published, user=user)
    session.add(post)
    session.commit()
    session.refresh(post)

    print(post.user.name) # avoid lazy loading
    return post

def list_posts(session: Session):
    return session.scalars(select(Post).options(joinedload(Post.user))).all() # joinedload

def view_post(post_id, session: Session):
    return session.scalar(select(Post).options(joinedload(Post.user)).where(Post.id == post_id))
        
def update_post(post_id, new_title, new_content, session: Session):
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
        
def delete_post(user_id, post_id, session: Session):
    existing_post = session.scalar(select(Post).where(Post.id == post_id, Post.user_id == user_id))
    if existing_post:
        session.delete(existing_post)
        session.commit()
        return existing_post
    else:
        return None  
        
def add_comment(user_id, post_id, comment, session: Session):
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

def view_comments(post_id, session: Session):
    return session.scalars(select(Comment).where(Comment.post_id == post_id).options(joinedload(Comment.user), joinedload(Comment.post))).all()

def update_comment(user_id, comment_id, new_comment, session: Session):
    comment = session.scalar(select(Comment).where(Comment.id == comment_id, Comment.user_id == user_id)) 
    if not comment:
         return None

    comment.content = new_comment
    session.commit()
    session.refresh(comment)

    return comment

def delete_comment(user_id , comment_id, session: Session):
    existing_comment = session.scalar(select(Comment).where(Comment.id == comment_id, Comment.user_id == user_id))
    if existing_comment:
        session.delete(existing_comment)
        session.commit()
        return existing_comment
    else:
        return None  
    
def show_posts_by_user(user_id, session: Session):
    return session.scalars(select(Post).where(Post.user_id == user_id).options(joinedload(Post.user))).all()
    
def show_comments_of_post(post_id, session: Session):
    return session.scalars(select(Comment).where(Comment.post_id == post_id).options(joinedload(Comment.user), joinedload(Comment.post))).all()

def count_posts_written_by_every_user(session: Session):
    result = session.execute(select(User.name, func.count(Post.id).label("post_count")).outerjoin(Post).group_by(User.name)).all()
    return [
        {
            "name": row.name,
            "post_count": row.post_count
        }
        for row in result
    ]
        
def count_comments_for_every_post(session: Session):
    result =  session.execute(select(Post.title, func.count(Comment.id).label("comment_count")).outerjoin(Comment).group_by(Post.title)).all()
    return [
        {
            "post": row.title,
            "comment_count": row.comment_count
        }
        for row in result
    ]
    
def show_latest_posts(page, per_page=5, session: Session=None):
    return session.scalars(select(Post).order_by(Post.created_at.desc()).offset((page-1)*per_page).limit(per_page)).all()
    


from random import choice, randint
def seed_database():
    with SessionLocal() as session:

        users = []

        names = [
            "Anas", "Alice", "John", "Sarah", "David",
            "Emma", "Michael", "Sophia", "James", "Olivia"
        ]

        for name in names:
            user = User(
                name=name,
                email = f"{name.lower()}{randint(1000,9999)}@example.com"
            )
            session.add(user)
            users.append(user)

        session.commit()

        posts = []

        titles = [
            "Learning SQLAlchemy",
            "FastAPI Basics",
            "Python Tips",
            "Docker Guide",
            "Linux Commands",
            "REST APIs",
            "ORM vs Raw SQL",
            "Database Indexes",
            "JWT Authentication",
            "Testing with Pytest",
        ]

        contents = [
            "This is my first blog post.",
            "Today I learned something new.",
            "Python is fun to use.",
            "Docker makes deployment easier.",
            "SQLAlchemy ORM is powerful.",
            "FastAPI is extremely fast.",
            "Always write clean code.",
            "Indexes improve query performance.",
            "Authentication is important.",
            "Testing saves time.",
        ]

        for i in range(10):
            post = Post(
                title=titles[i],
                content=contents[i],
                published=choice([True, False]),
                user_id=choice(users).id,
            )
            session.add(post)
            posts.append(post)

        session.commit()

        comments = [
            "Great post!",
            "Very helpful.",
            "I learned a lot.",
            "Thanks for sharing.",
            "Excellent explanation.",
            "Can you write Part 2?",
            "Nice article.",
            "This solved my problem.",
            "Well written.",
            "Awesome!",
            "Interesting.",
            "Good work.",
            "Loved this.",
            "Keep posting.",
            "Very informative.",
        ]

        for _ in range(30):
            comment = Comment(
                content=choice(comments),
                user_id=choice(users).id,
                post_id=choice(posts).id,
            )
            session.add(comment)

        session.commit()

        print("Database seeded successfully!")
        