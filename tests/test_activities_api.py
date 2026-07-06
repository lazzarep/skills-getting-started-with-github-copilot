def test_get_activities_returns_activity_map(client):
    # Arrange
    endpoint = "/activities"

    # Act
    response = client.get(endpoint)
    body = response.json()

    # Assert
    assert response.status_code == 200
    assert isinstance(body, dict)
    assert "Chess Club" in body
    assert "participants" in body["Chess Club"]
    assert isinstance(body["Chess Club"]["participants"], list)


def test_signup_successfully_registers_participant(client):
    # Arrange
    activity_name = "Chess Club"
    email = "new.student@mergington.edu"
    endpoint = f"/activities/{activity_name}/signup"

    # Act
    response = client.post(endpoint, params={"email": email})
    body = response.json()

    # Assert
    assert response.status_code == 200
    assert body["message"] == f"Signed up {email} for {activity_name}"


def test_signup_duplicate_participant_returns_conflict(client):
    # Arrange
    activity_name = "Chess Club"
    existing_email = "michael@mergington.edu"
    endpoint = f"/activities/{activity_name}/signup"

    # Act
    response = client.post(endpoint, params={"email": existing_email})
    body = response.json()

    # Assert
    assert response.status_code == 409
    assert body["detail"] == f"{existing_email} is already signed up for {activity_name}"


def test_signup_unknown_activity_returns_not_found(client):
    # Arrange
    activity_name = "Unknown Club"
    email = "student@mergington.edu"
    endpoint = f"/activities/{activity_name}/signup"

    # Act
    response = client.post(endpoint, params={"email": email})
    body = response.json()

    # Assert
    assert response.status_code == 404
    assert body["detail"] == "Activity not found"


def test_unregister_successfully_removes_participant(client):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"
    endpoint = f"/activities/{activity_name}/participants"

    # Act
    response = client.delete(endpoint, params={"email": email})
    body = response.json()

    # Assert
    assert response.status_code == 200
    assert body["message"] == f"Unregistered {email} from {activity_name}"


def test_unregister_unknown_activity_returns_not_found(client):
    # Arrange
    activity_name = "Unknown Club"
    email = "student@mergington.edu"
    endpoint = f"/activities/{activity_name}/participants"

    # Act
    response = client.delete(endpoint, params={"email": email})
    body = response.json()

    # Assert
    assert response.status_code == 404
    assert body["detail"] == "Activity not found"


def test_unregister_nonexistent_participant_returns_not_found(client):
    # Arrange
    activity_name = "Chess Club"
    email = "not.registered@mergington.edu"
    endpoint = f"/activities/{activity_name}/participants"

    # Act
    response = client.delete(endpoint, params={"email": email})
    body = response.json()

    # Assert
    assert response.status_code == 404
    assert body["detail"] == f"{email} is not signed up for {activity_name}"