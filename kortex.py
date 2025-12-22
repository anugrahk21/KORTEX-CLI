#!/usr/bin/env python3
"""
KORTEX-CLI - The Neural Layer for your Linux Kernel
An AI-powered CLI tool by Anugrah K
https://github.com/anugrahk21/Kortex-CLI
"""

import os
import sys
import subprocess
from pathlib import Path

# ═══════════════════════════════════════════════════════════════════════════════
# Configuration
# ═══════════════════════════════════════════════════════════════════════════════
# Resolve symlink to find the actual script directory (where .env lives)
SCRIPT_PATH = Path(__file__).resolve()  # Resolves symlink to actual file
if SCRIPT_PATH.is_symlink():
    SCRIPT_PATH = Path(os.readlink(SCRIPT_PATH))
SCRIPT_DIR = SCRIPT_PATH.parent
ENV_FILE = SCRIPT_DIR / ".env"
MODEL_NAME = "gemini-1.5-flash"

# ANSI Colors
C_RESET = "\033[0m"
C_BOLD = "\033[1m"
C_DIM = "\033[2m"
C_RED = "\033[91m"
C_GREEN = "\033[92m"
C_YELLOW = "\033[93m"
C_CYAN = "\033[96m"
C_MAGENTA = "\033[95m"

BANNER = f"""
{C_CYAN}{C_BOLD}
 ██╗  ██╗ ██████╗ ██████╗ ████████╗███████╗██╗  ██╗       ██████╗██╗     ██╗
 ██║ ██╔╝██╔═══██╗██╔══██╗╚══██╔══╝██╔════╝╚██╗██╔╝      ██╔════╝██║     ██║
 █████╔╝ ██║   ██║██████╔╝   ██║   █████╗   ╚███╔╝ █████╗██║     ██║     ██║
 ██╔═██╗ ██║   ██║██╔══██╗   ██║   ██╔══╝   ██╔██╗ ╚════╝██║     ██║     ██║
 ██║  ██╗╚██████╔╝██║  ██║   ██║   ███████╗██╔╝ ██╗      ╚██████╗███████╗██║
 ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝  ╚═╝       ╚═════╝╚══════╝╚═╝
{C_RESET}{C_DIM}              The Neural Layer for your Linux Kernel
                          By Anugrah K{C_RESET}
"""

SYSTEM_PROMPT = """You are KORTEX, an expert Linux/Unix system administrator and security professional.
Your ONLY task is to translate user requests into precise, executable shell commands.

STRICT RULES:
1. Output ONLY the raw command string - nothing else
2. NO markdown formatting (no ```bash blocks)
3. NO explanations or conversational text
4. For multi-step operations, chain with && or use semicolons
5. Always prefer one-liners when possible"""


# ═══════════════════════════════════════════════════════════════════════════════
# Utilities
# ═══════════════════════════════════════════════════════════════════════════════
def error(msg): print(f"{C_RED}✗ {msg}{C_RESET}")
def success(msg): print(f"{C_GREEN}✓ {msg}{C_RESET}")
def info(msg): print(f"{C_DIM}  → {msg}{C_RESET}")


def load_env():
    """Load API key from .env file."""
    if not ENV_FILE.exists():
        return None
    
    with open(ENV_FILE) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                if key.strip() == 'GEMINI_API_KEY':
                    return value.strip()
    return None


def get_api_key():
    """Get API key from .env file or environment."""
    # First check environment variable
    api_key = os.environ.get('GEMINI_API_KEY')
    if api_key and api_key != 'your_api_key_here':
        return api_key
    
    # Then check .env file
    api_key = load_env()
    if api_key and api_key != 'your_api_key_here':
        return api_key
    
    # No valid key found
    error("API key not configured!")
    print(f"\n  {C_YELLOW}Setup:{C_RESET}")
    print(f"  1. Run {C_CYAN}./install.sh{C_RESET} to configure")
    print(f"  2. Or create {C_CYAN}.env{C_RESET} with: GEMINI_API_KEY=your_key")
    print(f"\n  Get key: {C_CYAN}https://makersuite.google.com/app/apikey{C_RESET}\n")
    sys.exit(1)


