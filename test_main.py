from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]

def test_add():
    response = client.post("/add", json={"a": 5, "b": 3})
    assert response.status_code == 200
    assert response.json() == {"result": 8.0}

    response = client.post("/add", json={"a": -5, "b": 3})
    assert response.status_code == 200
    assert response.json() == {"result": -2.0}

    response = client.post("/add", json={"a": 0.1, "b": 0.2})
    assert response.status_code == 200
    # Floating point arithmetic check
    assert abs(response.json()["result"] - 0.3) < 0.000001

def test_sub():
    response = client.post("/sub", json={"a": 10, "b": 4})
    assert response.status_code == 200
    assert response.json() == {"result": 6.0}

    response = client.post("/sub", json={"a": 5, "b": 10})
    assert response.status_code == 200
    assert response.json() == {"result": -5.0}

def test_mul():
    response = client.post("/mul", json={"a": 6, "b": 7})
    assert response.status_code == 200
    assert response.json() == {"result": 42.0}

    response = client.post("/mul", json={"a": 5, "b": 0})
    assert response.status_code == 200
    assert response.json() == {"result": 0.0}

def test_div():
    response = client.post("/div", json={"a": 10, "b": 2})
    assert response.status_code == 200
    assert response.json() == {"result": 5.0}

    response = client.post("/div", json={"a": 5, "b": 2})
    assert response.status_code == 200
    assert response.json() == {"result": 2.5}

def test_div_by_zero():
    response = client.post("/div", json={"a": 5, "b": 0})
    assert response.status_code == 400
    assert response.json() == {"detail": "Division by zero"}

def test_invalid_input():
    response = client.post("/add", json={"a": "invalid", "b": 3})
    assert response.status_code == 422  # Unprocessable Entity
