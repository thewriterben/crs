#!/bin/bash
# Health check script for Cryptons.com deployment
# Run this to verify all services are running correctly

set -e

echo "🏥 Cryptons.com Health Check Starting..."
echo "=================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to check service
check_service() {
    local name=$1
    local url=$2
    local expected=$3
    
    echo -n "Checking $name... "
    
    response=$(curl -s -o /dev/null -w "%{http_code}" "$url" 2>/dev/null || echo "000")
    
    if [ "$response" = "$expected" ]; then
        echo -e "${GREEN}✓ OK${NC} (HTTP $response)"
        return 0
    else
        echo -e "${RED}✗ FAILED${NC} (HTTP $response)"
        return 1
    fi
}

# Function to check docker service
check_docker_service() {
    local service=$1
    echo -n "Checking Docker service $service... "
    
    if docker-compose ps | grep -q "$service.*Up"; then
        echo -e "${GREEN}✓ Running${NC}"
        return 0
    else
        echo -e "${RED}✗ Not Running${NC}"
        return 1
    fi
}

# Check if docker-compose is available
if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}Error: docker-compose not found${NC}"
    exit 1
fi

# Check Docker services
echo ""
echo "📦 Docker Services"
echo "------------------"
check_docker_service "backend"
check_docker_service "frontend"
check_docker_service "redis"

# Check Backend Health
echo ""
echo "🔧 Backend Health"
echo "------------------"
check_service "Backend Liveness" "http://localhost:5000/api/health/liveness" "200"
check_service "Backend Readiness" "http://localhost:5000/api/health/readiness" "200"
check_service "Backend Info" "http://localhost:5000/api/health/info" "200"

# Check Frontend
echo ""
echo "🎨 Frontend Health"
echo "------------------"
check_service "Frontend" "http://localhost:8080/health" "200"
check_service "Frontend Root" "http://localhost:8080/" "200"

# Check Redis
echo ""
echo "💾 Redis Health"
echo "------------------"
if docker-compose exec -T redis redis-cli ping | grep -q "PONG"; then
    echo -e "Redis Connection: ${GREEN}✓ OK${NC}"
else
    echo -e "Redis Connection: ${RED}✗ FAILED${NC}"
fi

# Check Database
echo ""
echo "🗄️  Database Health"
echo "------------------"
if docker-compose exec -T backend python -c "from src.models import db; from src.main import app; app.app_context().push(); db.session.execute('SELECT 1')" &>/dev/null; then
    echo -e "Database Connection: ${GREEN}✓ OK${NC}"
else
    echo -e "Database Connection: ${RED}✗ FAILED${NC}"
fi

# Check Disk Space
echo ""
echo "💿 Disk Space"
echo "------------------"
df -h / | tail -1 | awk '{print "Available: " $4 " (" $5 " used)"}'

# Check Memory
echo ""
echo "🧠 Memory Usage"
echo "------------------"
free -h | grep Mem | awk '{print "Available: " $7 " / " $2}'

# Docker Stats
echo ""
echo "📊 Container Stats"
echo "------------------"
docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}"

echo ""
echo "=================================="
echo "✅ Health check complete!"
echo ""
echo "For detailed logs, run:"
echo "  docker-compose logs -f"
echo ""
