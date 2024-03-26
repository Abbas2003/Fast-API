from fastapi.testclient import TestClient
from hero_api.main import app

def test_root_path():
    client = TestClient(app=app)
    response = client.get("/")
    assert response.status == 200

def test_root_path_content():
    client = TestClient(app=app)
    response = client.get("/")
    assert response.json() == {"Hello": "Fast API"}