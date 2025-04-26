import pytest
from app.models.models import Client
from datetime import datetime

def test_get_clients_unauthorized(client):
    response = client.get('/api/v1/clients')
    assert response.status_code == 401

def test_get_clients_success(client, auth_headers):
    response = client.get('/api/v1/clients', headers=auth_headers)
    assert response.status_code == 200
    assert len(response.json) == 1
    assert response.json[0]['name'] == 'Test Client'
    assert response.json[0]['date_of_birth'] == '1990-01-01'
    assert response.json[0]['contact_info'] == 'test@example.com'

def test_create_client_success(client, auth_headers):
    new_client = {
        'name': 'New Client',
        'date_of_birth': '1995-05-05',
        'contact_info': 'new@example.com'
    }
    response = client.post('/api/v1/clients', 
        json=new_client, 
        headers=auth_headers)
    assert response.status_code == 201
    assert response.json['name'] == new_client['name']
    assert response.json['date_of_birth'] == new_client['date_of_birth']
    assert response.json['contact_info'] == new_client['contact_info']

def test_create_client_missing_fields(client, auth_headers):
    response = client.post('/api/v1/clients', 
        json={'name': 'Incomplete Client'}, 
        headers=auth_headers)
    assert response.status_code == 400
    assert 'Missing required fields' in response.json['message']

def test_get_client_by_id_success(client, auth_headers):
    # First create a client
    new_client = {
        'name': 'Test Get Client',
        'date_of_birth': '1990-01-01',
        'contact_info': 'test@example.com'
    }
    create_response = client.post('/api/v1/clients', 
        json=new_client, 
        headers=auth_headers)
    client_id = create_response.json['id']

    # Then get it by ID
    response = client.get(f'/api/v1/clients/{client_id}', headers=auth_headers)
    assert response.status_code == 200
    assert response.json['name'] == new_client['name']
    assert response.json['date_of_birth'] == new_client['date_of_birth']
    assert response.json['contact_info'] == new_client['contact_info']

def test_get_nonexistent_client(client, auth_headers):
    response = client.get('/api/v1/clients/999', headers=auth_headers)
    assert response.status_code == 404
    assert 'Client not found' in response.json['message']

def test_update_client_success(client, auth_headers):
    # First create a client
    new_client = {
        'name': 'Original Client',
        'date_of_birth': '1990-01-01',
        'contact_info': 'original@example.com'
    }
    create_response = client.post('/api/v1/clients', 
        json=new_client, 
        headers=auth_headers)
    client_id = create_response.json['id']

    # Then update it
    updated_data = {
        'name': 'Updated Client',
        'date_of_birth': '1995-05-05',
        'contact_info': 'updated@example.com'
    }
    response = client.put(f'/api/v1/clients/{client_id}', 
        json=updated_data, 
        headers=auth_headers)
    assert response.status_code == 200
    assert response.json['name'] == updated_data['name']
    assert response.json['date_of_birth'] == updated_data['date_of_birth']
    assert response.json['contact_info'] == updated_data['contact_info']

def test_delete_client_success(client, auth_headers):
    # First create a client
    new_client = {
        'name': 'Client to Delete',
        'date_of_birth': '1990-01-01',
        'contact_info': 'delete@example.com'
    }
    create_response = client.post('/api/v1/clients', 
        json=new_client, 
        headers=auth_headers)
    client_id = create_response.json['id']

    # Then delete it
    response = client.delete(f'/api/v1/clients/{client_id}', headers=auth_headers)
    assert response.status_code == 200
    assert 'Client deleted successfully' in response.json['message']

    # Verify it's deleted
    get_response = client.get(f'/api/v1/clients/{client_id}', headers=auth_headers)
    assert get_response.status_code == 404 