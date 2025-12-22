#!/usr/bin/env python3
"""
 ██╗  ██╗ ██████╗ ██████╗ ████████╗███████╗██╗  ██╗       ██████╗██╗     ██╗
 ██║ ██╔╝██╔═══██╗██╔══██╗╚══██╔══╝██╔════╝╚██╗██╔╝      ██╔════╝██║     ██║
 █████╔╝ ██║   ██║██████╔╝   ██║   █████╗   ╚███╔╝ █████╗██║     ██║     ██║
 ██╔═██╗ ██║   ██║██╔══██╗   ██║   ██╔══╝   ██╔██╗ ╚════╝██║     ██║     ██║
 ██║  ██╗╚██████╔╝██║  ██║   ██║   ███████╗██╔╝ ██╗      ╚██████╗███████╗██║
 ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝  ╚═╝       ╚═════╝╚══════╝╚═╝
                                                    
KORTEX-CLI - The Neural Layer for your Linux Kernel
An AI-powered CLI tool by Anugrah K

Translates natural language to executable shell commands.
Repository: https://github.com/anugrahk21/Kortex-CLI
"""

import os
import sys
import subprocess
import stat
from pathlib import Path

try:
    import google.generativeai as genai
except ImportError:
    print("\033[91m✗ Error: google-generativeai package not found.\033[0m")
    print("  Please run: pip install google-generativeai")
    sys.exit(1)


# ═══════════════════════════════════════════════════════════════════════════════
# ANSI Color Codes
# ═══════════════════════════════════════════════════════════════════════════════
class Colors:
    """ANSI escape codes for terminal styling."""
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    
    # Colors
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"
    
    # Background
    BG_GREEN = "\033[42m"
    BG_BLUE = "\033[44m"


# ═══════════════════════════════════════════════════════════════════════════════
# Configuration
# ═══════════════════════════════════════════════════════════════════════════════
CONFIG_FILE = Path.home() / ".kortex_key"
MODEL_NAME = "gemini-1.5-flash"

SYSTEM_PROMPT = """You are KORTEX, an expert Linux/Unix system administrator and security professional. 
Your ONLY task is to translate user requests into precise, executable shell commands.

STRICT RULES:
1. Output ONLY the raw command string - nothing else
2. NO markdown formatting (no ```bash blocks)
3. NO explanations or conversational text
4. NO disclaimers or warnings
5. For multi-step operations, chain commands with && or use semicolons
6. Always prefer one-liners when possible
7. Use common, portable commands when available
8. For security tools (nmap, nikto, etc.), include relevant flags for thorough results

Examples of CORRECT output:
- User: "find all python files" → find . -name "*.py" -type f
- User: "check open ports on 192.168.1.1" → nmap -sS -sV 192.168.1.1
- User: "compress this folder" → tar -czvf archive.tar.gz ./folder
- User: "show disk usage" → df -h && du -sh * | sort -rh | head -20

Remember: Output ONLY the command. No text before or after."""


# ═══════════════════════════════════════════════════════════════════════════════
# Utility Functions
# ═══════════════════════════════════════════════════════════════════════════════
def print_banner():
    """Display the KORTEX-CLI ASCII banner."""
    banner = f"""
{Colors.CYAN}{Colors.BOLD}
 ██╗  ██╗ ██████╗ ██████╗ ████████╗███████╗██╗  ██╗       ██████╗██╗     ██╗
 ██║ ██╔╝██╔═══██╗██╔══██╗╚══██╔══╝██╔════╝╚██╗██╔╝      ██╔════╝██║     ██║
 █████╔╝ ██║   ██║██████╔╝   ██║   █████╗   ╚███╔╝ █████╗██║     ██║     ██║
 ██╔═██╗ ██║   ██║██╔══██╗   ██║   ██╔══╝   ██╔██╗ ╚════╝██║     ██║     ██║
 ██║  ██╗╚██████╔╝██║  ██║   ██║   ███████╗██╔╝ ██╗      ╚██████╗███████╗██║
 ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝  ╚═╝       ╚═════╝╚══════╝╚═╝
{Colors.RESET}{Colors.DIM}              The Neural Layer for your Linux Kernel
                          By Anugrah K{Colors.RESET}
"""
    print(banner)


