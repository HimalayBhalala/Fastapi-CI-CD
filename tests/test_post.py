from app import schemas
import pytest


def test_get_all_post(authorized_client, test_posts):
    res = authorized_client.get("/posts/")

    def validate(post):
        return schemas.PostOut(**post)

    post_map = map(validate, res.json())

    assert len(list(post_map)) == len(test_posts)
    assert res.status_code == 200


def test_get_all_post_unauthorized_user(client, test_posts):
    res = client.get("/posts/")
    assert res.status_code == 401


def test_get_one_post_unauthorized_user(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401


def test_get_one_post_authorized_user(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    post = schemas.PostOut(**res.json())
    assert post.title == "First Title"
    assert res.status_code == 200


def test_post_not_found_authorized(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{17278}")
    assert res.status_code == 404


@pytest.mark.parametrize("title, content, published", [
    ("awesome post", "This is a very good post", True),
    ("nice post", "This is a very nice post", False),
    ("famous post", "This is a very famous post", True)
])
def test_create_post(authorized_client, test_user, test_posts, title, content, published):
    res = authorized_client.post("/posts", json={"title": title, "content": content, "published": published})
    new_post = schemas.GetPost(**res.json())
    assert new_post.title == title
    assert new_post.content == content
    assert new_post.published == published
    assert new_post.owner_id == test_user.get('id')
    assert res.status_code == 201


def test_update_post(authorized_client, test_user, test_posts):
    res = authorized_client.put(
        f"/posts/{test_posts[1].id}",
        json={"title": "Abc title", "content": "This award goes to abc", "published": True}
    )
    assert res.status_code == 200
    assert res.json().get("title") == "Abc title"
    assert res.json().get("owner_id") == test_user.get("id")


def test_update_post_unauthorized_user(client, test_posts):
    res = client.put(
        f'/posts/{test_posts[1].id}',
        json={"title": "first title", "content": "This is a nice popular post", "published": True}
    )
    assert res.status_code == 401


def test_update_other_authenticated_user(authorized_client, test_posts):
    res = authorized_client.put(
        f'/posts/{test_posts[3].id}',
        json={"title": "first title", "content": "This is a nice popular post", "published": True}
    )
    assert res.status_code == 403


def test_delete_post(authorized_client, test_posts):
    res = authorized_client.delete(f'/posts/{test_posts[0].id}')
    assert res.status_code == 204


def test_delete_post_unauthenticated_user(client, test_posts):
    res = client.delete(f'/posts/{test_posts[0].id}')
    assert res.status_code == 401


def test_delete_other_authenticated_user(authorized_client, test_posts):
    res = authorized_client.delete(f'/posts/{test_posts[3].id}')
    assert res.status_code == 403
