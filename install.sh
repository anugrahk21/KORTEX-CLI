#!/bin/bash

# ═══════════════════════════════════════════════════════════════════════════════
#  ██╗  ██╗ ██████╗ ██████╗ ████████╗███████╗██╗  ██╗       ██████╗██╗     ██╗
#  ██║ ██╔╝██╔═══██╗██╔══██╗╚══██╔══╝██╔════╝╚██╗██╔╝      ██╔════╝██║     ██║
#  █████╔╝ ██║   ██║██████╔╝   ██║   █████╗   ╚███╔╝ █████╗██║     ██║     ██║
#  ██╔═██╗ ██║   ██║██╔══██╗   ██║   ██╔══╝   ██╔██╗ ╚════╝██║     ██║     ██║
#  ██║  ██╗╚██████╔╝██║  ██║   ██║   ███████╗██╔╝ ██╗      ╚██████╗███████╗██║
#  ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝  ╚═╝       ╚═════╝╚══════╝╚═╝
#
#  KORTEX-CLI Installation Script
#  The Neural Layer for your Linux Kernel
#  By Anugrah K
# ═══════════════════════════════════════════════════════════════════════════════

set -e

# Colors
RED='\033[0;91m'
GREEN='\033[0;92m'
YELLOW='\033[0;93m'
BLUE='\033[0;94m'
CYAN='\033[0;96m'
BOLD='\033[1m'
DIM='\033[2m'
RESET='\033[0m'

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
KORTEX_SCRIPT="$SCRIPT_DIR/kortex.py"
CONFIG_FILE="$HOME/.kortex_key"
SYMLINK_PATH="/usr/local/bin/kx"

# ═══════════════════════════════════════════════════════════════════════════════
# Utility Functions
# ═══════════════════════════════════════════════════════════════════════════════

print_banner() {
    echo -e "${CYAN}${BOLD}"
    echo " ██╗  ██╗ ██████╗ ██████╗ ████████╗███████╗██╗  ██╗       ██████╗██╗     ██╗"
    echo " ██║ ██╔╝██╔═══██╗██╔══██╗╚══██╔══╝██╔════╝╚██╗██╔╝      ██╔════╝██║     ██║"
    echo " █████╔╝ ██║   ██║██████╔╝   ██║   █████╗   ╚███╔╝ █████╗██║     ██║     ██║"
    echo " ██╔═██╗ ██║   ██║██╔══██╗   ██║   ██╔══╝   ██╔██╗ ╚════╝██║     ██║     ██║"
    echo " ██║  ██╗╚██████╔╝██║  ██║   ██║   ███████╗██╔╝ ██╗      ╚██████╗███████╗██║"
    echo " ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝  ╚═╝       ╚═════╝╚══════╝╚═╝"
    echo -e "${RESET}${DIM}              The Neural Layer for your Linux Kernel${RESET}"
    echo -e "${DIM}                          By Anugrah K${RESET}"
    echo ""
    echo -e "${YELLOW}════════════════════════════════════════════════════════════════════════${RESET}"
    echo -e "${BOLD}                         Installation Script                            ${RESET}"
    echo -e "${YELLOW}════════════════════════════════════════════════════════════════════════${RESET}"
    echo ""
}

print_step() {
    echo -e "${BLUE}▶ ${BOLD}$1${RESET}"
}

print_success() {
    echo -e "${GREEN}✓ $1${RESET}"
}

print_error() {
    echo -e "${RED}✗ Error: $1${RESET}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${RESET}"
}

print_info() {
    echo -e "${DIM}  → $1${RESET}"
}

# ═══════════════════════════════════════════════════════════════════════════════
# Installation Steps
# ═══════════════════════════════════════════════════════════════════════════════

check_python() {
    print_step "Checking Python installation..."
    
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version 2>&1)
        print_success "Found $PYTHON_VERSION"
    else
        print_error "Python 3 is not installed!"
        echo -e "  ${YELLOW}Please install Python 3.10 or later:${RESET}"
        echo -e "  ${CYAN}  sudo apt install python3 python3-pip${RESET}"
        exit 1
    fi
}

check_pip() {
    print_step "Checking pip installation..."
    
    if command -v pip3 &> /dev/null; then
        PIP_VERSION=$(pip3 --version 2>&1 | awk '{print $1, $2}')
        print_success "Found $PIP_VERSION"
    elif command -v pip &> /dev/null; then
        PIP_VERSION=$(pip --version 2>&1 | awk '{print $1, $2}')
        print_success "Found $PIP_VERSION"
    else
        print_error "pip is not installed!"
        echo -e "  ${YELLOW}Please install pip:${RESET}"
        echo -e "  ${CYAN}  sudo apt install python3-pip${RESET}"
        exit 1
    fi
}

