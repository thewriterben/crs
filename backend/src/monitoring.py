"""
Performance monitoring and metrics collection
"""
import time
import psutil
import os
from flask import request, g
from functools import wraps
from datetime import datetime
import json


class PerformanceMonitor:
    """Performance monitoring utilities"""
    
    def __init__(self, app=None):
        self.metrics = {}
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        """Initialize monitoring with Flask app"""
        
        @app.before_request
        def start_timer():
            """Record request start time"""
            g.start_time = time.time()
        
        @app.after_request
        def log_request(response):
            """Log request metrics"""
            if hasattr(g, 'start_time'):
                elapsed = time.time() - g.start_time
                
                # Log slow requests
                if elapsed > 1.0:  # > 1 second
                    app.logger.warning(
                        f"Slow request: {request.method} {request.path} took {elapsed:.2f}s"
                    )
                
                # Add performance header
                response.headers['X-Response-Time'] = f"{elapsed*1000:.2f}ms"
            
            return response


def monitor_performance(func):
    """
    Decorator to monitor function performance
    
    Usage:
        @monitor_performance
        def expensive_function():
            ...
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        
        try:
            result = func(*args, **kwargs)
            elapsed = time.time() - start_time
            
            # Log performance
            print(f"[PERF] {func.__name__} took {elapsed:.4f}s")
            
            return result
        except Exception as e:
            elapsed = time.time() - start_time
            print(f"[PERF] {func.__name__} failed after {elapsed:.4f}s: {str(e)}")
            raise
    
    return wrapper


class SystemMetrics:
    """System resource metrics"""
    
    @staticmethod
    def get_cpu_usage():
        """Get CPU usage percentage"""
        return psutil.cpu_percent(interval=1)
    
    @staticmethod
    def get_memory_usage():
        """Get memory usage information"""
        memory = psutil.virtual_memory()
        return {
            'total': memory.total,
            'available': memory.available,
            'percent': memory.percent,
            'used': memory.used,
            'free': memory.free
        }
    
    @staticmethod
    def get_disk_usage():
        """Get disk usage information"""
        disk = psutil.disk_usage('/')
        return {
            'total': disk.total,
            'used': disk.used,
            'free': disk.free,
            'percent': disk.percent
        }
    
    @staticmethod
    def get_network_stats():
        """Get network statistics"""
        net_io = psutil.net_io_counters()
        return {
            'bytes_sent': net_io.bytes_sent,
            'bytes_recv': net_io.bytes_recv,
            'packets_sent': net_io.packets_sent,
            'packets_recv': net_io.packets_recv,
            'errors_in': net_io.errin,
            'errors_out': net_io.errout
        }
    
    @staticmethod
    def get_process_info():
        """Get current process information"""
        process = psutil.Process(os.getpid())
        
        return {
            'pid': process.pid,
            'cpu_percent': process.cpu_percent(interval=1),
            'memory_percent': process.memory_percent(),
            'memory_info': process.memory_info()._asdict(),
            'num_threads': process.num_threads(),
            'create_time': datetime.fromtimestamp(process.create_time()).isoformat(),
            'status': process.status()
        }
    
    @staticmethod
    def get_all_metrics():
        """Get all system metrics"""
        return {
            'timestamp': datetime.utcnow().isoformat(),
            'cpu': SystemMetrics.get_cpu_usage(),
            'memory': SystemMetrics.get_memory_usage(),
            'disk': SystemMetrics.get_disk_usage(),
            'network': SystemMetrics.get_network_stats(),
            'process': SystemMetrics.get_process_info()
        }


class APIMetrics:
    """API performance metrics"""
    
    def __init__(self):
        self.request_counts = {}
        self.response_times = {}
        self.error_counts = {}
    
    def record_request(self, endpoint, method, response_time, status_code):
        """Record API request metrics"""
        key = f"{method} {endpoint}"
        
        # Count requests
        if key not in self.request_counts:
            self.request_counts[key] = 0
        self.request_counts[key] += 1
        
        # Track response times
        if key not in self.response_times:
            self.response_times[key] = []
        self.response_times[key].append(response_time)
        
        # Count errors
        if status_code >= 400:
            if key not in self.error_counts:
                self.error_counts[key] = 0
            self.error_counts[key] += 1
    
    def get_stats(self, endpoint=None):
        """Get statistics for endpoint(s)"""
        if endpoint:
            return self._get_endpoint_stats(endpoint)
        
        # Return all endpoints
        stats = {}
        for key in self.request_counts.keys():
            stats[key] = self._get_endpoint_stats(key)
        
        return stats
    
    def _get_endpoint_stats(self, key):
        """Calculate statistics for an endpoint"""
        if key not in self.request_counts:
            return None
        
        times = self.response_times.get(key, [])
        
        stats = {
            'request_count': self.request_counts[key],
            'error_count': self.error_counts.get(key, 0),
            'error_rate': self.error_counts.get(key, 0) / self.request_counts[key]
        }
        
        if times:
            sorted_times = sorted(times)
            stats.update({
                'avg_response_time': sum(times) / len(times),
                'min_response_time': min(times),
                'max_response_time': max(times),
                'p50': sorted_times[len(sorted_times) // 2],
                'p95': sorted_times[int(len(sorted_times) * 0.95)],
                'p99': sorted_times[int(len(sorted_times) * 0.99)]
            })
        
        return stats


class DatabaseMetrics:
    """Database performance metrics"""
    
    @staticmethod
    def get_connection_pool_stats(db):
        """Get database connection pool statistics"""
        engine = db.engine
        pool = engine.pool
        
        return {
            'pool_size': pool.size(),
            'checked_in': pool.checkedin(),
            'checked_out': pool.checkedout(),
            'overflow': pool.overflow(),
            'total_connections': pool.size() + pool.overflow()
        }
    
    @staticmethod
    def get_query_stats():
        """Get query performance statistics"""
        # This would integrate with query profiling
        # For now, return placeholder
        return {
            'slow_queries': 0,
            'total_queries': 0,
            'avg_query_time': 0.0
        }


class CacheMetrics:
    """Cache performance metrics"""
    
    def __init__(self):
        self.hits = 0
        self.misses = 0
        self.sets = 0
        self.deletes = 0
    
    def record_hit(self):
        """Record cache hit"""
        self.hits += 1
    
    def record_miss(self):
        """Record cache miss"""
        self.misses += 1
    
    def record_set(self):
        """Record cache set"""
        self.sets += 1
    
    def record_delete(self):
        """Record cache delete"""
        self.deletes += 1
    
    def get_stats(self):
        """Get cache statistics"""
        total_requests = self.hits + self.misses
        hit_rate = self.hits / total_requests if total_requests > 0 else 0
        
        return {
            'hits': self.hits,
            'misses': self.misses,
            'sets': self.sets,
            'deletes': self.deletes,
            'total_requests': total_requests,
            'hit_rate': hit_rate,
            'miss_rate': 1 - hit_rate
        }


# Global metrics instances
api_metrics = APIMetrics()
cache_metrics = CacheMetrics()


def setup_monitoring(app, db=None):
    """
    Setup comprehensive monitoring for Flask app
    
    Args:
        app: Flask application
        db: SQLAlchemy database instance (optional)
    """
    # Initialize performance monitor
    perf_monitor = PerformanceMonitor(app)
    
    @app.route('/api/metrics', methods=['GET'])
    def get_metrics():
        """Get comprehensive metrics"""
        metrics = {
            'system': SystemMetrics.get_all_metrics(),
            'api': api_metrics.get_stats(),
            'cache': cache_metrics.get_stats()
        }
        
        if db:
            metrics['database'] = DatabaseMetrics.get_connection_pool_stats(db)
        
        return metrics
    
    @app.route('/api/health/metrics', methods=['GET'])
    def health_metrics():
        """Get health check metrics"""
        system = SystemMetrics.get_all_metrics()
        
        # Determine health status
        health_status = 'healthy'
        issues = []
        
        # Check CPU usage
        if system['cpu'] > 80:
            health_status = 'degraded'
            issues.append('High CPU usage')
        
        # Check memory usage
        if system['memory']['percent'] > 80:
            health_status = 'degraded'
            issues.append('High memory usage')
        
        # Check disk usage
        if system['disk']['percent'] > 90:
            health_status = 'critical'
            issues.append('Low disk space')
        
        return {
            'status': health_status,
            'issues': issues,
            'metrics': system
        }
    
    return perf_monitor