def print_error(message: str):
    """Print an error message in red."""
    print(f"{Colors.RED}✗ Error: {message}{Colors.RESET}")


def print_success(message: str):
    """Print a success message in green."""
    print(f"{Colors.GREEN}✓ {message}{Colors.RESET}")


def print_info(message: str):
    """Print an info message in blue."""
    print(f"{Colors.BLUE}ℹ {message}{Colors.RESET}")


# ═══════════════════════════════════════════════════════════════════════════════
# Feature A: Configuration & Security
# ═══════════════════════════════════════════════════════════════════════════════
def check_file_permissions(filepath: Path) -> bool:
    """Check if the config file has secure permissions (600)."""
    if sys.platform == "win32":
        # Windows doesn't use Unix-style permissions
        return True
    
    try:
        file_stat = os.stat(filepath)
        mode = file_stat.st_mode
        # Check if file is readable/writable only by owner (600)
        if mode & (stat.S_IRWXG | stat.S_IRWXO):
            return False
        return True
    except OSError:
        return False


def load_api_key() -> str:
    """Load the API key from the config file with security checks."""
    if not CONFIG_FILE.exists():
        print_error("API key not found!")
        print(f"\n  {Colors.YELLOW}Please run the installation script:{Colors.RESET}")
        print(f"  {Colors.CYAN}  ./install.sh{Colors.RESET}")
        print(f"\n  Or manually create {Colors.DIM}{CONFIG_FILE}{Colors.RESET}")
        print(f"  with your Google Gemini API key.\n")
        sys.exit(1)
    
    # Check file permissions (Unix-like systems only)
    if sys.platform != "win32" and not check_file_permissions(CONFIG_FILE):
        print_error(f"Insecure permissions on {CONFIG_FILE}")
        print(f"\n  {Colors.YELLOW}Fix with:{Colors.RESET}")
        print(f"  {Colors.CYAN}  chmod 600 {CONFIG_FILE}{Colors.RESET}\n")
        sys.exit(1)
    
    try:
        api_key = CONFIG_FILE.read_text().strip()
        if not api_key:
            print_error("API key file is empty!")
            sys.exit(1)
        return api_key
    except PermissionError:
        print_error(f"Cannot read {CONFIG_FILE} - permission denied")
        sys.exit(1)
    except Exception as e:
        print_error(f"Failed to read API key: {e}")
        sys.exit(1)


# ═══════════════════════════════════════════════════════════════════════════════
# Feature B: The "Brain" (AI Logic)
# ═══════════════════════════════════════════════════════════════════════════════
def generate_command(user_query: str, api_key: str) -> str:
    """Generate a shell command from natural language using Gemini AI."""
    print(f"\n{Colors.MAGENTA}🧠 KORTEX is analyzing...{Colors.RESET}\n")
    
    try:
        # Configure the Gemini API
        genai.configure(api_key=api_key)
        
        # Initialize the model
        model = genai.GenerativeModel(
            model_name=MODEL_NAME,
            system_instruction=SYSTEM_PROMPT
        )
        
        # Generate the command
        response = model.generate_content(
            user_query,
            generation_config=genai.GenerationConfig(
                temperature=0.1,  # Low temperature for precise outputs
                max_output_tokens=256,
            )
        )
        
        # Extract and clean the command
        command = response.text.strip()
        
        # Remove any accidental markdown formatting
        if command.startswith("```"):
            lines = command.split("\n")
            command = "\n".join(lines[1:-1] if lines[-1] == "```" else lines[1:])
        
        return command.strip()
        
    except Exception as e:
        error_msg = str(e)
        if "API_KEY" in error_msg.upper() or "INVALID" in error_msg.upper():
            print_error("Invalid API key. Please check your configuration.")
        elif "QUOTA" in error_msg.upper():
            print_error("API quota exceeded. Please check your Google Cloud billing.")
        else:
            print_error(f"AI generation failed: {e}")
        sys.exit(1)


