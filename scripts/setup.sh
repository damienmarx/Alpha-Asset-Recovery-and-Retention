#!/bin/bash
set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║         FraudSim Lab - Automated Setup                     ║${NC}"
echo -e "${BLUE}║         PPP Fraud Simulation & Detection Platform          ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}✗ Python 3 not found. Please install Python 3.9+${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Python 3 found${NC}"

# Create virtual environment
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}→ Creating virtual environment...${NC}"
    python3 -m venv venv
    echo -e "${GREEN}✓ Virtual environment created${NC}"
else
    echo -e "${GREEN}✓ Virtual environment exists${NC}"
fi

# Activate venv
source venv/bin/activate
echo -e "${GREEN}✓ Virtual environment activated${NC}"

# Install dependencies
echo -e "${YELLOW}→ Installing Python dependencies...${NC}"
pip install --upgrade pip setuptools wheel > /dev/null 2>&1
pip install -r requirements.txt > /dev/null 2>&1
echo -e "${GREEN}✓ Dependencies installed${NC}"

# Create .env file
if [ ! -f ".env" ]; then
    echo ""
    echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║         Configuration Setup                                ║${NC}"
    echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
    echo ""

    # LLM Provider
    echo -e "${YELLOW}Select LLM Provider:${NC}"
    echo "1) Ollama (local, free)"
    echo "2) OpenAI (requires API key)"
    read -p "Choice (1 or 2): " llm_choice

    if [ "$llm_choice" = "2" ]; then
        LLM_PROVIDER="openai"
        read -p "Enter OpenAI API Key: " openai_key
        OPENAI_API_KEY="$openai_key"
    else
        LLM_PROVIDER="ollama"
        OPENAI_API_KEY=""
    fi

    # Twilio (optional)
    echo ""
    echo -e "${YELLOW}Twilio Configuration (optional - leave blank to skip):${NC}"
    read -p "Twilio Account SID: " twilio_sid
    if [ -n "$twilio_sid" ]; then
        read -p "Twilio Auth Token: " twilio_token
        read -p "Twilio Phone Number (+E.164): " twilio_phone
        TWILIO_ACCOUNT_SID="$twilio_sid"
        TWILIO_AUTH_TOKEN="$twilio_token"
        TWILIO_PHONE_NUMBER="$twilio_phone"
    else
        TWILIO_ACCOUNT_SID=""
        TWILIO_AUTH_TOKEN=""
        TWILIO_PHONE_NUMBER=""
    fi

    # Dashboard Customization
    echo ""
    echo -e "${YELLOW}Dashboard Customization (press Enter for defaults):${NC}"
    read -p "Dashboard Title [FraudSim Lab]: " dashboard_title
    dashboard_title="${dashboard_title:-FraudSim Lab}"
    
    read -p "Logo Text [FSL]: " logo_text
    logo_text="${logo_text:-FSL}"

    read -p "Primary Color [#0d6efd]: " primary_color
    primary_color="${primary_color:-#0d6efd}"

    read -p "Accent Color [#198754]: " accent_color
    accent_color="${accent_color:-#198754}"

    # Generate .env
    cat > .env << EOF
# FraudSim Lab Configuration
SECRET_KEY=$(openssl rand -hex 32)
APP_PORT=8000
DATABASE_URL=sqlite:///fraudlab.db

# LLM
LLM_PROVIDER=$LLM_PROVIDER
OPENAI_API_KEY=$OPENAI_API_KEY
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama2
ENABLE_LLM_DETECTION=True

# Twilio
TWILIO_ACCOUNT_SID=$TWILIO_ACCOUNT_SID
TWILIO_AUTH_TOKEN=$TWILIO_AUTH_TOKEN
TWILIO_PHONE_NUMBER=$TWILIO_PHONE_NUMBER

# Dashboard
DASHBOARD_TITLE=$dashboard_title
DASHBOARD_LOGO_TEXT=$logo_text
DASHBOARD_PRIMARY_COLOR=$primary_color
DASHBOARD_ACCENT_COLOR=$accent_color
DASHBOARD_BG_COLOR=#121212
DASHBOARD_CARD_COLOR=#1e1e2e
DASHBOARD_TEXT_COLOR=#e0e0e0
EOF
    echo -e "${GREEN}✓ .env file created${NC}"
else
    echo -e "${GREEN}✓ .env file exists${NC}"
fi

echo ""
echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║         Setup Complete!                                    ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${GREEN}Next steps:${NC}"
echo ""
echo "1. (Optional) Start Ollama if using local LLM:"
echo -e "   ${YELLOW}ollama run llama2${NC}"
echo ""
echo "2. (Optional) Start Cloudflare tunnel in another terminal:"
echo -e "   ${YELLOW}bash scripts/setup_tunnel.sh${NC}"
echo ""
echo "3. Start the FraudSim Lab application:"
echo -e "   ${YELLOW}python app.py${NC}"
echo ""
echo "4. Open browser and navigate to:"
echo -e "   ${YELLOW}http://localhost:8000${NC}"
echo ""
echo "5. Default login credentials:"
echo -e "   ${YELLOW}Username: admin${NC}"
echo -e "   ${YELLOW}Password: admin123${NC}"
echo ""
echo -e "${BLUE}Documentation: See README.md for more information${NC}"
echo ""
