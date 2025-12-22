#!/bin/bash
# KORTEX-CLI Installer | By Anugrah K

# Colors
RED='\033[91m'; GREEN='\033[92m'; YELLOW='\033[93m'; CYAN='\033[96m'
BOLD='\033[1m'; DIM='\033[2m'; RESET='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo -e "${CYAN}${BOLD}"
echo " ██╗  ██╗ ██████╗ ██████╗ ████████╗███████╗██╗  ██╗       ██████╗██╗     ██╗"
echo " ██║ ██╔╝██╔═══██╗██╔══██╗╚══██╔══╝██╔════╝╚██╗██╔╝      ██╔════╝██║     ██║"
echo " █████╔╝ ██║   ██║██████╔╝   ██║   █████╗   ╚███╔╝ █████╗██║     ██║     ██║"
echo " ██╔═██╗ ██║   ██║██╔══██╗   ██║   ██╔══╝   ██╔██╗ ╚════╝██║     ██║     ██║"
echo " ██║  ██╗╚██████╔╝██║  ██║   ██║   ███████╗██╔╝ ██╗      ╚██████╗███████╗██║"
echo " ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝  ╚═╝       ╚═════╝╚══════╝╚═╝"
echo -e "${RESET}${DIM}                        Installer | By Anugrah K${RESET}"
echo ""

echo -e "${BOLD}Checking requirements...${RESET}"

# Check Python
if command -v python3 &>/dev/null; then
    echo -e "  ${GREEN}✓${RESET} Python3: $(python3 --version 2>&1 | awk '{print $2}')"
else
    echo -e "  ${RED}✗${RESET} Python3: Not found"
    echo -e "    Install: ${CYAN}sudo apt install python3 python3-pip${RESET}"
    exit 1
fi

# Check pip
if command -v pip3 &>/dev/null; then
    echo -e "  ${GREEN}✓${RESET} pip3: Found"
else
    echo -e "  ${RED}✗${RESET} pip3: Not found"
    echo -e "    Install: ${CYAN}sudo apt install python3-pip${RESET}"
    exit 1
fi

# Check google-generativeai
if python3 -c "import google.generativeai" 2>/dev/null; then
    echo -e "  ${GREEN}✓${RESET} google-generativeai: Installed"
else
    echo -e "  ${YELLOW}!${RESET} google-generativeai: Not installed"
    echo ""
    read -p "  Install google-generativeai? [Y/n]: " INSTALL_DEP
    if [[ ! "$INSTALL_DEP" =~ ^[Nn]$ ]]; then
        echo -e "  Installing..."
        pip3 install --user google-generativeai
        if [ $? -eq 0 ]; then
            echo -e "  ${GREEN}✓${RESET} Installed successfully"
        else
            echo -e "  ${RED}✗${RESET} Installation failed. Try manually:"
            echo -e "     ${CYAN}pip3 install --user google-generativeai${RESET}"
            exit 1
        fi
    else
        echo -e "  ${RED}✗${RESET} Skipped. Run manually: pip3 install google-generativeai"
        exit 1
    fi
fi

echo ""

# Setup .env file
if [ -f "$SCRIPT_DIR/.env" ]; then
    CURRENT_KEY=$(grep "GEMINI_API_KEY=" "$SCRIPT_DIR/.env" 2>/dev/null | cut -d'=' -f2)
    if [ -z "$CURRENT_KEY" ] || [ "$CURRENT_KEY" = "your_api_key_here" ]; then
        echo -e "${YELLOW}!${RESET} API key not configured"
        echo ""
        echo -e "  Get your key: ${CYAN}https://makersuite.google.com/app/apikey${RESET}"
        echo ""
        read -p "  Enter your Gemini API Key: " API_KEY
        if [ -n "$API_KEY" ]; then
            echo "GEMINI_API_KEY=$API_KEY" > "$SCRIPT_DIR/.env"
            echo -e "  ${GREEN}✓${RESET} API key saved"
        fi
    else
        echo -e "${GREEN}✓${RESET} .env configured"
    fi
else
    echo -e "${YELLOW}!${RESET} Setting up API key..."
    echo ""
    echo -e "  Get your key: ${CYAN}https://makersuite.google.com/app/apikey${RESET}"
    echo ""
    read -p "  Enter your Gemini API Key: " API_KEY
    if [ -n "$API_KEY" ]; then
        echo "GEMINI_API_KEY=$API_KEY" > "$SCRIPT_DIR/.env"
        echo -e "  ${GREEN}✓${RESET} .env created"
    else
        echo -e "  ${RED}✗${RESET} No key entered. Add it later:"
        echo -e "     ${CYAN}echo 'GEMINI_API_KEY=your_key' > .env${RESET}"
    fi
fi

echo ""

# Create symlink
chmod +x "$SCRIPT_DIR/kortex.py"

if [ -L "/usr/local/bin/kx" ] || [ -f "/usr/local/bin/kx" ]; then
    echo -e "${YELLOW}!${RESET} /usr/local/bin/kx already exists"
    read -p "  Overwrite? [Y/n]: " OVERWRITE
    if [[ ! "$OVERWRITE" =~ ^[Nn]$ ]]; then
        sudo rm -f /usr/local/bin/kx
        sudo ln -s "$SCRIPT_DIR/kortex.py" /usr/local/bin/kx
        echo -e "  ${GREEN}✓${RESET} Symlink updated"
    fi
else
    echo -e "Creating global 'kx' command..."
    sudo ln -s "$SCRIPT_DIR/kortex.py" /usr/local/bin/kx
    echo -e "  ${GREEN}✓${RESET} Symlink created: /usr/local/bin/kx"
fi

echo ""
echo -e "${GREEN}${BOLD}✓ KORTEX-CLI installed!${RESET}"
echo ""
echo -e "  Try: ${CYAN}kx \"list all files\"${RESET}"
echo -e "  Help: ${CYAN}kx --help${RESET}"
echo ""
