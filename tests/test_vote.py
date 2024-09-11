from app.models import Vote
import pytest


@pytest.fixture
def test_vote(test_user, test_posts, session):
    vote = Vote(post_id=test_posts[0].id, user_id=test_user.get('id'))
    session.add(vote)
    session.commit()
    return vote


def test_user_can_vote_post_twice(authorized_client, test_vote, test_user, test_posts):
    res = authorized_client.post("/vote", json={'post_id': test_posts[0].id, 'dir': 1})
    assert res.status_code == 409


def test_user_can_vote_does_not_exist_post(authorized_client, test_user, test_posts):
    res = authorized_client.post("/vote", json={'post_id': test_posts[1].id, 'dir': 0})
    assert res.status_code == 404


def test_user_can_vote_post_unauthenticated_user(client, test_user, test_posts):
    res = client.post("/vote", json={'post_id': test_posts[0].id, 'dir': 1})
    assert res.status_code == 401


def test_user_can_vote_new_post(authorized_client, test_vote, test_posts):
    res = authorized_client.post("/vote", json={'post_id': test_posts[1].id, 'dir': 1})
    assert res.status_code == 201
    assert res.json().get('message') == "vote added"


def test_user_can_vote_remove_post_vote(authorized_client, test_vote, test_posts):
    res = authorized_client.post("/vote", json={'post_id': test_posts[0].id, 'dir': 0})
    assert res.status_code == 201
    assert res.json().get('message') == "vote deleted."
