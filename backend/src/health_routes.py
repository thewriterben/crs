"""
Health check and monitoring endpoints for CRS Backend
"""
from flask import Blueprint, jsonify
from datetime import datetime
import sys
import os

health_bp = Blueprint('health', __name__, url_prefix='/api/health')

@health_bp.route('/liveness', methods=['GET'])
def liveness():
    """
    Kubernetes/Docker liveness probe endpoint
    Returns 200 if the application is running
    """
    return jsonify({
        'status': 'alive',
        'timestamp': datetime.utcnow().isoformat()
    }), 200

@health_bp.route('/readiness', methods=['GET'])
def readiness():
    """
    Kubernetes/Docker readiness probe endpoint
    Returns 200 if the application is ready to serve traffic
    """
    checks = {
        'status': 'ready',
        'timestamp': datetime.utcnow().isoformat(),
        'checks': {}
    }
    
    # Check database connection
    try:
        from .models import db
        db.session.execute('SELECT 1')
        checks['checks']['database'] = 'healthy'
    except Exception as e:
        checks['checks']['database'] = f'unhealthy: {str(e)}'
        checks['status'] = 'not_ready'
    
    # Check Redis connection (if configured)
    if os.environ.get('REDIS_URL'):
        try:
            from redis import Redis
            redis_client = Redis.from_url(os.environ.get('REDIS_URL'))
            redis_client.ping()
            checks['checks']['redis'] = 'healthy'
        except Exception as e:
            checks['checks']['redis'] = f'unhealthy: {str(e)}'
            # Redis is optional, don't fail readiness check
    
    status_code = 200 if checks['status'] == 'ready' else 503
    return jsonify(checks), status_code

@health_bp.route('/metrics', methods=['GET'])
def metrics():
    """
    Basic application metrics endpoint
    """
    import psutil
    
    try:
        process = psutil.Process()
        memory_info = process.memory_info()
        
        metrics = {
            'timestamp': datetime.utcnow().isoformat(),
            'system': {
                'python_version': sys.version,
                'platform': sys.platform,
            },
            'process': {
                'memory_rss_mb': round(memory_info.rss / 1024 / 1024, 2),
                'memory_percent': round(process.memory_percent(), 2),
                'cpu_percent': round(process.cpu_percent(), 2),
                'num_threads': process.num_threads(),
            },
            'application': {
                'uptime_seconds': round(datetime.utcnow().timestamp() - process.create_time()),
            }
        }
    except Exception as e:
        metrics = {
            'error': f'Could not gather metrics: {str(e)}',
            'timestamp': datetime.utcnow().isoformat()
        }
    
    return jsonify(metrics), 200

@health_bp.route('/info', methods=['GET'])
def info():
    """
    Application information endpoint
    """
    return jsonify({
        'name': 'CRS Cryptocurrency Marketplace API',
        'version': '1.0.0',
        'environment': os.environ.get('FLASK_ENV', 'development'),
        'timestamp': datetime.utcnow().isoformat(),
        'endpoints': {
            'health': '/api/health/liveness',
            'readiness': '/api/health/readiness',
            'metrics': '/api/health/metrics',
            'api': '/api/ai/dashboard-data'
        }
    }), 200
