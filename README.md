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

**KORTEX** is an AI-powered CLI tool that translates natural language into shell commands. Stop Googling syntax — just describe what you want.

```bash
$ kx "find all files larger than 100MB"

🧠 Analyzing...

════════════════════════════════════════════════════════════
👉 Proposed Command:

   find . -type f -size +100M

════════════════════════════════════════════════════════════

[E]xecute  [R]efine  [C]ancel
> e

▶ Executing...

./backup.tar.gz
./videos/movie.mp4

✓ Done (exit code: 0)
```

---

## 🚀 Installation

### Step 1: Clone
```bash
git clone https://github.com/anugrahk21/Kortex-CLI.git
cd Kortex-CLI
```

### Step 2: Install
```bash
chmod +x install.sh
./install.sh
```

### Step 3: Get API Key (Free)
When prompted, get your key from: **https://makersuite.google.com/app/apikey**

**Done!** Use `kx` from anywhere.

---

## 💡 Usage

```bash
kx "<your request>"
```

### How It Works

| Step | What Happens |
|------|--------------|
| 1 | You describe what you want in plain English |
| 2 | AI generates the shell command |
| 3 | You choose: **[E]xecute**, **[R]efine**, or **[C]ancel** |

### Action Options

| Key | Action | Description |
|-----|--------|-------------|
| `E` | Execute | Run the command |
| `R` | Refine | Ask again with different wording |
| `C` | Cancel | Cancel without running |

---

## 📝 Examples

### File Operations
```bash
kx "find all python files"
kx "find files larger than 100MB"
kx "compress this folder to zip"
kx "delete files older than 30 days"
```

### Network & Security
```bash
kx "scan 192.168.1.1 for open ports"
kx "show active network connections"
kx "check if port 80 is open"
kx "show my public IP"
```

### System Administration
```bash
kx "show disk usage sorted by size"
kx "find processes using most CPU"
kx "show memory usage"
kx "list running services"
```

---

## 🛠️ Commands

| Command | Description |
|---------|-------------|
| `kx "<request>"` | Translate to shell command |
| `kx --help` | Show help |
| `kx --version` | Show version |
| `kx --models` | List available AI models |
| `kx update` | Update KORTEX from GitHub |

---

## 🔄 Updating

```bash
kx update
```

Handles everything automatically — no manual git commands needed!

---

## ⚙️ Configuration

API key is stored in `.env`:

```
GEMINI_API_KEY=your_key_here
```

To change: Edit `.env` or delete it and run `./install.sh` again.

---

## 📁 Structure

```
Kortex-CLI/
├── kortex.py        # Main application
├── install.sh       # Installer
├── .env             # API key (git-ignored)
├── requirements.txt # Dependencies
├── README.md        
└── LICENSE          
```

---

## 🛠️ Manual Installation

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
