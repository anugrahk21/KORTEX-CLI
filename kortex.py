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
MODEL_NAME = "gemini-2.5-flash"
VERSION = "1.1.0"

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

BANNER_MINI = f"{C_CYAN}{C_BOLD}KORTEX-CLI{C_RESET} v{VERSION} | Type 'help' for commands, 'exit' to quit\n"

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
# Update Feature
# ═══════════════════════════════════════════════════════════════════════════════
def update_kortex():
    """Update KORTEX-CLI from GitHub."""
    print(f"\n{C_CYAN}Updating KORTEX-CLI...{C_RESET}\n")
    
    os.chdir(SCRIPT_DIR)
    
    # Stash any local changes
    subprocess.run(["git", "stash"], capture_output=True)
    
    # Pull latest
    result = subprocess.run(["git", "pull"], capture_output=True, text=True)
    
    if result.returncode == 0:
        success("Updated successfully!")
        print(f"{C_DIM}{result.stdout}{C_RESET}")
    else:
        error("Update failed!")
        print(f"{C_DIM}{result.stderr}{C_RESET}")
    
    # Make executable
    os.chmod(SCRIPT_PATH, 0o755)
    print()


# ═══════════════════════════════════════════════════════════════════════════════
# AI Generation
# ═══════════════════════════════════════════════════════════════════════════════
def list_models(api_key: str):
    """List available Gemini models."""
    try:
        from google import genai
        client = genai.Client(api_key=api_key)
        print(f"\n{C_CYAN}Available Models:{C_RESET}")
        print(f"{C_DIM}{'─' * 40}{C_RESET}")
        
        # Paginate through models
        pager = client.models.list(config={"page_size": 100})
        found = False
        for model in pager:
            name = model.name.replace("models/", "")
            if "gemini" in name:
                print(f"  • {name}")
                found = True
        
        if not found:
            print(f"  {C_YELLOW}No Gemini models found explicitly.{C_RESET}")
            
        print(f"\n{C_DIM}Current Config: {MODEL_NAME}{C_RESET}\n")
        
    except Exception as e:
        error(f"Failed to list models: {e}")
        sys.exit(1)


def generate_command(query: str, api_key: str) -> str:
    """Generate shell command using Gemini AI (google-genai)."""
    try:
        from google import genai
        from google.genai import types
    except ImportError:
        error("google-genai not installed!")
        print(f"  Run: {C_CYAN}pip install google-genai{C_RESET}")
        sys.exit(1)
    
    print(f"\n{C_MAGENTA}🧠 Analyzing...{C_RESET}")
    
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
        return None


# ═══════════════════════════════════════════════════════════════════════════════
# CLI Interface
# ═══════════════════════════════════════════════════════════════════════════════
def display_command(command: str):
    """Display the proposed command."""
    border = "═" * 60
    print(f"\n{C_YELLOW}{border}{C_RESET}")
    print(f"{C_GREEN}{C_BOLD}👉 Proposed Command:{C_RESET}")
    print(f"\n   {C_CYAN}{C_BOLD}{command}{C_RESET}\n")
    print(f"{C_YELLOW}{border}{C_RESET}")


def get_action() -> str:
    """Get user action choice."""
    try:
        print(f"\n{C_BOLD}[E]{C_RESET}xecute  {C_BOLD}[R]{C_RESET}efine  {C_BOLD}[C]{C_RESET}ancel")
        choice = input(f"{C_DIM}> {C_RESET}").strip().lower()
        return choice
    except (KeyboardInterrupt, EOFError):
        return 'c'


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
  kx                     Enter interactive mode (KORTEX> prompt)
  kx "<your request>"    One-shot command translation
  
{C_BOLD}Commands:{C_RESET}
  kx update              Update KORTEX-CLI from GitHub
  kx --models            List available AI models
  kx --help              Show this help
  kx --version           Show version

{C_BOLD}Interactive Mode:{C_RESET}
  Type your request, then:
  [E] Execute the command
  [R] Refine - ask again with different wording
  [C] Cancel
