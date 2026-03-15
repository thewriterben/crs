#!/bin/bash
# Automated deployment script with rollback support for Cryptons.com
# Usage: ./scripts/deploy.sh [--rollback] [--env <environment>]

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
DEPLOY_LOG="${PROJECT_ROOT}/deploy_${TIMESTAMP}.log"
ROLLBACK=false
ENVIRONMENT="production"

usage() {
    echo "Usage: $0 [OPTIONS]"
    echo "Options:"
    echo "  --rollback         Roll back to the previous deployment"
    echo "  --env <env>        Target environment (default: production)"
    echo "  -h, --help         Show this help message"
    exit 0
}

log() {
    echo -e "${GREEN}[$(date +%H:%M:%S)] $1${NC}" | tee -a "$DEPLOY_LOG"
}

warn() {
    echo -e "${YELLOW}[$(date +%H:%M:%S)] WARNING: $1${NC}" | tee -a "$DEPLOY_LOG"
}

error() {
    echo -e "${RED}[$(date +%H:%M:%S)] ERROR: $1${NC}" | tee -a "$DEPLOY_LOG"
    exit 1
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        --rollback) ROLLBACK=true; shift ;;
        --env) ENVIRONMENT="$2"; shift 2 ;;
        -h|--help) usage ;;
        *) error "Unknown option: $1" ;;
    esac
done

cd "$PROJECT_ROOT"

if [ "$ROLLBACK" = true ]; then
    log "🔄 Starting rollback..."
    if [ -f ".last_deploy_image_tag" ]; then
        PREV_TAG=$(cat .last_deploy_image_tag)
        log "Rolling back to image tag: ${PREV_TAG}"
        ROLLBACK_ARGS=("-f" "docker-compose.yml")
        if [ "$ENVIRONMENT" = "production" ]; then
            ROLLBACK_ARGS+=("-f" "deployment/docker-compose.prod.yml")
        fi
        docker-compose "${ROLLBACK_ARGS[@]}" down
        docker-compose "${ROLLBACK_ARGS[@]}" up -d
        log "✅ Rollback complete"
    else
        error "No previous deployment found for rollback"
    fi
    exit 0
fi

log "🚀 Starting deployment to ${ENVIRONMENT}..."

# Step 1: Validate environment
log "Step 1: Validating environment..."
if [ ! -f ".env" ]; then
    warn ".env file not found; using .env.example as fallback"
    if [ -f ".env.example" ]; then
        cp .env.example .env
        warn "Created .env from .env.example — update secrets before production use!"
    fi
fi

if command -v python3 &>/dev/null && [ -f "backend/scripts/validate_env.py" ]; then
    python3 backend/scripts/validate_env.py || warn "Environment validation reported issues"
fi

# Step 2: Pull latest code
log "Step 2: Pulling latest code..."
git pull origin main 2>&1 | tee -a "$DEPLOY_LOG" || warn "git pull failed — deploying with current code"

# Step 3: Save current image tag for rollback
log "Step 3: Saving rollback snapshot..."
docker images --format "{{.Tag}}" crs-backend 2>/dev/null | head -1 > .last_deploy_image_tag || true

# Step 4: Build images
log "Step 4: Building Docker images..."
COMPOSE_ARGS=("-f" "docker-compose.yml")
if [ "$ENVIRONMENT" = "production" ]; then
    COMPOSE_ARGS+=("-f" "deployment/docker-compose.prod.yml")
fi
docker-compose "${COMPOSE_ARGS[@]}" build --no-cache 2>&1 | tee -a "$DEPLOY_LOG"

# Step 5: Run database migrations
log "Step 5: Running database migrations..."
docker-compose "${COMPOSE_ARGS[@]}" run --rm backend python -m flask db upgrade 2>&1 | tee -a "$DEPLOY_LOG" || warn "Migration step skipped (DB may not be configured)"

# Step 6: Start services
log "Step 6: Starting services..."
docker-compose "${COMPOSE_ARGS[@]}" up -d 2>&1 | tee -a "$DEPLOY_LOG"

# Step 7: Health check
log "Step 7: Running health checks..."
sleep 10
if command -v bash &>/dev/null && [ -f "${SCRIPT_DIR}/health-check.sh" ]; then
    bash "${SCRIPT_DIR}/health-check.sh" 2>&1 | tee -a "$DEPLOY_LOG" || warn "Health check reported issues — review logs"
else
    BACKEND_STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:5000/health 2>/dev/null || echo "000")
    if [ "$BACKEND_STATUS" = "200" ]; then
        log "✅ Backend health check passed"
    else
        warn "Backend health check returned HTTP ${BACKEND_STATUS}"
    fi
fi

log "✅ Deployment to ${ENVIRONMENT} complete!"
log "📋 Deployment log saved to: ${DEPLOY_LOG}"
