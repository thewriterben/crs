"""
Tests for health check endpoints
"""
import pytest


@pytest.mark.integration
@pytest.mark.api
class TestHealthEndpoints:
    """Test health check endpoints"""
    
    def test_liveness_probe(self, client):
        """Test liveness probe endpoint"""
        response = client.get('/api/health/liveness')
        
        assert response.status_code == 200
        data = response.json
        assert data['status'] == 'alive'
        assert 'timestamp' in data
    
    def test_readiness_probe(self, client):
        """Test readiness probe endpoint"""
        response = client.get('/api/health/readiness')
        
        # Should return 200 or 503 depending on dependencies
        assert response.status_code in [200, 503]
        data = response.json
        assert 'status' in data
        assert 'checks' in data
    
    def test_info_endpoint(self, client):
        """Test info endpoint"""
        response = client.get('/api/health/info')
        
        assert response.status_code == 200
        data = response.json
        assert 'version' in data
        assert 'python_version' in data
        assert 'platform' in data
