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

```
KORTEX> find all files larger than 100MB

🧠 Analyzing...

════════════════════════════════════════════════════════════
👉 Proposed Command:

   find . -type f -size +100M

════════════════════════════════════════════════════════════

[E]xecute  [R]efine  [C]ancel
> 
```

---

## 🚀 Installation (3 Steps)

### Step 1: Clone
```bash
git clone https://github.com/anugrahk21/Kortex-CLI.git
cd Kortex-CLI
```

### Step 2: Run Installer
```bash
chmod +x install.sh
./install.sh
```

The installer will:
- ✅ Check Python & pip
- ✅ Install `google-genai` (prompts you first)
- ✅ Ask for your API key
- ✅ Create global `kx` command

### Step 3: Get API Key (Free)
When prompted, get your key from: **https://makersuite.google.com/app/apikey**

**That's it!** Now use `kx` from anywhere on your system.

---

## 💡 Usage

KORTEX has **two modes**:

---

### Mode 1: Interactive Shell (`kx`)

Just type `kx` to enter the interactive `KORTEX>` prompt (like `msfconsole`):

```bash
kx
```

```
KORTEX-CLI v1.1.0 | Type 'help' for commands, 'exit' to quit

KORTEX> find large files
🧠 Analyzing...
════════════════════════════════════════════════════════════
👉 Proposed Command:
   find . -type f -size +100M
════════════════════════════════════════════════════════════
[E]xecute  [R]efine  [C]ancel
> 
```

**Commands inside the shell:**

| Command | Description |
|---------|-------------|
| `<your request>` | Translate to shell command |
| `help` | Show help |
| `update` | Update KORTEX from GitHub |
| `models` | List available AI models |
| `version` | Show version info |
| `clear` | Clear screen |
| `exit` | Exit KORTEX |

**Action options after command is generated:**
- `[E]` - Execute the command
- `[R]` - Refine (ask differently)
- `[C]` - Cancel

---

### Mode 2: One-Shot (`kx "request"`)

Run a single query directly from terminal:

```bash
kx "show disk usage"
```

Quick and direct - perfect for scripts or fast lookups.

---

### CLI Flags (work from anywhere)

```bash
kx --help       # Show help
kx --version    # Show version  
kx --models     # List AI models
kx update       # Update KORTEX
```

---

## 📝 Examples

```bash
# File operations
kx "find all python files modified today"
kx "compress this folder to zip"
kx "delete files older than 30 days"

# Network/Security
kx "scan 192.168.1.1 for open ports"
kx "show active network connections"
kx "check if port 80 is open"

# System
kx "show disk usage sorted by size"
kx "find processes using most CPU"
kx "show memory usage"
```

---

## 🔄 Updating

Inside KORTEX shell:
```
KORTEX> update
```

Or from terminal:
```bash
kx update
```

No need to manually `git pull` or fix permissions — the update command handles everything!

---

## ⚙️ Configuration

Your API key is stored in `.env` file (inside the Kortex-CLI folder):

```bash
GEMINI_API_KEY=your_key_here
```

To change it: Edit `.env` or delete it and run `./install.sh` again.

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

If you prefer manual setup:

```bash
pip install google-genai
echo "GEMINI_API_KEY=your_key" > .env
chmod +x kortex.py
sudo ln -s $(pwd)/kortex.py /usr/local/bin/kx
```

---

## 📄 License

MIT License - See [LICENSE](LICENSE)

---

<p align="center">
  <b>KORTEX-CLI</b> by <a href="https://github.com/anugrahk21">Anugrah K</a>
  <br><br>
  ⭐ Star if useful!
</p>
