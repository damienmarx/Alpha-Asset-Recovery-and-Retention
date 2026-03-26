#!/bin/bash

# Colors
BLUE='\033[0;34m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║         Cloudflare Tunnel Setup                            ║${NC}"
echo -e "${BLUE}║         Expose FraudSim Lab to the Internet                ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Check if cloudflared is installed
if ! command -v cloudflared &> /dev/null; then
    echo -e "${YELLOW}→ Installing cloudflared...${NC}"
    
    # Detect OS
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        wget -q https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64 -O /tmp/cloudflared
        sudo mv /tmp/cloudflared /usr/local/bin/
        sudo chmod +x /usr/local/bin/cloudflared
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        brew install cloudflare/cloudflare/cloudflared
    else
        echo -e "${YELLOW}Please install cloudflared manually from: https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/install-and-setup/installation/${NC}"
        exit 1
    fi
    echo -e "${GREEN}✓ cloudflared installed${NC}"
else
    echo -e "${GREEN}✓ cloudflared found${NC}"
fi

echo ""
echo -e "${YELLOW}Starting tunnel to http://localhost:8000${NC}"
echo ""
echo -e "${BLUE}Your tunnel URL will appear below. Use this for Twilio webhooks:${NC}"
echo ""

# Start tunnel
cloudflared tunnel --url http://localhost:8000

echo ""
echo -e "${YELLOW}Tunnel stopped${NC}"
