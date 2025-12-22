<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/AI-Gemini%202.5-orange?style=for-the-badge&logo=google&logoColor=white" alt="AI">
  <img src="https://img.shields.io/badge/Platform-Linux%20%7C%20macOS-green?style=for-the-badge&logo=linux&logoColor=white" alt="Platform">
</p>

<h1 align="center">🧠 KORTEX-CLI</h1>
<h4 align="center">The Neural Layer for your Linux Kernel</h4>
<h5 align="center">By <a href="https://github.com/anugrahk21">Anugrah K</a></h5>

<p align="center">
  <b>Translate natural language → shell commands using AI</b>
</p>

---

## 🎯 What is KORTEX?

**KORTEX** is an AI-powered CLI tool that translates natural language into precise shell commands. Stop Googling syntax — just describe what you want.

---

## 🚀 Installation

### Step 1: Clone the Repository
```bash
git clone https://github.com/anugrahk21/Kortex-CLI.git
cd Kortex-CLI
```

### Step 2: Run the Installer
```bash
chmod +x install.sh
./install.sh
```

The installer will:
- ✅ Check Python & pip
- ✅ Install `google-genai` dependency (prompts you first)
- ✅ Ask for your Gemini API key
- ✅ Create global `kx` command (works from anywhere)

### Step 3: Get Your API Key (Free)
When prompted, get your free key from: **https://makersuite.google.com/app/apikey**

**Done!** Now use `kx` from anywhere on your system.

---

## 💡 Usage Modes

KORTEX has **two modes** of operation:

### 1. Interactive Mode (`kx`)

Enter the interactive `KORTEX>` shell (similar to `msfconsole`):

```bash
kx
```

**What you see:**
```
 ██╗  ██╗ ██████╗ ██████╗ ████████╗███████╗██╗  ██╗       ██████╗██╗     ██╗
 ...
KORTEX-CLI v1.1.0 | Type 'help' for commands, 'exit' to quit

KORTEX> 
```

**How it works:**

| Step | Action | Description |
|------|--------|-------------|
| 1 | Type your request | `KORTEX> find large files` |
| 2 | Review the command | AI generates a shell command |
| 3 | Choose action | `[E]xecute`, `[R]efine`, or `[C]ancel` |

**Example Session:**
```
KORTEX> find all python files modified today

🧠 Analyzing...

════════════════════════════════════════════════════════════
👉 Proposed Command:

   find . -name "*.py" -mtime -1

════════════════════════════════════════════════════════════

[E]xecute  [R]efine  [C]ancel
> e

▶ Executing...

./scripts/backup.py
./main.py

✓ Done (exit code: 0)

KORTEX> 
```

---

### 2. One-Shot Mode (`kx "request"`)

Run a single query directly from terminal without entering the shell:

```bash
kx "your request here"
```

**How it works:**

| Step | Action | Description |
|------|--------|-------------|
| 1 | Run command with query | `kx "show disk usage"` |
| 2 | Review the command | AI generates a shell command |
| 3 | Choose action | `[E]xecute`, `[R]efine`, or `[C]ancel` |

**Example:**
```bash
$ kx "compress the logs folder"

🧠 Analyzing...

════════════════════════════════════════════════════════════
👉 Proposed Command:

   tar -czvf logs.tar.gz logs/

════════════════════════════════════════════════════════════

[E]xecute  [R]efine  [C]ancel
> 
```

---

## 🛠️ Built-in Commands

### Commands Inside Interactive Shell (`KORTEX>`)

| Command | Description |
|---------|-------------|
| `<your request>` | Translate natural language to shell command |
| `help` | Show help menu |
| `update` | Update KORTEX-CLI from GitHub |
| `models` | List available AI models |
| `version` | Show version info |
| `clear` | Clear the screen |
| `exit` / `quit` / `q` | Exit KORTEX |

### CLI Flags (Terminal Commands)

| Command | Description |
|---------|-------------|
| `kx` | Enter interactive mode |
| `kx "request"` | One-shot query |
| `kx --help` or `kx -h` | Show help |
| `kx --version` or `kx -v` | Show version |
| `kx --models` | List available AI models |
| `kx update` | Update KORTEX-CLI from GitHub |

### Action Options (After Command is Generated)

| Key | Action | Description |
|-----|--------|-------------|
| `E` | Execute | Run the proposed command |
| `R` | Refine | Ask again with different wording |
| `C` | Cancel | Cancel and return to prompt |

---

## 📝 Examples

### File Operations
```bash
kx "find all python files"
kx "find files larger than 100MB"
kx "compress this folder to zip"
kx "delete files older than 30 days"
kx "count lines of code in this project"
```

### Network & Security
```bash
kx "scan 192.168.1.1 for open ports"
kx "show active network connections"
kx "check if port 80 is open"
kx "show my public IP"
kx "list all listening ports"
```

### System Administration
```bash
kx "show disk usage sorted by size"
kx "find processes using most CPU"
kx "show memory usage"
kx "list all running services"
kx "check system uptime"
```

---

## 🔄 Updating KORTEX

### From Inside Interactive Shell:
```
KORTEX> update
```

### From Terminal:
```bash
kx update
```

The update command automatically:
- ✅ Stashes local changes
- ✅ Pulls latest from GitHub
- ✅ Fixes file permissions

No manual `git pull` or `chmod` needed!

---

## ⚙️ Configuration

Your API key is stored in the `.env` file (inside the Kortex-CLI folder):

```
GEMINI_API_KEY=your_api_key_here
```

**To change your API key:**
1. Edit `.env` file directly, OR
2. Delete `.env` and run `./install.sh` again

---

## 📁 Project Structure

```
Kortex-CLI/
├── kortex.py        # Main application
├── install.sh       # One-time installer
├── .env             # Your API key (git-ignored)
├── requirements.txt # Dependencies
├── README.md        # This file
└── LICENSE          # MIT License
```

---

## 🛠️ Manual Installation

If you prefer manual setup instead of using the installer:

```bash
# Install dependency
pip install google-genai

# Create .env file with your API key
echo "GEMINI_API_KEY=your_key_here" > .env

# Make executable
chmod +x kortex.py

# Create global symlink
sudo ln -s $(pwd)/kortex.py /usr/local/bin/kx
```

---

## 📄 License

MIT License - See [LICENSE](LICENSE)

---

<p align="center">
  <b>KORTEX-CLI</b> by <a href="https://github.com/anugrahk21">Anugrah K</a>
  <br><br>
  ⭐ Star this repo if you find it useful!
</p>
