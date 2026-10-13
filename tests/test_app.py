import pytest

from app import app, clients


@pytest.fixture
def client():
    app.config["TESTING"] = True

    with app.test_client() as test_client:
        yield test_client


@pytest.fixture(autouse=True)
def clear_clients():
    clients.clear()


def test_home(client):
    response = client.get("/")

    assert response.status_code == 200

    data = response.get_json()

    assert data["application"] == "ACEest Fitness & Gym"
    assert data["status"] == "running"


def test_health(client):
    response = client.get("/health")

    assert response.status_code == 200

    data = response.get_json()

    assert data["status"] == "healthy"


def test_programs(client):
    response = client.get("/api/programs")

    assert response.status_code == 200

    data = response.get_json()

    assert "Fat Loss" in data
    assert "Muscle Gain" in data
    assert "Beginner" in data


def test_get_clients(client):
    response = client.get("/api/clients")

    assert response.status_code == 200
    assert response.get_json() == []


def test_add_client(client):
    response = client.post(
        "/api/clients",
        json={
            "name": "Test User",
            "age": 25,
            "weight": 70,
            "program": "Muscle Gain"
        }
    )

    assert response.status_code == 201

    data = response.get_json()

    assert data["message"] == "Client added successfully"
    assert data["client"]["name"] == "Test User"
    assert data["client"]["program"] == "Muscle Gain"


def test_invalid_program(client):
    response = client.post(
        "/api/clients",
        json={
            "name": "Test User",
            "age": 25,
            "weight": 70,
            "program": "Invalid Program"
        }
    )

    assert response.status_code == 400

    data = response.get_json()

    assert data["error"] == "Invalid fitness program"


def test_missing_field(client):
    response = client.post(
        "/api/clients",
        json={
            "name": "Test User"
        }
    )

    assert response.status_code == 400

    data = response.get_json()

    assert data["error"] == "Missing field: age"


def test_empty_request_body(client):
    response = client.post(
        "/api/clients",
        json={}
    )

    assert response.status_code == 400
