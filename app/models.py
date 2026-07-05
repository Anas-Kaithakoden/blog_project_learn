from app.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Boolean, Text, ForeignKey, DateTime
from datetime import datetime, timezone

class User(Base):
    __tablename__ = "users"

    id:Mapped[int] = mapped_column(primary_key=True)
    name:Mapped[str] = mapped_column(String(225), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True)
    phone: Mapped[str] = mapped_column(String(20), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda :datetime.now(timezone.utc))
    posts: Mapped[list["Post"]] = relationship( back_populates="user")
    comments: Mapped[list["Comment"]] = relationship(back_populates="user")


class Post(Base):
    __tablename__ = "posts"

    id:Mapped[int] = mapped_column(primary_key=True)
    title:Mapped[str] = mapped_column(Text, nullable=False)
    content:Mapped[str] = mapped_column(Text)
    published:Mapped[bool] = mapped_column(Boolean, default=False)
    category: Mapped[str] = mapped_column(String(100),nullable=True)
    created_at:Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda :datetime.now(timezone.utc))
    user_id:Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    user: Mapped["User"] = relationship( back_populates="posts")
    comments: Mapped[list["Comment"]] = relationship(back_populates="post")
    


class Comment(Base):
    __tablename__ = "comments"

    id:Mapped[int] = mapped_column(primary_key=True)
    content:Mapped[str] = mapped_column(Text)
    created_at:Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda :datetime.now(timezone.utc))
    post_id:Mapped[int] = mapped_column(ForeignKey("posts.id"), nullable=False)
    user_id:Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    user: Mapped["User"] = relationship( back_populates="comments")
    post: Mapped["Post"] = relationship( back_populates="comments")