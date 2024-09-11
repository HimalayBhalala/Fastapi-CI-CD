from app import schemas
from jose import jwt
from app.config import settings
import pytest


def test_hello(client, session):
    res = client.get("/")
    assert res.json().get('message') == "Hello World"
    assert res.status_code == 200


def test_create_user(client):
    res = client.post("/users", json={"email": "test@gmail.com", "password": "test"})
    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "test@gmail.com"
    assert res.status_code == 201


def test_user_login(test_user, client):
    res = client.post("/login", data={"username": test_user["email"], "password": test_user["password"]})
    token_data = schemas.Token(**res.json())
    token_decode = jwt.decode(token_data.access_token, settings.secret_key, settings.algorithm)
    assert test_user['id'] == token_decode.get('user_id')
    assert token_data.access_token == res.json().get('access_token')
    assert token_data.token_type == "bearer"
    assert res.status_code == 200


@pytest.mark.parametrize("email, password, status_code", [
    ("wrongemail@gmail.com", "password123", 403),
    ("test@gmail.com", "wrong-password", 403),
    (None, "password", 422),
    ("test@gmail.com", None, 422)
])
def test_user_failed_login(client, email, password, status_code):
    res = client.post("/login", data={"username": email, "password": password})
    assert res.status_code == status_code


def test_user_get(test_user, client):
    res = client.get(f"/users/{test_user.get('id')}")
    assert res.status_code == 200
    assert res.json().get('email') == "test@gmail.com"
