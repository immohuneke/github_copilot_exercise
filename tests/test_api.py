from urllib.parse import quote

from fastapi.testclient import TestClient


def test_get_activities_returns_all_activities(client: TestClient):
    # Arrange
    url = "/activities"

    # Act
    response = client.get(url)

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert isinstance(data["Chess Club"]["participants"], list)
    assert data["Chess Club"]["max_participants"] == 12


def test_signup_success_adds_participant(client: TestClient):
    # Arrange
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"
    url = f"/activities/{quote(activity_name)}/signup?email={quote(email, safe='')}"

    # Act
    response = client.post(url)

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for {activity_name}"}

    activities_response = client.get("/activities").json()
    assert email in activities_response[activity_name]["participants"]


def test_signup_nonexistent_activity_returns_404(client: TestClient):
    # Arrange
    activity_name = "Nonexistent Club"
    email = "student@mergington.edu"
    url = f"/activities/{quote(activity_name)}/signup?email={quote(email, safe='')}"

    # Act
    response = client.post(url)

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_duplicate_returns_409(client: TestClient):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"
    url = f"/activities/{quote(activity_name)}/signup?email={quote(email, safe='')}"

    # Act
    response = client.post(url)

    # Assert
    assert response.status_code == 409
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_unregister_success_removes_participant(client: TestClient):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"
    url = f"/activities/{quote(activity_name)}/unregister?email={quote(email, safe='')}"

    # Act
    response = client.delete(url)

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Unregistered {email} from {activity_name}"}

    activities_response = client.get("/activities").json()
    assert email not in activities_response[activity_name]["participants"]


def test_unregister_nonexistent_activity_returns_404(client: TestClient):
    # Arrange
    activity_name = "Nonexistent Club"
    email = "student@mergington.edu"
    url = f"/activities/{quote(activity_name)}/unregister?email={quote(email, safe='')}"

    # Act
    response = client.delete(url)

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_nonexistent_participant_returns_404(client: TestClient):
    # Arrange
    activity_name = "Chess Club"
    email = "unknown@mergington.edu"
    url = f"/activities/{quote(activity_name)}/unregister?email={quote(email, safe='')}"

    # Act
    response = client.delete(url)

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Student not found in activity"