install_dependencies() {
    print_step "Installing Python dependencies..."
    
    if [ -f "$SCRIPT_DIR/requirements.txt" ]; then
        pip3 install -q -r "$SCRIPT_DIR/requirements.txt" 2>/dev/null || \
        pip install -q -r "$SCRIPT_DIR/requirements.txt" 2>/dev/null
        print_success "Dependencies installed successfully"
    else
        print_warning "requirements.txt not found, installing manually..."
        pip3 install -q google-generativeai 2>/dev/null || \
        pip install -q google-generativeai 2>/dev/null
        print_success "google-generativeai installed"
    fi
}

configure_api_key() {
    print_step "Configuring API Key..."
    
    if [ -f "$CONFIG_FILE" ]; then
        echo ""
        print_warning "Existing API key found at $CONFIG_FILE"
        read -p "  → Overwrite existing key? [y/N]: " OVERWRITE
        if [[ ! "$OVERWRITE" =~ ^[Yy]$ ]]; then
            print_info "Keeping existing API key"
            return
        fi
    fi
    
    echo ""
    echo -e "  ${CYAN}Get your API key from: https://makersuite.google.com/app/apikey${RESET}"
    echo ""
    
    # Read API key securely (hidden input)
    read -sp "  Enter your Google Gemini API Key: " API_KEY
    echo ""
    
    if [ -z "$API_KEY" ]; then
        print_error "API key cannot be empty!"
        exit 1
    fi
    
    # Write API key to config file
    echo "$API_KEY" > "$CONFIG_FILE"
    
    # Set secure permissions (owner read/write only)
    chmod 600 "$CONFIG_FILE"
    
    print_success "API key saved to $CONFIG_FILE"
    print_info "File permissions set to 600 (owner only)"
}

create_symlink() {
    print_step "Creating global 'kx' command..."
    
    # Make the python script executable
    chmod +x "$KORTEX_SCRIPT"
    
    # Check if symlink already exists
    if [ -L "$SYMLINK_PATH" ]; then
        print_warning "Symlink already exists, updating..."
        sudo rm "$SYMLINK_PATH"
    elif [ -f "$SYMLINK_PATH" ]; then
        print_error "A file already exists at $SYMLINK_PATH"
        print_info "Please remove it manually and re-run the installer"
        exit 1
    fi
    
    # Create symlink (requires sudo for /usr/local/bin)
    echo ""
    print_info "Creating symlink requires sudo permissions..."
    
    if sudo ln -s "$KORTEX_SCRIPT" "$SYMLINK_PATH"; then
        print_success "Symlink created: $SYMLINK_PATH → $KORTEX_SCRIPT"
    else
        print_error "Failed to create symlink. Try manually:"
        echo -e "  ${CYAN}  sudo ln -s $KORTEX_SCRIPT $SYMLINK_PATH${RESET}"
        exit 1
    fi
}

verify_installation() {
    print_step "Verifying installation..."
    
    if command -v kx &> /dev/null; then
        print_success "KORTEX is ready to use!"
    else
        print_warning "Command 'kx' not found in PATH"
        print_info "You may need to restart your terminal or run:"
        echo -e "  ${CYAN}  source ~/.bashrc${RESET}"
    fi
}

print_completion() {
    echo ""
    echo -e "${GREEN}════════════════════════════════════════════════════════════${RESET}"
    echo -e "${GREEN}${BOLD}           ✓ KORTEX Installation Complete!                  ${RESET}"
    echo -e "${GREEN}════════════════════════════════════════════════════════════${RESET}"
    echo ""
    echo -e "${BOLD}Quick Start:${RESET}"
    echo -e "  ${CYAN}kx \"find all python files\"${RESET}"
    echo -e "  ${CYAN}kx \"scan 192.168.1.1 for open ports\"${RESET}"
    echo -e "  ${CYAN}kx \"compress the logs folder\"${RESET}"
    echo ""
    echo -e "${BOLD}Help:${RESET}"
    echo -e "  ${CYAN}kx --help${RESET}"
    echo ""
    echo -e "${DIM}Config: $CONFIG_FILE${RESET}"
    echo -e "${DIM}Script: $KORTEX_SCRIPT${RESET}"
    echo ""
}

# ═══════════════════════════════════════════════════════════════════════════════
# Main Installation Flow
# ═══════════════════════════════════════════════════════════════════════════════

main() {
    print_banner
    
    check_python
    check_pip
    echo ""
    
    install_dependencies
    echo ""
    
    configure_api_key
    echo ""
    
    create_symlink
    echo ""
    
    verify_installation
    
    print_completion
}

# Run main function
main "$@"
