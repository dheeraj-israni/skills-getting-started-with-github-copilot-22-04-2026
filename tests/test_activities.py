import pytest
from fastapi.testclient import TestClient


class TestGetActivities:
    """Tests for GET /activities endpoint"""

    def test_get_activities_returns_all_activities(self, client):
        # Arrange
        expected_activities = {"Chess Club", "Programming Class", "Gym Class", 
                               "Basketball Team", "Tennis Club", "Theater Club", 
                               "Art Studio", "Science Club", "Debate Team"}

        # Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == 200
        activities = response.json()
        assert set(activities.keys()) == expected_activities

    def test_get_activities_contains_required_fields(self, client):
        # Arrange
        required_fields = {"description", "schedule", "max_participants", "participants"}

        # Act
        response = client.get("/activities")
        activities = response.json()

        # Assert
        for activity_name, activity_data in activities.items():
            assert set(activity_data.keys()) == required_fields

    def test_get_activities_participants_is_list(self, client):
        # Arrange & Act
        response = client.get("/activities")
        activities = response.json()

        # Assert
        for activity_name, activity_data in activities.items():
            assert isinstance(activity_data["participants"], list)
            for participant in activity_data["participants"]:
                assert isinstance(participant, str)

    def test_get_activities_max_participants_is_positive(self, client):
        # Arrange & Act
        response = client.get("/activities")
        activities = response.json()

        # Assert
        for activity_name, activity_data in activities.items():
            assert activity_data["max_participants"] > 0

    def test_get_activities_participant_count_within_limit(self, client):
        # Arrange & Act
        response = client.get("/activities")
        activities = response.json()

        # Assert
        for activity_name, activity_data in activities.items():
            participant_count = len(activity_data["participants"])
            assert participant_count <= activity_data["max_participants"]


class TestSignupForActivity:
    """Tests for POST /activities/{activity_name}/signup endpoint"""

    def test_signup_successful(self, client):
        # Arrange
        activity_name = "Chess Club"
        email = "newstudent@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert email in data["message"]

    def test_signup_adds_participant_to_activity(self, client):
        # Arrange
        activity_name = "Chess Club"
        email = "newstudent@mergington.edu"

        # Act
        client.post(f"/activities/{activity_name}/signup", params={"email": email})
        response = client.get("/activities")

        # Assert
        activities = response.json()
        assert email in activities[activity_name]["participants"]

    def test_signup_activity_not_found(self, client):
        # Arrange
        activity_name = "NonExistent Club"
        email = "student@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]

    def test_signup_duplicate_already_registered(self, client):
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Already registered

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 400
        assert "already signed up" in response.json()["detail"]

    def test_signup_with_special_characters_in_email(self, client):
        # Arrange
        activity_name = "Chess Club"
        email = "student+tag@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 200
        activities_response = client.get("/activities")
        assert email in activities_response.json()["Chess Club"]["participants"]

    def test_signup_with_special_characters_in_activity_name(self, client):
        # Arrange - first verify "Art Studio" exists
        response = client.get("/activities")
        activities = response.json()
        assert "Art Studio" in activities

        activity_name = "Art Studio"
        email = "testuser@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 200

    def test_signup_participant_count_increases(self, client):
        # Arrange
        activity_name = "Programming Class"
        email = "newprogrammer@mergington.edu"
        
        response_before = client.get("/activities")
        count_before = len(response_before.json()[activity_name]["participants"])

        # Act
        client.post(f"/activities/{activity_name}/signup", params={"email": email})

        # Assert
        response_after = client.get("/activities")
        count_after = len(response_after.json()[activity_name]["participants"])
        assert count_after == count_before + 1


class TestRemoveParticipant:
    """Tests for DELETE /activities/{activity_name}/participants/{email} endpoint"""

    def test_remove_participant_successful(self, client):
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"

        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants/{email}"
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert email in data["message"]

    def test_remove_participant_actually_removes(self, client):
        # Arrange
        activity_name = "Programming Class"
        email = "emma@mergington.edu"

        # Act
        client.delete(f"/activities/{activity_name}/participants/{email}")
        response = client.get("/activities")

        # Assert
        activities = response.json()
        assert email not in activities[activity_name]["participants"]

    def test_remove_participant_activity_not_found(self, client):
        # Arrange
        activity_name = "NonExistent Club"
        email = "student@mergington.edu"

        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants/{email}"
        )

        # Assert
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]

    def test_remove_participant_not_found_in_activity(self, client):
        # Arrange
        activity_name = "Chess Club"
        email = "notregistered@mergington.edu"

        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants/{email}"
        )

        # Assert
        assert response.status_code == 404
        assert "Participant not found" in response.json()["detail"]

    def test_remove_participant_decreases_count(self, client):
        # Arrange
        activity_name = "Gym Class"
        email = "john@mergington.edu"
        
        response_before = client.get("/activities")
        count_before = len(response_before.json()[activity_name]["participants"])

        # Act
        client.delete(f"/activities/{activity_name}/participants/{email}")
        response_after = client.get("/activities")

        # Assert
        count_after = len(response_after.json()[activity_name]["participants"])
        assert count_after == count_before - 1

    def test_remove_participant_with_special_characters(self, client):
        # Arrange - first add participant with special chars
        activity_name = "Chess Club"
        email = "student+test@mergington.edu"
        client.post(f"/activities/{activity_name}/signup", params={"email": email})

        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants/{email}"
        )

        # Assert
        assert response.status_code == 200
        activities_response = client.get("/activities")
        assert email not in activities_response.json()[activity_name]["participants"]

    def test_remove_participant_idempotency(self, client):
        # Arrange
        activity_name = "Tennis Club"
        email = "alexis@mergington.edu"
        
        # First removal should succeed
        response_first = client.delete(
            f"/activities/{activity_name}/participants/{email}"
        )
        assert response_first.status_code == 200

        # Act - second removal attempt
        response_second = client.delete(
            f"/activities/{activity_name}/participants/{email}"
        )

        # Assert - should fail since participant already removed
        assert response_second.status_code == 404
