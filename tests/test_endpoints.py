
def test_root(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Welcome to Blog API"
    }

def test_user(client):
    response = client.get("/users")

    data = response.json()

    assert response.status_code == 200
