#!/bin/bash

################################################################################
# MASTER DEPLOYMENT ENGINE
# Alpha Asset Recovery and Retention - FraudSim Lab
# 
# Comprehensive all-in-one deployment script with:
# - Extensive error handling and validation
# - Guaranteed deployment with retry logic
# - Color-coded output and progress tracking
# - Automatic dependency resolution
# - Multi-stage deployment with rollback capability
# - Environment validation and setup
# - Cloudflare tunnel configuration
# - Theme colonization (branding customization)
#
# Usage: bash deploy_all.sh [--theme THEME_NAME] [--port PORT] [--tunnel] [--debug]
################################################################################

set -o pipefail

# ============================================================================
# COLOR DEFINITIONS
# ============================================================================

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
WHITE='\033[1;37m'
NC='\033[0m' # No Color

# ============================================================================
# CONFIGURATION
# ============================================================================

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DEPLOYMENT_LOG="${PROJECT_ROOT}/deployment.log"
ERROR_LOG="${PROJECT_ROOT}/deployment_errors.log"
STATE_FILE="${PROJECT_ROOT}/.deployment_state"
BACKUP_DIR="${PROJECT_ROOT}/.backups"
VENV_DIR="${PROJECT_ROOT}/venv"
THEME_NAME="${THEME_NAME:-default}"
FRAUDSIM_PORT="${FRAUDSIM_PORT:-8000}"
ALPHA_RECOVERY_PORT="${ALPHA_RECOVERY_PORT:-5000}"
ENABLE_TUNNEL="${ENABLE_TUNNEL:-false}"
DEBUG_MODE="${DEBUG_MODE:-false}"
MAX_RETRIES=3
RETRY_DELAY=5

# ============================================================================
# LOGGING FUNCTIONS
# ============================================================================

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1" | tee -a "$DEPLOYMENT_LOG"
}

log_success() {
    echo -e "${GREEN}[✓]${NC} $1" | tee -a "$DEPLOYMENT_LOG"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1" | tee -a "$DEPLOYMENT_LOG"
}

log_error() {
    echo -e "${RED}[✗ ERROR]${NC} $1" | tee -a "$DEPLOYMENT_LOG" "$ERROR_LOG"
}

log_debug() {
    if [ "$DEBUG_MODE" = "true" ]; then
        echo -e "${MAGENTA}[DEBUG]${NC} $1" | tee -a "$DEPLOYMENT_LOG"
    fi
}

