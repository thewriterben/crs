"""
API tests for authentication endpoints
"""
import pytest
import json


@pytest.mark.integration
@pytest.mark.api
@pytest.mark.auth
class TestAuthAPI:
    """Test authentication API endpoints"""
    
    def test_register_success(self, client):
        """Test successful user registration"""
        response = client.post('/api/auth/register', json={
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'SecurePass123!'
        })
        
        assert response.status_code == 201
        data = response.json
        assert 'message' in data
        assert 'user' in data
        assert data['user']['username'] == 'newuser'
    
    def test_register_duplicate_username(self, client, test_user):
        """Test registration with duplicate username"""
        response = client.post('/api/auth/register', json={
            'username': 'testuser',
            'email': 'another@example.com',
            'password': 'SecurePass123!'
        })
        
        assert response.status_code == 400
        data = response.json
        assert 'error' in data
    
    def test_login_success(self, client, test_user):
        """Test successful login"""
        response = client.post('/api/auth/login', json={
            'username': 'testuser',
            'password': 'testpassword123'
        })
        
        assert response.status_code == 200
        data = response.json
        assert 'access_token' in data
        assert 'refresh_token' in data
        assert 'user' in data
    
    def test_login_invalid_credentials(self, client, test_user):
        """Test login with invalid credentials"""
        response = client.post('/api/auth/login', json={
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        
        assert response.status_code == 401
        data = response.json
        assert 'error' in data
    
    def test_get_profile_authenticated(self, client, auth_headers):
        """Test getting profile with authentication"""
        response = client.get('/api/auth/profile', headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json
        assert 'user' in data
        assert data['user']['username'] == 'testuser'
    
    def test_get_profile_unauthenticated(self, client):
        """Test getting profile without authentication"""
        response = client.get('/api/auth/profile')
        
        assert response.status_code == 401
    
    def test_logout(self, client, auth_headers):
        """Test logout endpoint"""
        response = client.post('/api/auth/logout', headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json
        assert 'message' in data
