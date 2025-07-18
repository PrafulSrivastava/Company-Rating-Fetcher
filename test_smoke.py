from fastapi.testclient import TestClient
import pytest

from app import app

client = TestClient(app)

def test_ratings_endpoint():
    response = client.get("/ratings?company=Google")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "ratings" in data
    assert isinstance(data["ratings"], list)
    assert any(isinstance(item, dict) and 'source' in item for item in data["ratings"])
