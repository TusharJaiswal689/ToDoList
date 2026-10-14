from fastapi.testclient import TestClient
from fastapi import status
import sys
from pathlib import Path

SRC_DIR = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC_DIR))

import main

client = TestClient(main.app)

def test_health_check():
    response = client.get("/healthy")
    assert response.status_code==status.HTTP_200_OK
    assert response.json()== {"status": "Healthy"}

def test_logout_clears_access_token_cookie():
    client.cookies.set("access_token", "test-token", path="/")

    response = client.post("/auth/logout")

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert "access_token=" in response.headers["set-cookie"]
    assert "Max-Age=0" in response.headers["set-cookie"]
