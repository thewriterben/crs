#!/bin/bash
# Update dependencies for Cryptons.com (frontend npm + backend pip)
# Usage: ./scripts/update.sh [--frontend] [--backend] [--all]

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
DO_FRONTEND=false
DO_BACKEND=false

usage() {
    echo "Usage: $0 [OPTIONS]"
    echo "Options:"
    echo "  --frontend   Update frontend (npm) dependencies"
    echo "  --backend    Update backend (pip) dependencies"
    echo "  --all        Update both frontend and backend (default if no option given)"
    echo "  -h, --help   Show this help message"
    exit 0
}

log() { echo -e "${GREEN}[$(date +%H:%M:%S)] $1${NC}"; }
warn() { echo -e "${YELLOW}[$(date +%H:%M:%S)] WARNING: $1${NC}"; }
error() { echo -e "${RED}[$(date +%H:%M:%S)] ERROR: $1${NC}"; exit 1; }

while [[ $# -gt 0 ]]; do
    case "$1" in
        --frontend) DO_FRONTEND=true; shift ;;
        --backend)  DO_BACKEND=true;  shift ;;
        --all)      DO_FRONTEND=true; DO_BACKEND=true; shift ;;
        -h|--help)  usage ;;
        *) error "Unknown option: $1" ;;
    esac
done

# Default: update both if no flag given
if [ "$DO_FRONTEND" = false ] && [ "$DO_BACKEND" = false ]; then
    DO_FRONTEND=true
    DO_BACKEND=true
fi

cd "$PROJECT_ROOT"

if [ "$DO_FRONTEND" = true ]; then
    log "📦 Updating frontend dependencies..."
    cd "${PROJECT_ROOT}/frontend"
    npm update 2>&1
    npm audit fix 2>&1 || warn "npm audit fix reported issues that may require manual review"
    log "✅ Frontend dependencies updated"
    cd "$PROJECT_ROOT"
fi

if [ "$DO_BACKEND" = true ]; then
    log "🐍 Updating backend dependencies..."
    if [ -d "${PROJECT_ROOT}/backend/venv" ]; then
        # shellcheck disable=SC1091
        source "${PROJECT_ROOT}/backend/venv/bin/activate" 2>/dev/null || true
    fi
    pip install --upgrade pip -q
    pip install --upgrade -r "${PROJECT_ROOT}/backend/requirements.txt" -q \
        && log "✅ Backend dependencies updated" \
        || warn "Some backend packages could not be upgraded — check requirements.txt"
fi

log "✅ Dependency update complete"
