#!/bin/bash
# Restore from a Cryptons.com backup archive
# Usage: ./scripts/restore.sh --backup <path/to/backup_TIMESTAMP.tar.gz>

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
BACKUP_FILE=""

usage() {
    echo "Usage: $0 --backup <path/to/backup.tar.gz>"
    echo "Options:"
    echo "  --backup <file>  Path to the backup archive to restore"
    echo "  -h, --help       Show this help message"
    exit 0
}

log() { echo -e "${GREEN}[$(date +%H:%M:%S)] $1${NC}"; }
warn() { echo -e "${YELLOW}[$(date +%H:%M:%S)] WARNING: $1${NC}"; }
error() { echo -e "${RED}[$(date +%H:%M:%S)] ERROR: $1${NC}"; exit 1; }

while [[ $# -gt 0 ]]; do
    case "$1" in
        --backup) BACKUP_FILE="$2"; shift 2 ;;
        -h|--help) usage ;;
        *) error "Unknown option: $1" ;;
    esac
done

[ -z "$BACKUP_FILE" ] && error "No backup file specified. Use: $0 --backup <file>"
[ ! -f "$BACKUP_FILE" ] && error "Backup file not found: $BACKUP_FILE"

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
REDIS_CONTAINER="${REDIS_CONTAINER:-cryptons-redis}"

RESTORE_TMP=$(mktemp -d)
trap 'rm -rf "$RESTORE_TMP"' EXIT

log "📦 Extracting backup archive: ${BACKUP_FILE}"
tar -xzf "$BACKUP_FILE" -C "$RESTORE_TMP"
RESTORE_DIR=$(find "$RESTORE_TMP" -maxdepth 1 -type d | tail -1)

# Step 1: Restore database
log "Step 1: Restoring PostgreSQL database..."
if [ -f "${RESTORE_DIR}/database.sql" ]; then
    if docker ps --format '{{.Names}}' | grep -q "$POSTGRES_CONTAINER"; then
        docker exec -i "$POSTGRES_CONTAINER" \
            psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" \
            < "${RESTORE_DIR}/database.sql" \
            && log "✅ Database restore complete" \
            || error "Database restore failed"
    else
        warn "PostgreSQL container '${POSTGRES_CONTAINER}' not running — skipping DB restore"
    fi
else
    warn "No database.sql found in backup — skipping database restore"
fi

# Step 2: Restore Redis
log "Step 2: Restoring Redis..."
if [ -f "${RESTORE_DIR}/redis_dump.rdb" ]; then
    if docker ps --format '{{.Names}}' | grep -q "$REDIS_CONTAINER"; then
        docker cp "${RESTORE_DIR}/redis_dump.rdb" "${REDIS_CONTAINER}:/data/dump.rdb"
        docker restart "$REDIS_CONTAINER" &>/dev/null
        log "✅ Redis restore complete"
    else
        warn "Redis container '${REDIS_CONTAINER}' not running — skipping Redis restore"
    fi
else
    warn "No redis_dump.rdb found in backup — skipping Redis restore"
fi

log "✅ Restore complete"
