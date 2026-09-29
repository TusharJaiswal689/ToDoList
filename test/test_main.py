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
