from pydantic import BaseModel
from datetime import datetime


class CommentCreate(BaseModel):
    content: str


class CommentUpdate(BaseModel):
    content: str
    blocked: bool


class CommentInDB(CommentUpdate):
    id: int
    post_id: int
    created_at: datetime

    class Config:
        orm_mode = True


class PostCreate(BaseModel):
    title: str
    content: str
    owner_id: int
    auto_reply_enabled: bool = False
    auto_reply_delay: int = 5


class PostUpdate(BaseModel):
    title: str
    content: str
    auto_reply_enabled: bool = False
    auto_reply_delay: int = 5


class PostInDB(PostUpdate):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class CommentAnalytics(BaseModel):
    date: str
    total_comments: int
    blocked_comments: int


class AutoReplySettingsUpdate(BaseModel):
    delay: int
    enabled: bool
