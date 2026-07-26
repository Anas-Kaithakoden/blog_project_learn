from app.models import Post

def test_create_post_success(client,post_payload, auth_headers, db_session):
    responce = client.post("/posts", json=post_payload, headers=auth_headers,)

    assert responce.status_code == 201
    data = responce.json()

    assert data["title"] == post_payload["title"]

    post = db_session.query(Post).filter_by(
        title=post_payload["title"]
    ).first()

    assert post is not None

def test_create_post_without_token(client, post_payload):
    response = client.post("/posts", json=post_payload)

    assert response.status_code == 401


def test_create_post_without_title(
    client,
    auth_headers,
):
    response = client.post(
        "/posts",
        json={
            "content": "Only content"
        },
        headers=auth_headers,
    )

    assert response.status_code == 422

def test_delete_post_success(client, auth_headers, post, db_session):
    response = client.delete(
        f"/posts/{post['id']}",
        headers=auth_headers,
    )

    assert response.status_code == 204

    assert (db_session.query(Post).where(Post.id == post['id']).first() is None )