""")


def show_version():
    """Display version."""
    print(f"\n{C_CYAN}KORTEX-CLI{C_RESET} v{VERSION}")
    print(f"By Anugrah K")
    print(f"Model: {MODEL_NAME}")
    print(f"https://github.com/anugrahk21/Kortex-CLI\n")


# ═══════════════════════════════════════════════════════════════════════════════
# Interactive Mode
# ═══════════════════════════════════════════════════════════════════════════════
def interactive_mode(api_key: str):
    """Run KORTEX in interactive REPL mode."""
    print(BANNER)
    print(BANNER_MINI)
    
    while True:
        try:
            # KORTEX> prompt
            query = input(f"{C_CYAN}{C_BOLD}KORTEX>{C_RESET} ").strip()
            
            if not query:
                continue
            
            # Handle special commands
            if query.lower() in ('exit', 'quit', 'q'):
                print(f"\n{C_DIM}Goodbye!{C_RESET}\n")
                break
            elif query.lower() in ('help', 'h', '?'):
                show_help()
                continue
            elif query.lower() == 'update':
                update_kortex()
                continue
            elif query.lower() == 'models':
                list_models(api_key)
                continue
            elif query.lower() == 'clear':
                os.system('clear' if os.name != 'nt' else 'cls')
                print(BANNER_MINI)
                continue
            elif query.lower() == 'version':
                show_version()
                continue
            
            # Generate command
            command = generate_command(query, api_key)
            if not command:
                continue
            
            display_command(command)
            
            # Action loop (allows refinement)
            while True:
                action = get_action()
                
                if action in ('e', 'y', 'yes', 'execute'):
                    execute(command)
                    break
                elif action in ('r', 'refine', 'again'):
                    print(f"\n{C_DIM}Describe what you want differently:{C_RESET}")
                    new_query = input(f"{C_CYAN}{C_BOLD}KORTEX>{C_RESET} ").strip()
                    if new_query:
                        command = generate_command(new_query, api_key)
                        if command:
                            display_command(command)
                        else:
                            break
                else:
                    print(f"{C_DIM}  → Cancelled{C_RESET}")
                    break
            
            print()  # Spacing
            
        except KeyboardInterrupt:
            print(f"\n\n{C_DIM}Goodbye!{C_RESET}\n")
            break
        except EOFError:
            break


# ═══════════════════════════════════════════════════════════════════════════════
# One-Shot Mode
# ═══════════════════════════════════════════════════════════════════════════════
def one_shot_mode(query: str, api_key: str):
    """Run a single query and exit."""
    command = generate_command(query, api_key)
    if not command:
        return
    
    display_command(command)
    
    while True:
        action = get_action()
        
        if action in ('e', 'y', 'yes', 'execute'):
            execute(command)
            break
        elif action in ('r', 'refine', 'again'):
            print(f"\n{C_DIM}Describe what you want differently:{C_RESET}")
            try:
                new_query = input(f"{C_CYAN}{C_BOLD}KORTEX>{C_RESET} ").strip()
                if new_query:
                    command = generate_command(new_query, api_key)
                    if command:
                        display_command(command)
                    else:
                        break
            except (KeyboardInterrupt, EOFError):
                break
        else:
            print(f"\n{C_DIM}  → Cancelled{C_RESET}\n")
            break


# ═══════════════════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════════════════
def main():
    # No arguments -> Interactive mode
    if len(sys.argv) < 2:
        api_key = get_api_key()
        interactive_mode(api_key)
        return
    
    arg = sys.argv[1].lower()
    
    # Special commands
    if arg in ('--help', '-h', 'help'):
        print(BANNER)
        show_help()
        return
    
    if arg in ('--version', '-v', 'version'):
        show_version()
        return
    
    if arg in ('--models', 'models'):
        api_key = get_api_key()
        list_models(api_key)
        return
        
    if arg in ('update', '--update'):
        update_kortex()
        return
    
    # One-shot query mode
    query = " ".join(sys.argv[1:])
    api_key = get_api_key()
    one_shot_mode(query, api_key)
