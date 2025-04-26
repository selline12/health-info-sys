import pytest
from app.models.models import User

def test_login_success(client):
    response = client.post('/api/v1/auth/login', 
        json={'username': 'testuser', 'password': 'testpass'})
    assert response.status_code == 200
    assert 'access_token' in response.json

def test_login_wrong_password(client):
    response = client.post('/api/v1/auth/login', 
        json={'username': 'testuser', 'password': 'wrongpass'})
    assert response.status_code == 401
    assert 'Invalid credentials' in response.json['message']

def test_login_nonexistent_user(client):
    response = client.post('/api/v1/auth/login', 
        json={'username': 'nonexistent', 'password': 'testpass'})
    assert response.status_code == 401
    assert 'Invalid credentials' in response.json['message']

def test_login_missing_fields(client):
    response = client.post('/api/v1/auth/login', 
        json={'username': 'testuser'})
    assert response.status_code == 400
    assert 'Missing required fields' in response.json['message']

def test_protected_route_without_token(client):
    response = client.get('/api/v1/clients')
    assert response.status_code == 401
    assert 'Missing Authorization Header' in response.json['message']

def test_protected_route_with_invalid_token(client):
    response = client.get('/api/v1/clients', 
        headers={'Authorization': 'Bearer invalid_token'})
    assert response.status_code == 422
    assert 'Not enough segments' in response.json['message'] 