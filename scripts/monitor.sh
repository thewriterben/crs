#!/bin/bash
# Continuous monitoring script for Cryptons.com
# Usage: ./scripts/monitor.sh [--interval <seconds>] [--once]

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
INTERVAL=60
RUN_ONCE=false
LOG_FILE="${PROJECT_ROOT}/monitor.log"

usage() {
    echo "Usage: $0 [OPTIONS]"
    echo "Options:"
    echo "  --interval <secs>  Polling interval in seconds (default: 60)"
    echo "  --once             Run a single check and exit"
    echo "  --log <file>       Log file path (default: ./monitor.log)"
    echo "  -h, --help         Show this help message"
    exit 0
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        --interval) INTERVAL="$2"; shift 2 ;;
        --once) RUN_ONCE=true; shift ;;
        --log) LOG_FILE="$2"; shift 2 ;;
        -h|--help) usage ;;
        *) echo "Unknown option: $1"; usage ;;
    esac
done

log() {
    local msg="[$(date '+%Y-%m-%d %H:%M:%S')] $1"
    echo -e "${GREEN}${msg}${NC}"
    echo "$msg" >> "$LOG_FILE"
}

warn() {
    local msg="[$(date '+%Y-%m-%d %H:%M:%S')] WARNING: $1"
    echo -e "${YELLOW}${msg}${NC}"
    echo "$msg" >> "$LOG_FILE"
}

alert() {
    local msg="[$(date '+%Y-%m-%d %H:%M:%S')] ALERT: $1"
    echo -e "${RED}${msg}${NC}"
    echo "$msg" >> "$LOG_FILE"
}

check_http() {
    local name="$1"
    local url="$2"
    local expected="${3:-200}"
    local code
    code=$(curl -s -o /dev/null -w "%{http_code}" --max-time 5 "$url" 2>/dev/null || echo "000")
    if [ "$code" = "$expected" ]; then
        log "✅ ${name}: HTTP ${code}"
        return 0
    else
        alert "❌ ${name}: HTTP ${code} (expected ${expected}) — URL: ${url}"
        return 1
    fi
}

check_container() {
    local name="$1"
    if docker ps --format '{{.Names}}' 2>/dev/null | grep -q "^${name}$"; then
        log "✅ Container ${name}: running"
        return 0
    else
        alert "❌ Container ${name}: not running"
        return 1
    fi
}

run_checks() {
    local failures=0

    echo -e "${BLUE}========================================${NC}"
    log "🔍 Monitor check starting..."

    # Container health
    check_container "cryptons-backend"  || ((failures++)) || true
    check_container "cryptons-frontend" || ((failures++)) || true
    check_container "cryptons-redis"    || ((failures++)) || true
    check_container "cryptons-postgres" || ((failures++)) || true

    # API health
    check_http "Backend liveness"  "http://localhost:5000/health"       "200" || ((failures++)) || true
    check_http "Backend readiness" "http://localhost:5000/health/ready"  "200" || ((failures++)) || true
    check_http "Frontend"          "http://localhost:80/"                "200" || ((failures++)) || true

    # Disk space
    DISK_USED=$(df -h / | awk 'NR==2{print $5}' | tr -d '%')
    if [ "$DISK_USED" -gt 90 ] 2>/dev/null; then
        alert "Disk usage at ${DISK_USED}% — consider cleanup"
        ((failures++)) || true
    else
        log "💿 Disk usage: ${DISK_USED}%"
    fi

    # Memory
    if command -v free &>/dev/null; then
        MEM_TOTAL=$(free -m | awk '/Mem:/{print $2}')
        MEM_USED=$(free -m  | awk '/Mem:/{print $3}')
        MEM_PCT=$(( MEM_USED * 100 / MEM_TOTAL ))
        if [ "$MEM_PCT" -gt 90 ]; then
            warn "Memory usage at ${MEM_PCT}% (${MEM_USED}MB / ${MEM_TOTAL}MB)"
        else
            log "🧠 Memory: ${MEM_PCT}% (${MEM_USED}MB / ${MEM_TOTAL}MB)"
        fi
    fi

    if [ "$failures" -gt 0 ]; then
        alert "Monitor check completed with ${failures} failure(s)"
    else
        log "✅ All checks passed"
    fi

    return $failures
}

if [ "$RUN_ONCE" = true ]; then
    run_checks
    exit $?
fi

log "🚀 Starting continuous monitoring (interval: ${INTERVAL}s, log: ${LOG_FILE})"
log "Press Ctrl+C to stop"

while true; do
    run_checks || true
    sleep "$INTERVAL"
done
