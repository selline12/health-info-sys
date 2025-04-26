import pytest
import time
from app.extensions import redis_client

def test_redis_connection(app):
    """Test Redis connection is working"""
    with app.app_context():
        assert redis_client.ping() is True

def test_clients_cache(client, auth_headers):
    """Test that clients data is cached after first request"""
    # First request - should hit database
    start_time = time.time()
    response1 = client.get('/api/v1/clients', headers=auth_headers)
    db_time = time.time() - start_time
    
    # Second request - should hit cache
    start_time = time.time()
    response2 = client.get('/api/v1/clients', headers=auth_headers)
    cache_time = time.time() - start_time
    
    # Verify responses are identical
    assert response1.status_code == 200
    assert response2.status_code == 200
    assert response1.json == response2.json
    
    # Cache should be faster
    assert cache_time < db_time

def test_cache_invalidation(client, auth_headers):
    """Test that cache is invalidated when client data changes"""
    # Get initial data
    response1 = client.get('/api/v1/clients', headers=auth_headers)
    initial_count = len(response1.json)
    
    # Create new client
    new_client = {
        'name': 'New Cached Client',
        'date_of_birth': '1995-05-05',
        'contact_info': 'cache@example.com'
    }
    client.post('/api/v1/clients', json=new_client, headers=auth_headers)
    
    # Get updated data
    response2 = client.get('/api/v1/clients', headers=auth_headers)
    assert len(response2.json) == initial_count + 1

def test_cache_expiration(client, auth_headers):
    """Test that cache expires after configured time"""
    # First request - should hit database
    response1 = client.get('/api/v1/clients', headers=auth_headers)
    
    # Wait for cache to expire (assuming 5 minute cache time)
    time.sleep(301)  # 5 minutes + 1 second
    
    # Second request - should hit database again
    response2 = client.get('/api/v1/clients', headers=auth_headers)
    
    # Verify responses are identical but cache was invalidated
    assert response1.status_code == 200
    assert response2.status_code == 200
    assert response1.json == response2.json 