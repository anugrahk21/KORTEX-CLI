<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/AI-Gemini%201.5%20Flash-orange?style=for-the-badge&logo=google&logoColor=white" alt="AI">
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

```bash
$ kx "find all files larger than 100MB"

🧠 KORTEX is analyzing...

════════════════════════════════════════════════════════════
👉 Proposed Action:
   find . -type f -size +100M

════════════════════════════════════════════════════════════

[E]xecute  [C]ancel : 
```

## 🚀 Quick Start

### 1. Clone & Install

```bash
git clone https://github.com/anugrahk21/Kortex-CLI.git
cd Kortex-CLI
chmod +x install.sh
./install.sh
```

### 2. Get Your API Key

Visit: **https://makersuite.google.com/app/apikey**

The installer will prompt you to enter it.

### 3. Use It!

```bash
kx "your request here"
```

## 💡 Examples

```bash
# File operations
kx "find all python files modified today"
kx "compress this folder"

# Network/Security
kx "scan 192.168.1.1 for open ports"
kx "show active network connections"

# System
kx "show disk usage sorted by size"
kx "find processes using most CPU"
```

## ⚙️ Configuration

Your API key is stored in `.env` file:

```bash
# .env
GEMINI_API_KEY=your_key_here
```

To update: Edit `.env` or delete it and run `./install.sh` again.

## 📁 Structure

```
Kortex-CLI/
├── kortex.py        # Main app
├── install.sh       # Installer (creates .env)
├── .env             # Your API key (git-ignored)
├── requirements.txt # Dependencies
├── README.md        # Docs
└── LICENSE          # MIT
```

## 🛠️ Manual Setup

```bash
pip install google-genai
echo "GEMINI_API_KEY=your_key_here" > .env
chmod +x kortex.py
sudo ln -s $(pwd)/kortex.py /usr/local/bin/kx
```

## 📄 License

MIT License - See [LICENSE](LICENSE)

---

<p align="center">
  <b>KORTEX-CLI</b> by <a href="https://github.com/anugrahk21">Anugrah K</a>
  <br>
  ⭐ Star if useful!
</p>
