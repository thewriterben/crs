"""
Integration tests for API endpoints
"""
import pytest


@pytest.mark.integration
@pytest.mark.api
class TestHealthEndpoints:
    """Test cases for health check endpoints"""
    
    def test_liveness_check(self, client):
        """Test liveness endpoint"""
        response = client.get('/health/live')
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] == 'alive'
    
    def test_readiness_check(self, client):
        """Test readiness endpoint"""
        response = client.get('/health/ready')
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] == 'ready'
    
    def test_health_info(self, client):
        """Test health info endpoint"""
        response = client.get('/health/info')
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'service' in data
        assert 'version' in data
        assert 'uptime' in data
