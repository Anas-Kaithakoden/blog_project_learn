
def test_create_post_with_invalid_token(client, post_payload):
    response = client.post(
        "/posts",
        json=post_payload,
        headers={
            "Authorization": "Bearer invalid_token"
        }
    )

    assert response.status_code == 401


def test_login_wrong_password(client, user_payload, auth_headers):
    user_payload_copy = user_payload.copy()
    user_payload_copy["password"] = "12345kk"
    response = client.post(
        "/login",
        json=user_payload_copy
    )

    assert response.status_code == 401

def test_login_unknown_user(client, user_payload):
    user_payload_copy = user_payload.copy()
    user_payload_copy["username"] = "unknown_user"
    response = client.post(
        "/login",
        json=user_payload_copy
    )

    assert response.status_code == 401

from app.security import create_access_token
from datetime import timedelta

def test_create_post_after_token_expire(client, user, post_payload):
    expired_token = create_access_token(
        data={"sub": str(user["id"])},
        expires_delta=timedelta(minutes=-1)
    )

    response = client.post(f"/posts", json=post_payload,headers={
            "Authorization": f"Bearer {expired_token}"
        },)

    assert response.status_code == 401

def test_delete_post_of_user(client, auth_headers, post):
    # Create a new user
    response = client.delete(f"/posts/{post['id']}", headers=auth_headers)

    assert response.status_code == 204

def test_delete_post_of_another_user(client, another_post, auth_headers,):
    # Create a new user
    response = client.delete(f"/posts/{another_post['id']}", headers=auth_headers)

    assert response.status_code == 404


    