import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

# --- GET /activities ---
def test_get_activities():
    # Arrange: (nothing needed, uses in-memory DB)
    # Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

# --- POST /activities/{activity_name}/signup ---
def test_signup_success():
    # Arrange
    activity = "Chess Club"
    email = "testuser@mergington.edu"
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 200
    assert f"Signed up {email}" in response.json()["message"]
    # Cleanup
    client.delete(f"/activities/{activity}/participants?email={email}")

def test_signup_duplicate():
    # Arrange
    activity = "Chess Club"
    email = "duplicate@mergington.edu"
    client.post(f"/activities/{activity}/signup?email={email}")
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]
    # Cleanup
    client.delete(f"/activities/{activity}/participants?email={email}")

def test_signup_activity_not_found():
    # Arrange
    activity = "Nonexistent Club"
    email = "nouser@mergington.edu"
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]

# --- DELETE /activities/{activity_name}/participants ---
def test_remove_participant_success():
    # Arrange
    activity = "Chess Club"
    email = "removeuser@mergington.edu"
    client.post(f"/activities/{activity}/signup?email={email}")
    # Act
    response = client.delete(f"/activities/{activity}/participants?email={email}")
    # Assert
    assert response.status_code == 200
    assert f"Removed {email}" in response.json()["message"]

def test_remove_participant_not_found():
    # Arrange
    activity = "Chess Club"
    email = "notfound@mergington.edu"
    # Act
    response = client.delete(f"/activities/{activity}/participants?email={email}")
    # Assert
    assert response.status_code == 404
    assert "Participant not found" in response.json()["detail"]

def test_remove_activity_not_found():
    # Arrange
    activity = "Nonexistent Club"
    email = "nouser@mergington.edu"
    # Act
    response = client.delete(f"/activities/{activity}/participants?email={email}")
    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]