# ═══════════════════════════════════════════════════════════════════════════════
# Feature C: The "Body" (Interactive CLI)
# ═══════════════════════════════════════════════════════════════════════════════
def display_proposed_command(command: str):
    """Display the proposed command with styling."""
    border = "═" * 60
    
    print(f"{Colors.YELLOW}{border}{Colors.RESET}")
    print(f"{Colors.GREEN}{Colors.BOLD}👉 Proposed Action:{Colors.RESET}")
    print(f"\n   {Colors.CYAN}{Colors.BOLD}{command}{Colors.RESET}\n")
    print(f"{Colors.YELLOW}{border}{Colors.RESET}\n")


def get_user_confirmation() -> bool:
    """Prompt user for execution confirmation."""
    while True:
        try:
            choice = input(f"{Colors.BOLD}[E]xecute  [C]ancel : {Colors.RESET}").strip().lower()
            
            if choice in ('e', 'execute', 'y', 'yes'):
                return True
            elif choice in ('c', 'cancel', 'n', 'no', 'q', 'quit'):
                return False
            else:
                print(f"{Colors.DIM}  → Please enter 'E' to execute or 'C' to cancel{Colors.RESET}")
        except KeyboardInterrupt:
            print(f"\n{Colors.DIM}  → Operation cancelled{Colors.RESET}")
            return False
        except EOFError:
            return False


def execute_command(command: str):
    """Execute the shell command."""
    print(f"\n{Colors.GREEN}▶ Executing command...{Colors.RESET}\n")
    print(f"{Colors.DIM}{'─' * 60}{Colors.RESET}\n")
    
    try:
        # Run the command in the user's shell
        result = subprocess.run(
            command,
            shell=True,
            executable=os.environ.get('SHELL', '/bin/bash')
        )
        
        print(f"\n{Colors.DIM}{'─' * 60}{Colors.RESET}")
        
        if result.returncode == 0:
            print_success(f"Command completed successfully (exit code: {result.returncode})")
        else:
            print(f"{Colors.YELLOW}⚠ Command finished with exit code: {result.returncode}{Colors.RESET}")
            
    except FileNotFoundError:
        print_error("Shell not found. Cannot execute command.")
        sys.exit(1)
    except Exception as e:
        print_error(f"Execution failed: {e}")
        sys.exit(1)


def show_usage():
    """Display usage information."""
    print(f"""
{Colors.BOLD}Usage:{Colors.RESET}
  kx "<your request in natural language>"

{Colors.BOLD}Examples:{Colors.RESET}
  kx "find all python files modified today"
  kx "check for open ports on 192.168.1.1"
  kx "compress the logs folder into a tar.gz"
  kx "show system resource usage"
  kx "extract this tar.gz file"

{Colors.BOLD}Options:{Colors.RESET}
  --help, -h     Show this help message
  --version, -v  Show version information
""")


def show_version():
    """Display version information."""
    print(f"""
{Colors.CYAN}KORTEX{Colors.RESET} v1.0.0
The Neural Layer for your Linux Kernel
By Anugrah K

Model: {MODEL_NAME}
Config: {CONFIG_FILE}
Repository: https://github.com/anugrahk21/Kortex-CLI
""")


# ═══════════════════════════════════════════════════════════════════════════════
# Main Entry Point
# ═══════════════════════════════════════════════════════════════════════════════
def main():
    """Main entry point for KORTEX."""
    # Handle special flags
    if len(sys.argv) < 2:
        print_banner()
        show_usage()
        sys.exit(0)
    
    arg = sys.argv[1].lower()
    
    if arg in ('--help', '-h', 'help'):
        print_banner()
        show_usage()
        sys.exit(0)
    
    if arg in ('--version', '-v', 'version'):
        print_banner()
        show_version()
        sys.exit(0)
    
    # Get the user's query (join all arguments)
    user_query = " ".join(sys.argv[1:])
    
    # Load API key (Feature A)
    api_key = load_api_key()
    
    # Generate command using AI (Feature B)
    command = generate_command(user_query, api_key)
    
    # Display proposed command (Feature C)
    display_proposed_command(command)
    
    # Get user confirmation
    if get_user_confirmation():
        execute_command(command)
    else:
        print(f"\n{Colors.DIM}  → Operation cancelled. No changes made.{Colors.RESET}\n")
        sys.exit(0)


if __name__ == "__main__":
    main()
