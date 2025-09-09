import requests
import json
import uuid

# Replace with your actual frontend URL if different
BASE_URL = "http://localhost:3000"
# Since the backend is running on port 8000, we'll target that directly for our tests
API_URL = "http://localhost:8000"

def generate_unique_user():
    unique_id = str(uuid.uuid4())
    return {
        "username": f"testuser_{unique_id}",
        "email": f"test_{unique_id}@example.com",
        "password": "password123"
    }

def test_signup():
    print("Testing Sign-Up...")
    user_data = generate_unique_user()

    response = requests.post(f"{API_URL}/accounts/register", json=user_data)

    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")

    assert response.status_code == 201
    assert response.json()["status"] == "success"
    print("Sign-Up Test Passed!")
    return user_data

def test_signin(user_data):
    print("\nTesting Sign-In...")
    signin_data = {
        "identifier": user_data["email"],
        "password": user_data["password"]
    }

    response = requests.post(f"{API_URL}/accounts/login", json=signin_data)

    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")

    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert "access_token" in response.cookies
    assert "refresh_token" in response.cookies
    print("Sign-In Test Passed!")

if __name__ == "__main__":
    try:
        new_user = test_signup()
        test_signin(new_user)
        print("\nAll tests passed!")
    except AssertionError as e:
        print(f"\nTest failed: {e}")
    except Exception as e:
        print(f"\nAn error occurred: {e}")
