import pytest
from app import create_app
from app.extensions import db
from app.models.models import User, Client
from datetime import datetime

@pytest.fixture
def app():
    app = create_app('testing')
    app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'JWT_SECRET_KEY': 'test-secret-key',
        'REDIS_URL': 'redis://localhost:6379/1'
    })

    with app.app_context():
        db.create_all()
        
        # Create test user
        test_user = User(username='testuser')
        test_user.set_password('testpass')
        db.session.add(test_user)
        
        # Create test client
        test_client = Client(
            name='Test Client',
            date_of_birth=datetime.strptime('1990-01-01', '%Y-%m-%d').date(),
            contact_info='test@example.com'
        )
        db.session.add(test_client)
        db.session.commit()
        
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def auth_headers(client):
    # Login and get token
    response = client.post('/api/v1/auth/login', 
        json={'username': 'testuser', 'password': 'testpass'})
    token = response.json['access_token']
    return {'Authorization': f'Bearer {token}'}

@pytest.fixture
def test_user():
    return {
        'username': 'testuser',
        'password': 'testpass'
    }

@pytest.fixture
def test_client_data():
    return {
        'name': 'Test Client',
        'date_of_birth': '1990-01-01',
        'contact_info': 'test@example.com'
    } 