import pytest
from fastapi.testclient import TestClient
import json
from main import app

client = TestClient(app)

def test_home():
    response = client.get("/")
    assert response.status_code == 200
    # assert response.text == "Welcome to Circle"

