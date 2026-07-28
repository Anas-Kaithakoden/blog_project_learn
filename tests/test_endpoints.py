
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

# mocks--------------

# def summarize(text):
#     return openai.chat.completions.create(...)

# with patch("app.ai.summarize") as mock_summary:

#     mock_summary.return_value = {
#         "summary": "FastAPI is great."
#     }

#     response = client.post(...)