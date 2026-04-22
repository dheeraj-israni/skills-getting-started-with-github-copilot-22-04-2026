import pytest
from fastapi.testclient import TestClient
from src.app import app
import copy


# Store the initial state of activities
INITIAL_ACTIVITIES = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Basketball Team": {
        "description": "Competitive basketball team for intramural and tournament play",
        "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
        "max_participants": 15,
        "participants": ["james@mergington.edu"]
    },
    "Tennis Club": {
        "description": "Learn tennis skills and compete in friendly matches",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:00 PM",
        "max_participants": 10,
        "participants": ["sarah@mergington.edu", "alexis@mergington.edu"]
    },
    "Theater Club": {
        "description": "Perform in school plays and musicals",
        "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 25,
        "participants": ["lucas@mergington.edu", "maya@mergington.edu"]
    },
    "Art Studio": {
        "description": "Explore painting, drawing, and sculpture techniques",
        "schedule": "Thursdays, 3:30 PM - 5:00 PM",
        "max_participants": 18,
        "participants": ["ava@mergington.edu"]
    },
    "Science Club": {
        "description": "Conduct experiments and explore scientific concepts",
        "schedule": "Mondays, 3:30 PM - 4:30 PM",
        "max_participants": 16,
        "participants": ["ryan@mergington.edu", "zara@mergington.edu"]
    },
    "Debate Team": {
        "description": "Develop argumentation and public speaking skills",
        "schedule": "Fridays, 3:30 PM - 4:30 PM",
        "max_participants": 12,
        "participants": ["rachel@mergington.edu"]
    }
}


@pytest.fixture
def client():
    """Fixture providing TestClient for FastAPI app with reset state before each test"""
    # Import activities from app to reset it
    from src import app as app_module
    
    # Reset the activities to initial state
    app_module.activities.clear()
    app_module.activities.update(copy.deepcopy(INITIAL_ACTIVITIES))
    
    # Return TestClient
    return TestClient(app_module.app)