# ═══════════════════════════════════════════════════════════════════════════════
# AI Generation
# ═══════════════════════════════════════════════════════════════════════════════
def generate_command(query: str, api_key: str) -> str:
    """Generate shell command using Gemini AI (google-genai)."""
    try:
        from google import genai
        from google.genai import types
    except ImportError:
        error("google-genai not installed!")
        print(f"  Run: {C_CYAN}pip install google-genai{C_RESET}")
        sys.exit(1)
    
    print(f"\n{C_MAGENTA}🧠 KORTEX is analyzing...{C_RESET}\n")
    
    try:
        client = genai.Client(api_key=api_key)
        
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=query,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                temperature=0.1,
                max_output_tokens=256
            )
        )
        
        command = response.text.strip()
        # Remove markdown formatting if present
        if command.startswith("```"):
            lines = command.split("\n")
            command = "\n".join(lines[1:-1] if lines[-1].startswith("```") else lines[1:])
        return command.strip()
        
    except Exception as e:
        error(f"AI generation failed: {e}")
        sys.exit(1)


# ═══════════════════════════════════════════════════════════════════════════════
# CLI Interface
# ═══════════════════════════════════════════════════════════════════════════════
def display_command(command: str):
    """Display the proposed command."""
    border = "═" * 60
    print(f"{C_YELLOW}{border}{C_RESET}")
    print(f"{C_GREEN}{C_BOLD}👉 Proposed Action:{C_RESET}")
    print(f"\n   {C_CYAN}{C_BOLD}{command}{C_RESET}\n")
    print(f"{C_YELLOW}{border}{C_RESET}\n")


def confirm() -> bool:
    """Get user confirmation."""
    try:
        choice = input(f"{C_BOLD}[E]xecute  [C]ancel : {C_RESET}").strip().lower()
        return choice in ('e', 'y', 'yes', 'execute')
    except (KeyboardInterrupt, EOFError):
        return False


def execute(command: str):
    """Execute the command."""
    print(f"\n{C_GREEN}▶ Executing...{C_RESET}\n")
    print(f"{C_DIM}{'─' * 60}{C_RESET}\n")
    
    result = subprocess.run(command, shell=True, executable=os.environ.get('SHELL', '/bin/bash'))
    
    print(f"\n{C_DIM}{'─' * 60}{C_RESET}")
    if result.returncode == 0:
        success(f"Done (exit code: {result.returncode})")
    else:
        print(f"{C_YELLOW}⚠ Exit code: {result.returncode}{C_RESET}")


def show_help():
    """Display help."""
    print(BANNER)
    print(f"""
{C_BOLD}Usage:{C_RESET}
  kx "<your request>"

{C_BOLD}Examples:{C_RESET}
  kx "find all python files"
  kx "scan 192.168.1.1 for open ports"
  kx "compress the logs folder"

{C_BOLD}Options:{C_RESET}
  --help, -h     Show this help
  --version, -v  Show version
""")


def show_version():
    """Display version."""
    print(f"\n{C_CYAN}KORTEX-CLI{C_RESET} v1.0.0")
    print(f"By Anugrah K")
    print(f"https://github.com/anugrahk21/Kortex-CLI\n")


# ═══════════════════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════════════════
def main():
    if len(sys.argv) < 2:
        print(BANNER)
        show_help()
        return
    
    arg = sys.argv[1].lower()
    
    if arg in ('--help', '-h', 'help'):
        show_help()
        return
    
    if arg in ('--version', '-v', 'version'):
        show_version()
        return
    
    # Get query and API key
    query = " ".join(sys.argv[1:])
    api_key = get_api_key()
    
    # Generate and display command
    command = generate_command(query, api_key)
    display_command(command)
    
    # Execute if confirmed
    if confirm():
        execute(command)
    else:
        print(f"\n{C_DIM}  → Cancelled{C_RESET}\n")


if __name__ == "__main__":
    main()
