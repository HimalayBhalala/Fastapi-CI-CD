import pytest
from app.oauth import create_access_token
from app.models import Post
from .database import client


@pytest.fixture
def test_user(client):
    user_data = {
        "email": "test@gmail.com",
        "password": "test"
    }

    res = client.post('/users', json=user_data)
    assert res.status_code == 201, "User creation failed"
    new_user = res.json()
    new_user['password'] = user_data["password"]
    assert new_user['email'] == user_data['email'], "User email does not match"
    return new_user


@pytest.fixture
def test_user1(client):
    user_data = {
        "email": "test1@gmail.com",
        "password": "test1"
    }
    res = client.post('/users', json=user_data)
    assert res.status_code == 201, "User creation failed"
    new_user = res.json()
    new_user['password'] = user_data["password"]
    assert new_user['email'] == user_data['email'], "User email does not match"
    return new_user


@pytest.fixture
def test_token(test_user):
    return create_access_token({"user_id": test_user['id']})


@pytest.fixture
def authorized_client(client, test_token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {test_token}"
    }
    return client


@pytest.fixture
def test_posts(client, session, test_user, test_user1):
    post_data = [
        {
            "id": 1001,
            "title": "First Title",
            "content": "This is a very good first post",
            "owner_id": test_user.get("id")
        },
        {
            "id": 1002,
            "title": "Second Title",
            "content": "This is a very famous second post",
            "owner_id": test_user.get("id")
        },
        {
            "id": 1003,
            "title": "Third Title",
            "content": "This is a very shown post",
            "owner_id": test_user.get("id")
        },
        {
            "id": 1004,
            "title": "Four Title",
            "content": "This is a very good post",
            "owner_id": test_user1.get("id")
        }
    ]

    def create_user_post(post):
        return Post(**post)

    post_map = map(create_user_post, post_data)
    posts = list(post_map)
    session.add_all(posts)
    session.commit()
    all_posts = session.query(Post).all()
    return all_posts
