import requests
import json

BASE_URL = "http://localhost:5000"

def test_authentication():
    # Test login
    print("Testing login...")
    login_url = f"{BASE_URL}/api/v1/auth/login"
    login_data = {
        "username": "admin",
        "password": "admin"
    }
    
    try:
        # Login request
        login_response = requests.post(login_url, json=login_data)
        print(f"Login Response Status: {login_response.status_code}")
        print(f"Login Response: {login_response.text}")
        
        if login_response.status_code == 200:
            token = login_response.json()["access_token"]
            print("\nLogin successful! Token received.")
            
            # Test protected endpoint
            print("\nTesting protected endpoint...")
            clients_url = f"{BASE_URL}/api/v1/clients"
            headers = {
                "Authorization": f"Bearer {token}"
            }
            clients_response = requests.get(clients_url, headers=headers)
            print(f"Clients Response Status: {clients_response.status_code}")
            print(f"Clients Response: {clients_response.text}")
        else:
            print("Login failed!")
            
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        print("Make sure the Flask server is running!")

if __name__ == "__main__":
    test_authentication() 