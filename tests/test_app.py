from fastapi.testclient import TestClient

from src.app import app, activities


client = TestClient(app)


def test_signup_updates_activity_participants():
    activity_name = "Chess Club"
    original_participants = list(activities[activity_name]["participants"])
    email = "signup-refresh@mergington.edu"

    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    assert response.status_code == 200
    assert email in activities[activity_name]["participants"]

    activities[activity_name]["participants"] = original_participants


def test_unregister_participant_removes_email():
    activity_name = "Chess Club"
    original_participants = list(activities[activity_name]["participants"])
    email = original_participants[0]

    response = client.delete(f"/activities/{activity_name}/participants/{email}")

    assert response.status_code == 200
    assert email not in activities[activity_name]["participants"]
    assert response.json()["message"] == f"Removed {email} from {activity_name}"

    activities[activity_name]["participants"] = original_participants
