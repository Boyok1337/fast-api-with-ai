from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime
from base import Base
from sqlalchemy.orm import relationship


class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="posts")
    blocked = Column(Boolean, default=False)
    auto_reply_enabled = Column(Boolean, default=False)
    auto_reply_delay = Column(Integer, default=5)  # delay in minutes
    comments = relationship("Comment", order_by="Comment.id", back_populates="post")


class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True, index=True)
    content = Column(String)
    post_id = Column(Integer, ForeignKey("posts.id"))
    post = relationship("Post", back_populates="comments")
    blocked = Column(Boolean, default=False)
    created_at = Column(DateTime)
    parent_id = Column(Integer, ForeignKey("comments.id"), nullable=True)


from user.models import User

User.posts = relationship("Post", order_by=Post.id, back_populates="owner")
Post.comments = relationship("Comment", order_by=Comment.id, back_populates="post")
