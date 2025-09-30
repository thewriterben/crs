"""
Integration tests for authentication routes
"""
import pytest
import json


@pytest.mark.integration
@pytest.mark.auth
class TestAuthRoutes:
    """Test cases for authentication endpoints"""
    
    def test_register_success(self, client):
        """Test successful user registration"""
        response = client.post('/api/auth/register', 
            json={
                'username': 'newuser',
                'email': 'newuser@example.com',
                'password': 'SecurePassword123!'
            }
        )
        
        assert response.status_code == 201
        data = response.get_json()
        assert data['message'] == 'User registered successfully'
        assert 'user' in data
        assert data['user']['username'] == 'newuser'
        assert data['user']['email'] == 'newuser@example.com'
    
    def test_register_duplicate_username(self, client):
        """Test registration with duplicate username"""
        # Register first user
        client.post('/api/auth/register', 
            json={
                'username': 'testuser',
                'email': 'test1@example.com',
                'password': 'Password123!'
            }
        )
        
        # Try to register with same username
        response = client.post('/api/auth/register', 
            json={
                'username': 'testuser',
                'email': 'test2@example.com',
                'password': 'Password123!'
            }
        )
        
        assert response.status_code == 400
        data = response.get_json()
        assert 'already exists' in data['message'].lower()
    
    def test_register_invalid_email(self, client):
        """Test registration with invalid email"""
        response = client.post('/api/auth/register', 
            json={
                'username': 'testuser',
                'email': 'invalid-email',
                'password': 'Password123!'
            }
        )
        
        assert response.status_code == 400
    
    def test_register_weak_password(self, client):
        """Test registration with weak password"""
        response = client.post('/api/auth/register', 
            json={
                'username': 'testuser',
                'email': 'test@example.com',
                'password': '123'
            }
        )
        
        assert response.status_code == 400
    
    def test_login_success(self, client):
        """Test successful login"""
        # Register user first
        client.post('/api/auth/register', 
            json={
                'username': 'testuser',
                'email': 'test@example.com',
                'password': 'Password123!'
            }
        )
        
        # Login
        response = client.post('/api/auth/login', 
            json={
                'username': 'testuser',
                'password': 'Password123!'
            }
        )
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'access_token' in data
        assert 'refresh_token' in data
        assert 'user' in data
    
    def test_login_wrong_password(self, client):
        """Test login with wrong password"""
        # Register user first
        client.post('/api/auth/register', 
            json={
                'username': 'testuser',
                'email': 'test@example.com',
                'password': 'Password123!'
            }
        )
        
        # Login with wrong password
        response = client.post('/api/auth/login', 
            json={
                'username': 'testuser',
                'password': 'WrongPassword!'
            }
        )
        
        assert response.status_code == 401
    
    def test_login_nonexistent_user(self, client):
        """Test login with non-existent user"""
        response = client.post('/api/auth/login', 
            json={
                'username': 'nonexistent',
                'password': 'Password123!'
            }
        )
        
        assert response.status_code == 401
    
    def test_get_profile_authenticated(self, client):
        """Test getting profile with authentication"""
        # Register and login
        client.post('/api/auth/register', 
            json={
                'username': 'testuser',
                'email': 'test@example.com',
                'password': 'Password123!'
            }
        )
        
        login_response = client.post('/api/auth/login', 
            json={
                'username': 'testuser',
                'password': 'Password123!'
            }
        )
        
        access_token = login_response.get_json()['access_token']
        
        # Get profile
        response = client.get('/api/auth/profile',
            headers={'Authorization': f'Bearer {access_token}'}
        )
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['username'] == 'testuser'
        assert data['email'] == 'test@example.com'
    
    def test_get_profile_unauthenticated(self, client):
        """Test getting profile without authentication"""
        response = client.get('/api/auth/profile')
        
        assert response.status_code == 401
    
    def test_logout_success(self, client):
        """Test successful logout"""
        # Register and login
        client.post('/api/auth/register', 
            json={
                'username': 'testuser',
                'email': 'test@example.com',
                'password': 'Password123!'
            }
        )
        
        login_response = client.post('/api/auth/login', 
            json={
                'username': 'testuser',
                'password': 'Password123!'
            }
        )
        
        access_token = login_response.get_json()['access_token']
        
        # Logout
        response = client.post('/api/auth/logout',
            headers={'Authorization': f'Bearer {access_token}'}
        )
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'logged out' in data['message'].lower()
