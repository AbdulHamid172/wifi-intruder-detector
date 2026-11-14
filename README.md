# 🛡️ WiFi Intruder Detector

A desktop app that scans your home WiFi and flags unauthorized devices.

**Platforms:** Linux • Windows • macOS
**Developed by Abdul Hamid**

## ⚠️ Legal
Only scan networks you own. Scanning other networks is illegal.

## Features
- Auto-detects your subnet
- Scans all devices on the network (IP + MAC + vendor)
- Trusted-device list saved locally
- Unknown devices highlighted in red
- Dark UI with sidebar navigation

## Install

```bash
sudo apt install nmap -y          # Linux
# brew install nmap               # macOS
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt