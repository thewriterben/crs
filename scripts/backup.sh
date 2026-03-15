#!/bin/bash
# Database and configuration backup script for Cryptons.com
# Usage: ./scripts/backup.sh [--output-dir <path>]

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="${PROJECT_ROOT}/backups"
OUTPUT_DIR=""

usage() {
    echo "Usage: $0 [OPTIONS]"
    echo "Options:"
    echo "  --output-dir <path>  Directory to store backups (default: ./backups)"
    echo "  -h, --help           Show this help message"
    exit 0
}

log() { echo -e "${GREEN}[$(date +%H:%M:%S)] $1${NC}"; }
warn() { echo -e "${YELLOW}[$(date +%H:%M:%S)] WARNING: $1${NC}"; }
error() { echo -e "${RED}[$(date +%H:%M:%S)] ERROR: $1${NC}"; exit 1; }

while [[ $# -gt 0 ]]; do
    case "$1" in
        --output-dir) OUTPUT_DIR="$2"; shift 2 ;;
        -h|--help) usage ;;
        *) error "Unknown option: $1" ;;
    esac
done

[ -n "$OUTPUT_DIR" ] && BACKUP_DIR="$OUTPUT_DIR"
BACKUP_PATH="${BACKUP_DIR}/backup_${TIMESTAMP}"
mkdir -p "$BACKUP_PATH"

cd "$PROJECT_ROOT"

# Load environment
if [ -f ".env" ]; then
    set -a
    # shellcheck disable=SC1091
    source .env
    set +a
fi

POSTGRES_USER="${POSTGRES_USER:-crs_user}"
POSTGRES_DB="${POSTGRES_DB:-crs_db}"
POSTGRES_CONTAINER="${POSTGRES_CONTAINER:-cryptons-postgres}"

log "🗄️  Starting backup to ${BACKUP_PATH}..."

# Step 1: Database backup
log "Step 1: Backing up PostgreSQL database..."
if docker ps --format '{{.Names}}' | grep -q "$POSTGRES_CONTAINER"; then
    docker exec "$POSTGRES_CONTAINER" \
        pg_dump -U "$POSTGRES_USER" "$POSTGRES_DB" \
        > "${BACKUP_PATH}/database.sql" 2>/dev/null \
        && log "✅ Database backup complete: ${BACKUP_PATH}/database.sql" \
        || warn "Database backup failed — container may not be running"
else
    warn "PostgreSQL container '${POSTGRES_CONTAINER}' not found — skipping database backup"
fi

# Step 2: Environment configuration backup (secrets masked)
log "Step 2: Backing up configuration..."
if [ -f ".env" ]; then
    sed 's/\(SECRET_KEY\|JWT_SECRET_KEY\|DATABASE_URL\|POSTGRES_PASSWORD\|REDIS_URL\)=.*/\1=<REDACTED>/' \
        .env > "${BACKUP_PATH}/config.env.masked"
    log "✅ Masked config backup: ${BACKUP_PATH}/config.env.masked"
fi
[ -f ".env.example" ] && cp .env.example "${BACKUP_PATH}/.env.example"

# Step 3: Redis data snapshot
log "Step 3: Backing up Redis..."
REDIS_CONTAINER="${REDIS_CONTAINER:-cryptons-redis}"
if docker ps --format '{{.Names}}' | grep -q "$REDIS_CONTAINER"; then
    docker exec "$REDIS_CONTAINER" redis-cli BGSAVE &>/dev/null && sleep 2
    docker cp "${REDIS_CONTAINER}:/data/dump.rdb" "${BACKUP_PATH}/redis_dump.rdb" 2>/dev/null \
        && log "✅ Redis backup complete" \
        || warn "Redis backup failed"
else
    warn "Redis container '${REDIS_CONTAINER}' not found — skipping Redis backup"
fi

# Step 4: Compress backup
log "Step 4: Compressing backup archive..."
tar -czf "${BACKUP_DIR}/backup_${TIMESTAMP}.tar.gz" -C "$BACKUP_DIR" "backup_${TIMESTAMP}"
rm -rf "$BACKUP_PATH"
log "✅ Backup archive: ${BACKUP_DIR}/backup_${TIMESTAMP}.tar.gz"

# Step 5: Clean up old backups (keep last 7)
log "Step 5: Cleaning up old backups (keeping last 7)..."
ls -t "${BACKUP_DIR}"/backup_*.tar.gz 2>/dev/null | tail -n +8 | xargs rm -f 2>/dev/null || true

log "✅ Backup complete: ${BACKUP_DIR}/backup_${TIMESTAMP}.tar.gz"