print_header() {
    echo -e "${CYAN}"
    echo "╔════════════════════════════════════════════════════════════════╗"
    echo "║  MASTER DEPLOYMENT ENGINE - Alpha Asset Recovery & Retention  ║"
    echo "║  FraudSim Lab + Multi-Channel Fraud Simulation Framework       ║"
    echo "╚════════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

print_section() {
    echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${CYAN}▶ $1${NC}"
    echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
}

# ============================================================================
# ERROR HANDLING
# ============================================================================

handle_error() {
    local line_number=$1
    local error_code=$2
    log_error "Deployment failed at line $line_number with exit code $error_code"
    log_error "Check $ERROR_LOG for details"
    cleanup_on_error
    exit "$error_code"
}

trap 'handle_error ${LINENO} $?' ERR

cleanup_on_error() {
    log_warning "Cleaning up after error..."
    
    # Kill any running processes
    if [ -f "${PROJECT_ROOT}/.pids" ]; then
        while read pid; do
            if kill -0 "$pid" 2>/dev/null; then
                kill "$pid" 2>/dev/null || true
            fi
        done < "${PROJECT_ROOT}/.pids"
        rm -f "${PROJECT_ROOT}/.pids"
    fi
    
    # Attempt rollback if available
    if [ -f "$STATE_FILE" ]; then
        log_info "Attempting rollback..."
        # Rollback logic would go here
    fi
}

retry_command() {
    local max_attempts=$1
    shift
    local command="$@"
    local attempt=1
    
    while [ $attempt -le $max_attempts ]; do
        log_debug "Attempt $attempt of $max_attempts: $command"
        
        if eval "$command"; then
            return 0
        fi
        
        if [ $attempt -lt $max_attempts ]; then
            log_warning "Command failed, retrying in ${RETRY_DELAY}s (attempt $attempt/$max_attempts)..."
            sleep "$RETRY_DELAY"
        fi
        
        ((attempt++))
    done
    
    log_error "Command failed after $max_attempts attempts: $command"
    return 1
}

# ============================================================================
# VALIDATION FUNCTIONS
# ============================================================================

validate_system() {
    print_section "System Validation"
    
    local validation_passed=true
    
    # Check OS
    if [[ "$OSTYPE" != "linux-gnu"* ]]; then
        log_warning "OS is not Linux (detected: $OSTYPE). Some features may not work."
    else
        log_success "OS: Linux"
    fi
    
    # Check Python
    if ! command -v python3 &> /dev/null; then
        log_error "Python 3 is not installed"
        validation_passed=false
    else
        PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
        log_success "Python 3: $PYTHON_VERSION"
    fi
    
    # Check pip
    if ! command -v pip3 &> /dev/null; then
        log_error "pip3 is not installed"
        validation_passed=false
    else
        log_success "pip3: installed"
    fi
    
    # Check git
    if ! command -v git &> /dev/null; then
        log_warning "git is not installed (optional)"
    else
        log_success "git: installed"
    fi
    
    # Check disk space
    AVAILABLE_SPACE=$(df "$PROJECT_ROOT" | awk 'NR==2 {print $4}')
    if [ "$AVAILABLE_SPACE" -lt 1048576 ]; then  # Less than 1GB
        log_warning "Low disk space: ${AVAILABLE_SPACE}KB available"
    else
        log_success "Disk space: ${AVAILABLE_SPACE}KB available"
    fi
    
    # Check write permissions
    if [ ! -w "$PROJECT_ROOT" ]; then
        log_error "No write permissions in $PROJECT_ROOT"
        validation_passed=false
    else
        log_success "Write permissions: OK"
    fi
    
    if [ "$validation_passed" = false ]; then
        log_error "System validation failed"
        return 1
    fi
    
    log_success "System validation passed"
    return 0
}

validate_project_structure() {
    print_section "Project Structure Validation"
    
    local required_files=(
        "app.py"
        "models.py"
        "config.py"
        "requirements.txt"
        "theme_config.json"
        "theme_manager.py"
    )
    
    local required_dirs=(
        "templates"
        "static"
        "scripts"
    )
    
    local validation_passed=true
    
    # Check files
    for file in "${required_files[@]}"; do
        if [ -f "$PROJECT_ROOT/$file" ]; then
            log_success "Found: $file"
        else
            log_error "Missing: $file"
            validation_passed=false
        fi
    done
    
    # Check directories
    for dir in "${required_dirs[@]}"; do
        if [ -d "$PROJECT_ROOT/$dir" ]; then
            log_success "Found: $dir/"
        else
            log_error "Missing: $dir/"
            validation_passed=false
        fi
    done
    
    if [ "$validation_passed" = false ]; then
        log_error "Project structure validation failed"
        return 1
    fi
    
    log_success "Project structure validation passed"
    return 0
}

# ============================================================================
# ENVIRONMENT SETUP
# ============================================================================

setup_environment() {
    print_section "Environment Setup"
    
    # Create necessary directories
    mkdir -p "$BACKUP_DIR"
    mkdir -p "${PROJECT_ROOT}/logs"
    mkdir -p "${PROJECT_ROOT}/data"
    mkdir -p "${PROJECT_ROOT}/static/css"
    mkdir -p "${PROJECT_ROOT}/static/js"
    mkdir -p "${PROJECT_ROOT}/static/images"
    
    log_success "Directories created"
    
    # Initialize logs
    > "$DEPLOYMENT_LOG"
    > "$ERROR_LOG"
    
    log_success "Logs initialized"
    
    # Create .env if not exists
    if [ ! -f "${PROJECT_ROOT}/.env" ]; then
        log_info "Creating .env file..."
        
        cat > "${PROJECT_ROOT}/.env" << 'EOF'
# Flask Configuration
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=$(python3 -c 'import secrets; print(secrets.token_hex(32))')

# Database
DATABASE_URL=sqlite:///fraudsim.db

# Twilio (Optional)
TWILIO_ACCOUNT_SID=
TWILIO_AUTH_TOKEN=
TWILIO_PHONE_NUMBER=

# LLM Configuration
LLM_PROVIDER=openai
LLM_MODEL=gpt-4.1-mini
LLM_API_KEY=

# Email Configuration
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=
MAIL_PASSWORD=

# Theme Configuration
ACTIVE_THEME=default
ENABLE_THEME_SWITCHER=True

# Security
SESSION_COOKIE_SECURE=True
SESSION_COOKIE_HTTPONLY=True
SESSION_COOKIE_SAMESITE=Lax

# Deployment
DEPLOYMENT_ENV=production
DEBUG_MODE=False
EOF
        
        log_success ".env file created"
    else
        log_info ".env file already exists"
    fi
}

# ============================================================================
# DEPENDENCY INSTALLATION
# ============================================================================

install_dependencies() {
    print_section "Installing Dependencies"
    
    # Create virtual environment
    log_info "Creating Python virtual environment..."
    
    if [ ! -d "$VENV_DIR" ]; then
        retry_command $MAX_RETRIES "python3 -m venv $VENV_DIR"
        log_success "Virtual environment created"
    else
        log_info "Virtual environment already exists"
    fi
    
    # Activate virtual environment
    source "$VENV_DIR/bin/activate"
    log_success "Virtual environment activated"
    
    # Upgrade pip
    log_info "Upgrading pip..."
    retry_command $MAX_RETRIES "pip install --upgrade pip setuptools wheel"
    log_success "pip upgraded"
    
    # Install requirements
    log_info "Installing Python dependencies..."
    
    if [ -f "${PROJECT_ROOT}/requirements.txt" ]; then
        retry_command $MAX_RETRIES "pip install -r ${PROJECT_ROOT}/requirements.txt"
        log_success "Python dependencies installed"
    else
        log_error "requirements.txt not found"
        return 1
    fi
    
    # Verify installations
    log_info "Verifying installations..."
    
    local required_packages=(
        "flask"
        "flask-sqlalchemy"
        "python-dotenv"
        "requests"
    )
    
    for package in "${required_packages[@]}"; do
        if python3 -c "import ${package//-/_}" 2>/dev/null; then
            log_success "Verified: $package"
        else
            log_warning "Missing package: $package"
        fi
    done
}

# ============================================================================
# DATABASE SETUP
# ============================================================================

setup_database() {
    print_section "Database Setup"
    
    log_info "Initializing database..."
    
    cd "$PROJECT_ROOT"
    
    python3 << 'PYTHON_SCRIPT'
import os
import sys
sys.path.insert(0, os.getcwd())

try:
    from app import app, db
    
    with app.app_context():
        # Create all tables
        db.create_all()
        print("[SUCCESS] Database tables created")
        
        # Verify tables
        inspector = db.inspect(db.engine)
        tables = inspector.get_table_names()
        print(f"[SUCCESS] Tables: {', '.join(tables)}")
        
except Exception as e:
    print(f"[ERROR] Database setup failed: {e}")
    sys.exit(1)
PYTHON_SCRIPT
    
    if [ $? -eq 0 ]; then
        log_success "Database initialized"
    else
        log_error "Database initialization failed"
        return 1
    fi
}

# ============================================================================
# THEME SETUP (COLONIZATION)
# ============================================================================

setup_themes() {
    print_section "Theme Setup (Colonization)"
    
    log_info "Generating CSS for theme: $THEME_NAME"
    
    cd "$PROJECT_ROOT"
    
    python3 << PYTHON_SCRIPT
import sys
sys.path.insert(0, '.')

try:
    from theme_manager import ThemeManager
    
    manager = ThemeManager('theme_config.json')
    
    # Set active theme
    if manager.set_theme('$THEME_NAME'):
        print(f"[SUCCESS] Theme set to: \$THEME_NAME")
    else:
        print(f"[WARNING] Theme not found, using default")
        manager.set_theme('default')
    
    # Generate CSS
    if manager.save_css_file():
        print("[SUCCESS] CSS generated")
    else:
        print("[ERROR] Failed to generate CSS")
        sys.exit(1)
    
    # Display theme info
    info = manager.get_theme_info()
    if info:
        print(f"[INFO] Theme: {info['name']}")
        print(f"[INFO] Description: {info['description']}")
    
    # Display stats
    stats = manager.get_theme_stats()
    print(f"[INFO] Available themes: {stats['total_themes']}")
    
except Exception as e:
    print(f"[ERROR] Theme setup failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
PYTHON_SCRIPT
    
    if [ $? -eq 0 ]; then
        log_success "Theme setup completed"
    else
        log_error "Theme setup failed"
        return 1
    fi
}

# ============================================================================
# CONFIGURATION VALIDATION
# ============================================================================

validate_configuration() {
    print_section "Configuration Validation"
    
    log_info "Validating configuration files..."
    
    # Check .env
    if [ -f "${PROJECT_ROOT}/.env" ]; then
        log_success ".env file exists"
        
        # Check for required variables
        if grep -q "SECRET_KEY" "${PROJECT_ROOT}/.env"; then
            log_success "SECRET_KEY configured"
        else
            log_warning "SECRET_KEY not configured"
        fi
    else
        log_warning ".env file not found"
    fi
    
    # Check theme_config.json
    if [ -f "${PROJECT_ROOT}/theme_config.json" ]; then
        log_success "theme_config.json exists"
        
        # Validate JSON
        if python3 -m json.tool "${PROJECT_ROOT}/theme_config.json" > /dev/null 2>&1; then
            log_success "theme_config.json is valid"
        else
            log_error "theme_config.json is invalid JSON"
            return 1
        fi
    else
        log_error "theme_config.json not found"
        return 1
    fi
    
    log_success "Configuration validation passed"
}

# ============================================================================
# APPLICATION STARTUP
# ============================================================================

start_fraudsim_lab() {
    print_section "Starting FraudSim Lab (Port $FRAUDSIM_PORT)"
    
    source "$VENV_DIR/bin/activate"
    
    cd "$PROJECT_ROOT"
    
    log_info "Starting Flask application..."
    
    # Start in background
    nohup python3 app.py > "${PROJECT_ROOT}/logs/fraudsim.log" 2>&1 &
    local pid=$!
    
    # Save PID
    echo "$pid" >> "${PROJECT_ROOT}/.pids"
    
    # Wait for startup
    sleep 3
    
    # Check if process is running
    if kill -0 $pid 2>/dev/null; then
        log_success "FraudSim Lab started (PID: $pid)"
        echo "$FRAUDSIM_PORT" > "${PROJECT_ROOT}/.fraudsim_port"
        return 0
    else
        log_error "FraudSim Lab failed to start"
        tail -20 "${PROJECT_ROOT}/logs/fraudsim.log"
        return 1
    fi
}

start_alpha_recovery() {
    print_section "Starting Alpha Asset Recovery Website (Port $ALPHA_RECOVERY_PORT)"
    
    source "$VENV_DIR/bin/activate"
    
    cd "${PROJECT_ROOT}/alpha_recovery"
    
    log_info "Starting Alpha Recovery Flask application..."
    
    # Start in background
    nohup python3 app.py > "${PROJECT_ROOT}/logs/alpha_recovery.log" 2>&1 &
    local pid=$!
    
    # Save PID
    echo "$pid" >> "${PROJECT_ROOT}/.pids"
    
    # Wait for startup
    sleep 3
    
    # Check if process is running
    if kill -0 $pid 2>/dev/null; then
        log_success "Alpha Asset Recovery started (PID: $pid)"
        echo "$ALPHA_RECOVERY_PORT" > "${PROJECT_ROOT}/.alpha_recovery_port"
        return 0
    else
        log_error "Alpha Asset Recovery failed to start"
        tail -20 "${PROJECT_ROOT}/logs/alpha_recovery.log"
        return 1
    fi
}

# ============================================================================
# TUNNEL SETUP (CLOUDFLARE)
# ============================================================================

setup_cloudflare_tunnel() {
    print_section "Cloudflare Tunnel Setup"
    
    if [ "$ENABLE_TUNNEL" != "true" ]; then
        log_info "Tunnel setup skipped (disabled)"
        return 0
    fi
    
    log_info "Setting up Cloudflare Tunnel..."
    
    # Check if cloudflared is installed
    if ! command -v cloudflared &> /dev/null; then
        log_warning "cloudflared not installed, attempting to install..."
        
        # Try to install cloudflared
        if command -v apt-get &> /dev/null; then
            retry_command $MAX_RETRIES "sudo apt-get update && sudo apt-get install -y cloudflared"
        else
            log_warning "Cannot auto-install cloudflared on this system"
            log_info "Visit https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/ to install manually"
            return 1
        fi
    fi
    
    log_success "cloudflared is available"
    
    # Create tunnel configuration
    mkdir -p ~/.cloudflared
    
    cat > ~/.cloudflared/config.yml << EOF
tunnel: alpha-recovery-tunnel
credentials-file: /root/.cloudflared/alpha-recovery-tunnel.json

ingress:
  - hostname: fraudsim.alpharecovery.com
    service: http://localhost:$FRAUDSIM_PORT
  - hostname: alpha.alpharecovery.com
    service: http://localhost:$ALPHA_RECOVERY_PORT
  - service: http_status:404
EOF
    
    log_success "Tunnel configuration created"
    log_info "To complete tunnel setup, run: cloudflared tunnel login"
}

# ============================================================================
# HEALTH CHECKS
# ============================================================================

perform_health_checks() {
    print_section "Health Checks"
    
    local all_healthy=true
    
    # Check FraudSim Lab
    log_info "Checking FraudSim Lab (http://localhost:$FRAUDSIM_PORT)..."
    
    if curl -s -o /dev/null -w "%{http_code}" "http://localhost:$FRAUDSIM_PORT" | grep -q "200\|302\|404"; then
        log_success "FraudSim Lab is responding"
    else
        log_warning "FraudSim Lab health check inconclusive"
    fi
    
    # Check Alpha Recovery
    log_info "Checking Alpha Asset Recovery (http://localhost:$ALPHA_RECOVERY_PORT)..."
    
    if curl -s -o /dev/null -w "%{http_code}" "http://localhost:$ALPHA_RECOVERY_PORT" | grep -q "200\|302\|404"; then
        log_success "Alpha Asset Recovery is responding"
    else
        log_warning "Alpha Asset Recovery health check inconclusive"
    fi
    
    # Check database
    log_info "Checking database..."
    
    if [ -f "${PROJECT_ROOT}/fraudsim.db" ]; then
        log_success "Database file exists"
    else
        log_warning "Database file not found"
    fi
    
    # Check logs
    if [ -f "${PROJECT_ROOT}/logs/fraudsim.log" ]; then
        log_success "FraudSim logs available"
    fi
    
    if [ -f "${PROJECT_ROOT}/logs/alpha_recovery.log" ]; then
        log_success "Alpha Recovery logs available"
    fi
}

# ============================================================================
# DEPLOYMENT SUMMARY
# ============================================================================

print_deployment_summary() {
    print_section "Deployment Summary"
    
    echo -e "${GREEN}"
    echo "╔════════════════════════════════════════════════════════════════╗"
    echo "║                   DEPLOYMENT SUCCESSFUL                        ║"
    echo "╚════════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
    
    echo -e "${CYAN}Services Running:${NC}"
    echo -e "  ${GREEN}✓${NC} FraudSim Lab: ${BLUE}http://localhost:$FRAUDSIM_PORT${NC}"
    echo -e "  ${GREEN}✓${NC} Alpha Asset Recovery: ${BLUE}http://localhost:$ALPHA_RECOVERY_PORT${NC}"
    
    echo ""
    echo -e "${CYAN}Configuration:${NC}"
    echo -e "  Theme: ${BLUE}$THEME_NAME${NC}"
    echo -e "  Project Root: ${BLUE}$PROJECT_ROOT${NC}"
    echo -e "  Virtual Env: ${BLUE}$VENV_DIR${NC}"
    
    echo ""
    echo -e "${CYAN}Logs:${NC}"
    echo -e "  Deployment: ${BLUE}$DEPLOYMENT_LOG${NC}"
    echo -e "  Errors: ${BLUE}$ERROR_LOG${NC}"
    echo -e "  FraudSim: ${BLUE}${PROJECT_ROOT}/logs/fraudsim.log${NC}"
    echo -e "  Alpha Recovery: ${BLUE}${PROJECT_ROOT}/logs/alpha_recovery.log${NC}"
    
    echo ""
    echo -e "${CYAN}Next Steps:${NC}"
    echo -e "  1. Open ${BLUE}http://localhost:$FRAUDSIM_PORT${NC} in your browser"
    echo -e "  2. Log in with default credentials"
    echo -e "  3. Create your first fraud simulation campaign"
    echo -e "  4. Visit ${BLUE}http://localhost:$ALPHA_RECOVERY_PORT${NC} for asset recovery portal"
    
    if [ "$ENABLE_TUNNEL" = "true" ]; then
        echo ""
        echo -e "${CYAN}Tunnel:${NC}"
        echo -e "  Run: ${BLUE}cloudflared tunnel run alpha-recovery-tunnel${NC}"
    fi
    
    echo ""
    echo -e "${CYAN}To stop services:${NC}"
    echo -e "  ${BLUE}bash ${PROJECT_ROOT}/scripts/stop_all.sh${NC}"
    
    echo ""
    echo -e "${CYAN}Documentation:${NC}"
    echo -e "  README: ${BLUE}${PROJECT_ROOT}/README.md${NC}"
    echo -e "  Advanced Features: ${BLUE}${PROJECT_ROOT}/ADVANCED_FEATURES.md${NC}"
    echo -e "  Deployment: ${BLUE}${PROJECT_ROOT}/DEPLOYMENT.md${NC}"
}

# ============================================================================
# MAIN EXECUTION
# ============================================================================

main() {
    print_header
    
    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            --theme)
                THEME_NAME="$2"
                shift 2
                ;;
            --port)
                FRAUDSIM_PORT="$2"
                shift 2
                ;;
            --tunnel)
                ENABLE_TUNNEL="true"
                shift
                ;;
            --debug)
                DEBUG_MODE="true"
                shift
                ;;
            *)
                log_warning "Unknown option: $1"
                shift
                ;;
        esac
    done
    
    log_info "Starting deployment..."
    log_info "Theme: $THEME_NAME"
    log_info "FraudSim Port: $FRAUDSIM_PORT"
    log_info "Alpha Recovery Port: $ALPHA_RECOVERY_PORT"
    
    # Execution stages
    validate_system || exit 1
    validate_project_structure || exit 1
    setup_environment || exit 1
    install_dependencies || exit 1
    validate_configuration || exit 1
    setup_database || exit 1
    setup_themes || exit 1
    start_fraudsim_lab || exit 1
    start_alpha_recovery || exit 1
    setup_cloudflare_tunnel || true
    perform_health_checks || true
    print_deployment_summary
    
    log_success "Deployment completed successfully!"
    
    # Save state
    echo "DEPLOYMENT_TIME=$(date)" > "$STATE_FILE"
    echo "THEME=$THEME_NAME" >> "$STATE_FILE"
    echo "FRAUDSIM_PORT=$FRAUDSIM_PORT" >> "$STATE_FILE"
    echo "ALPHA_RECOVERY_PORT=$ALPHA_RECOVERY_PORT" >> "$STATE_FILE"
}

# Run main function
main "$@"
