from datetime import datetime, timedelta
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from base import Base
from main import app
from user.models import User
from post.models import Post, Comment

SQLALCHEMY_DATABASE_URL = "sqlite:///./db.sqlite3"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

client = TestClient(app)


@pytest.fixture(scope="module", autouse=True)
def setup_and_teardown():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def create_test_user():
    db = TestingSessionLocal()
    user = db.query(User).filter(User.email == "test@example.com").first()
    if not user:
        user = User(email="test@example.com", hashed_password="test_password_hashed")
        db.add(user)
        db.commit()
    db.close()

    response = client.post(
        "/user/login", json={"email": "test@example.com", "password": "test_password"}
    )
    token = response.json().get("access_token")
    return user, token


def test_create_user(create_test_user):
    response = client.post(
        "/user/signup", json={"email": "newuser@example.com", "password": "newpassword"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data or data.get("detail") == "Email already in use"


def test_login_user(create_test_user):
    _, token = create_test_user
    response = client.post(
        "/user/login", json={"email": "test@example.com", "password": "test_password"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data


def test_create_post(create_test_user):
    _, token = create_test_user

    response = client.post(
        "/posts/",
        json={"title": "Test Title", "content": "Test Content", "owner_id": 1},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200, response.json()
    data = response.json()
    assert data["title"] == "Test Title"
    assert data["content"] == "Test Content"

    db = TestingSessionLocal()
    post = db.query(Post).filter(Post.title == "Test Title").first()
    if post:
        db.delete(post)
        db.commit()
    db.close()


def test_get_comments_daily_breakdown(create_test_user):
    user, token = create_test_user

    today_date = datetime.now().strftime("%Y-%m-%d")
    next_day_date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")

    db = TestingSessionLocal()
    post = Post(title="Test Post", content="Test Content", owner_id=user.id)
    db.add(post)

    comment_good = Comment(
        content="Good comment",
        post_id=post.id,
        created_at=datetime.now(),
        blocked=False,
    )
    db.add(comment_good)

    comment_bad = Comment(
        content="Bad comment with bad words",
        post_id=post.id,
        created_at=datetime.now(),
        blocked=True,
    )
    db.add(comment_bad)

    db.commit()

    comments = db.query(Comment).all()
    assert len(comments) >= 2

    response = client.get(
        "/comments-daily-breakdown",
        params={"date_from": today_date, "date_to": next_day_date},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    data = response.json()
    assert "total_comments" in data[0]
    assert "blocked_comments" in data[0]
    assert data[0]["blocked_comments"] >= 1

    comment_good = db.query(Comment).filter(Comment.content == "Good comment").first()
    if comment_good:
        db.delete(comment_good)

    comment_bad = (
        db.query(Comment)
        .filter(Comment.content == "Bad comment with bad words")
        .first()
    )
    if comment_bad:
        db.delete(comment_bad)

    post = db.query(Post).filter(Post.title == "Test Post").first()
    if post:
        db.delete(post)

    db.commit()
    db.close()


def test_protected_route(create_test_user):
    _, token = create_test_user

    response = client.get("/posts/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200


def test_protected_route_without_login():
    response = client.get("/posts/")
    assert response.status_code == 403
