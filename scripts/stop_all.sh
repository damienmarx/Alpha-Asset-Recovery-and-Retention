#!/bin/bash

################################################################################
# STOP ALL SERVICES
# Gracefully stops all running services
################################################################################

set -o pipefail

# Color definitions
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PIDS_FILE="${PROJECT_ROOT}/.pids"

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[✓]${NC} $1"
}

log_error() {
    echo -e "${RED}[✗]${NC} $1"
}

echo -e "${CYAN}"
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║              STOPPING ALL SERVICES                             ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Stop processes from PID file
if [ -f "$PIDS_FILE" ]; then
    log_info "Stopping processes..."
    
    while read pid; do
        if kill -0 "$pid" 2>/dev/null; then
            log_info "Stopping process $pid..."
            kill "$pid" 2>/dev/null
            
            # Wait for graceful shutdown
            sleep 2
            
            # Force kill if still running
            if kill -0 "$pid" 2>/dev/null; then
                log_info "Force killing process $pid..."
                kill -9 "$pid" 2>/dev/null
            fi
            
            log_success "Process $pid stopped"
        fi
    done < "$PIDS_FILE"
    
    rm -f "$PIDS_FILE"
else
    log_info "No PID file found"
fi

# Kill any remaining Flask processes
log_info "Checking for remaining Flask processes..."

if pgrep -f "python.*app.py" > /dev/null; then
    log_info "Found Flask processes, stopping..."
    pkill -f "python.*app.py"
    sleep 2
    log_success "Flask processes stopped"
fi

# Stop Cloudflare tunnel if running
if pgrep -f "cloudflared" > /dev/null; then
    log_info "Stopping Cloudflare tunnel..."
    pkill -f "cloudflared"
    sleep 1
    log_success "Cloudflare tunnel stopped"
fi

echo -e "${GREEN}"
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║                    ALL SERVICES STOPPED                        ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

log_success "All services have been stopped gracefully"
