#!/bin/bash
# Start Phase 3 API Server

echo "Starting Phase 3 API Server..."
echo "================================"
echo ""

# Set Python path
export PYTHONPATH=/home/runner/work/crs/crs/backend

# Navigate to backend
cd "$(dirname "$0")/../backend"

# Start the server
python3 api/phase3_api.py
