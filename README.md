<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python Version">
  <img src="https://img.shields.io/badge/AI-Gemini%201.5%20Flash-orange?style=for-the-badge&logo=google&logoColor=white" alt="AI Model">
  <img src="https://img.shields.io/badge/Platform-Linux%20%7C%20macOS-green?style=for-the-badge&logo=linux&logoColor=white" alt="Platform">
  <img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge" alt="License">
</p>

<h1 align="center">
  <br>
  🧠 KORTEX
  <br>
</h1>

<h4 align="center">A project by <a href="https://github.com/anugrahk21">Anugrah K</a></h4>

<h3 align="center">The Neural Layer for your Linux Kernel</h3>

<p align="center">
  <b>Stop context-switching. Start commanding.</b><br>
  Translate natural language into precise shell commands using AI.
</p>

---

## 🎯 What is KORTEX?

**KORTEX** is a lightweight AI-powered CLI tool (invoked via `kx` command) that bridges the gap between human intent and complex Linux shell execution. Forget memorizing cryptic command syntax—just describe what you want to do in plain English, and KORTEX translates it into precise terminal commands.

```bash
$ kx "find all files larger than 100MB modified in the last week"

🧠 KORTEX is analyzing...

════════════════════════════════════════════════════════════
👉 Proposed Action:
   find . -type f -size +100M -mtime -7

════════════════════════════════════════════════════════════

[E]xecute  [C]ancel :
```

## ✨ Features

- 🚀 **Instant Translation** — Natural language to shell commands in < 2 seconds
- 🔒 **Secure by Design** — API keys stored locally with proper file permissions
- ⚡ **Zero Context Switching** — Stay in your terminal workflow
- 🎨 **Beautiful CLI** — ANSI-colored output for clarity
- 🛡️ **Confirmation Loop** — Always review before execution
- 🐧 **Multi-Platform** — Linux (Ubuntu, Kali, Debian, Arch) & macOS

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or later
- pip (Python package manager)
- A [Google Gemini API Key](https://makersuite.google.com/app/apikey) (Free tier available)

### Installation

```bash
# Clone the repository
git clone https://github.com/anugrahk21/Kortex-CLI.git
cd Kortex-CLI

# Run the installer
chmod +x install.sh
./install.sh
```

The installer will:
1. ✅ Check Python & pip installation
2. ✅ Install required dependencies
3. ✅ Securely prompt for your Gemini API key
4. ✅ Create the global `kx` command

### Manual Setup (Alternative)

If you prefer manual setup:

```bash
# Install dependencies
pip install -r requirements.txt

# Create API key file
echo "YOUR_API_KEY_HERE" > ~/.kortex_key
chmod 600 ~/.kortex_key

# Make script executable
chmod +x kortex.py

# Create symlink (requires sudo)
sudo ln -s $(pwd)/kortex.py /usr/local/bin/kx
```

## 💡 Usage Examples

### Security & Penetration Testing

```bash
kx "scan 192.168.1.1 for open ports"
# → nmap -sS -sV 192.168.1.1

kx "check for SMB vulnerabilities on 10.10.10.5"
# → nmap -p 445 --script smb-vuln* 10.10.10.5

kx "capture network traffic on eth0"
# → sudo tcpdump -i eth0 -w capture.pcap
```

### File Operations

```bash
kx "find all python files modified today"
# → find . -name "*.py" -type f -mtime 0

kx "compress the logs folder"
# → tar -czvf logs.tar.gz ./logs

kx "extract this tar.gz file"
# → tar -xzvf file.tar.gz
```

### System Administration

```bash
kx "show disk usage sorted by size"
# → du -sh * | sort -rh | head -20

kx "find processes using more than 50% CPU"
# → ps aux --sort=-%cpu | head -10

kx "check which service is using port 8080"
# → lsof -i :8080
```

### Networking

```bash
kx "test connectivity to google.com"
# → ping -c 4 google.com

kx "download a file from this URL"
# → wget https://example.com/file.zip

kx "show all active network connections"
# → netstat -tuln
```

## ⚙️ Configuration

### API Key Location

Your API key is stored at: `~/.kortex_key`

To update your API key:
```bash
echo "NEW_API_KEY" > ~/.kortex_key
chmod 600 ~/.kortex_key
```

### Changing the AI Model

By default, KORTEX uses `gemini-1.5-flash` for optimal speed. To change this, edit `kortex.py`:

```python
MODEL_NAME = "gemini-1.5-pro"  # For more complex queries
```

## 🛡️ Security Considerations

1. **API Key Protection**: Your API key is stored locally in `~/.kortex_key` with `600` permissions (owner read/write only).

2. **Command Review**: KORTEX always shows the proposed command before execution. Review carefully!

3. **No Automatic Execution**: Commands never run without your explicit confirmation.

4. **Trust Model**: This version trusts user judgment. Complex safeguards (like blocking `rm -rf`) are planned for future versions.

## 📁 Project Structure

```
Kortex-CLI/
├── kortex.py            # Main application logic
├── install.sh           # Automated setup script
├── requirements.txt     # Python dependencies
└── README.md            # Documentation (you are here!)
```

## 🔧 Troubleshooting

### "Command 'kx' not found"

```bash
# Restart your terminal, or:
source ~/.bashrc

# Verify symlink exists:
ls -la /usr/local/bin/kx
```

### "API key not found"

```bash
# Create the key file:
echo "YOUR_KEY" > ~/.kortex_key
chmod 600 ~/.kortex_key
```

### "Permission denied" errors

```bash
# Fix script permissions:
chmod +x kortex.py

# Fix config permissions:
chmod 600 ~/.kortex_key
```

### API Errors

- **Invalid API Key**: Get a new key from [Google AI Studio](https://makersuite.google.com/app/apikey)
- **Quota Exceeded**: Check your [Google Cloud Console](https://console.cloud.google.com/) for billing

## 🗺️ Roadmap

- [ ] Command history & favorites
- [ ] Dangerous command detection & warnings
- [ ] Multi-command pipeline support
- [ ] Custom aliases & shortcuts
- [ ] Shell integration (bash-completion)
- [ ] Offline mode with local LLM

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<p align="center">
  <b>KORTEX - Built with 🧠 by <a href="https://github.com/anugrahk21">Anugrah K</a></b>
  <br>
  <i>For security enthusiasts, system administrators, and terminal power users.</i>
  <br><br>
  <a href="https://github.com/anugrahk21/Kortex-CLI">⭐ Star Kortex-CLI</a> if you find it useful!
</p>
