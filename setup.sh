#!/bin/bash

# ═══════════════════════════════════════════════════════════════
#  ATOMIC - Setup Script
#  Advanced Telegram Group/Channel Reporting Tool
# ═══════════════════════════════════════════════════════════════

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color
BOLD='\033[1m'

# Banner
banner() {
    echo -e "${CYAN}"
    echo "  ██████╗ ███████╗ ██████╗ ██████╗ "
    echo "  ██╔══██╗██╔════╝██╔════╝██╔═══██╗"
    echo "  ██║  ██║█████╗  ██║     ██║   ██║"
    echo "  ██║  ██║██╔══╝  ██║     ██║   ██║"
    echo "  ██████╔╝███████╗╚██████╗╚██████╔╝"
    echo "  ╚═════╝ ╚══════╝ ╚═════╝ ╚═════╝ "
    echo -e "${NC}"
    echo -e "${YELLOW}═══════════════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}  ATOMIC Setup Script${NC}"
    echo -e "${YELLOW}═══════════════════════════════════════════════════════════${NC}"
    echo ""
}

# Check Python version
check_python() {
    echo -e "${BLUE}[1/5]${NC} Checking Python version..."
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1-2)
        echo -e "${GREEN}✓${NC} Python $PYTHON_VERSION found"
    else
        echo -e "${RED}✗${NC} Python not found!"
        echo -e "${YELLOW}  Install Python 3.9+ first${NC}"
        exit 1
    fi
}

# Install dependencies
install_deps() {
    echo -e "${BLUE}[2/5]${NC} Installing dependencies..."
    
    # Upgrade pip
    python3 -m pip install --upgrade pip 2>/dev/null || true
    
    # Install telethon
    pip3 install telethon --break-system-packages 2>/dev/null
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓${NC} Telethon installed"
    else
        echo -e "${YELLOW}!${NC} Telethon already installed or using existing"
    fi
    
    # Install other requirements
    pip3 install asyncio --break-system-packages 2>/dev/null || true
    echo -e "${GREEN}✓${NC} Dependencies ready"
}

# Setup configuration files
setup_files() {
    echo -e "${BLUE}[3/5]${NC} Setting up configuration files..."
    
    # Create accounts.json if not exists
    if [ ! -f "accounts.json" ]; then
        cat > accounts.json << 'EOF'
[
  {
    "api_id": 0,
    "api_hash": "",
    "session": "account1"
  }
]
EOF
        echo -e "${YELLOW}✓${NC} Created accounts.json - EDIT THIS FILE!"
    else
        echo -e "${GREEN}✓${NC} accounts.json already exists"
    fi
    
    # Create config.json if not exists
    if [ ! -f "config.json" ]; then
        cat > config.json << 'EOF'
{
  "admin_id": 8754040441,
  "max_reports": 100,
  "interval": 3,
  "image_path": "",
  "rate_limit_wait": 60
}
EOF
        echo -e "${YELLOW}✓${NC} Created config.json"
    else
        echo -e "${GREEN}✓${NC} config.json already exists"
    fi
    
    # Create proxies.json if not exists
    if [ ! -f "proxies.json" ]; then
        echo "[]" > proxies.json
        echo -e "${YELLOW}✓${NC} Created proxies.json (empty)"
    else
        echo -e "${GREEN}✓${NC} proxies.json already exists"
    fi
    
    # Create reports.json
    if [ ! -f "reports.json" ]; then
        echo "[]" > reports.json
        echo -e "${YELLOW}✓${NC} Created reports.json"
    fi
}

# Show next steps
next_steps() {
    echo ""
    echo -e "${YELLOW}═══════════════════════════════════════════════════════════${NC}"
    echo -e "${BOLD}⚠️  NEXT STEPS REQUIRED:${NC}"
    echo -e "${YELLOW}═══════════════════════════════════════════════════════════${NC}"
    echo ""
    echo -e "${RED}1.${NC} Edit ${BOLD}accounts.json${NC} with your API credentials"
    echo "   • Get from https://my.telegram.org"
    echo "   • api_id must be a NUMBER (not string)"
    echo "   • api_hash is a string"
    echo ""
    echo -e "${RED}2.${NC} Run the bot:"
    echo "   ${GREEN}python3 userbot.py${NC}"
    echo ""
    echo -e "${RED}3.${NC} Login with your phone number when prompted"
    echo ""
    echo -e "${YELLOW}═══════════════════════════════════════════════════════════${NC}"
    echo ""
}

# Main
main() {
    banner
    check_python
    install_deps
    setup_files
    next_steps
    
    echo -e "${GREEN}✅ Setup complete!${NC}"
    echo ""
    echo -e "For help: ${CYAN}python3 userbot.py --help${NC}"
    echo ""
}

main "$@"
