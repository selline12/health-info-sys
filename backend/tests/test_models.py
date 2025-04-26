import pytest
from app.models.models import User, Client
from datetime import datetime

def test_user_creation():
    """Test user creation and password hashing"""
    user = User(username='testuser')
    user.set_password('testpass')
    
    assert user.username == 'testuser'
    assert user.check_password('testpass') is True
    assert user.check_password('wrongpass') is False
    assert user.password_hash is not None
    assert user.password_hash != 'testpass'

def test_client_creation():
    """Test client creation with valid data"""
    client = Client(
        name='Test Client',
        date_of_birth=datetime.strptime('1990-01-01', '%Y-%m-%d').date(),
        contact_info='test@example.com'
    )
    
    assert client.name == 'Test Client'
    assert client.date_of_birth == datetime.strptime('1990-01-01', '%Y-%m-%d').date()
    assert client.contact_info == 'test@example.com'
    assert client.created_at is not None
    assert client.updated_at is not None

def test_client_validation():
    """Test client validation with invalid data"""
    with pytest.raises(ValueError):
        Client(
            name='',  # Empty name
            date_of_birth=datetime.strptime('1990-01-01', '%Y-%m-%d').date(),
            contact_info='test@example.com'
        )
    
    with pytest.raises(ValueError):
        Client(
            name='Test Client',
            date_of_birth=datetime.strptime('1990-01-01', '%Y-%m-%d').date(),
            contact_info=''  # Empty contact info
        )

def test_client_update():
    """Test client data update"""
    client = Client(
        name='Original Client',
        date_of_birth=datetime.strptime('1990-01-01', '%Y-%m-%d').date(),
        contact_info='original@example.com'
    )
    
    original_updated_at = client.updated_at
    
    # Update client data
    client.name = 'Updated Client'
    client.contact_info = 'updated@example.com'
    
    assert client.name == 'Updated Client'
    assert client.contact_info == 'updated@example.com'
    assert client.updated_at > original_updated_at

def test_client_serialization():
    """Test client data serialization"""
    client = Client(
        name='Test Client',
        date_of_birth=datetime.strptime('1990-01-01', '%Y-%m-%d').date(),
        contact_info='test@example.com'
    )
    
    serialized = client.to_dict()
    
    assert serialized['name'] == 'Test Client'
    assert serialized['date_of_birth'] == '1990-01-01'
    assert serialized['contact_info'] == 'test@example.com'
    assert 'id' in serialized
    assert 'created_at' in serialized
    assert 'updated_at' in serialized 