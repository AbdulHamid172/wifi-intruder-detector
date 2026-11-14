# 🛡️ WiFi Intruder Detector

A cross-platform desktop app that scans your WiFi network, lists every connected device, and highlights unknown ones so you can spot intruders.

Built with **Python + PySide6 (Qt)** on top of **nmap**.

**Platforms:** Linux · Windows · macOS

---

## ⚠️ Legal

**Only scan networks you own or have explicit permission to monitor.** Scanning other people's WiFi is illegal in most countries (Kenya — Computer Misuse Act 2018; USA — CFAA + Wiretap Act; UK — CMA 1990; EU — GDPR).

This tool is **defensive only** — no deauth, no cracking, no offensive features.

---

## Features

- Auto-detects your local subnet
- Scans every device: **IP · MAC · vendor**
- **Unknown devices highlighted in red**
- **Trust** recognized devices — they turn green and stop being flagged
- Trusted list saved locally (`known_devices.json`)
- Dark UI with sidebar (Dashboard · Devices · Settings · About)

---

## Requirements

- **Python 3.9+**
- **nmap** installed at OS level (not pip)
- **~80 MB** for PySide6 dependencies

---

## Install (Linux)

```bash
# 1. Install nmap and Python tools
sudo apt update
sudo apt install nmap python3 python3-venv python3-pip git -y

# 2. Clone the repo
cd ~
git clone https://github.com/AbdulHamid172/wifi-intruder-detector.git
cd wifi-intruder-detector

# 3. Set up isolated Python environment
python3 -m venv venv
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Run
sudo python3 main.py
```

**On macOS:** `brew install nmap` before step 2.

**On Windows:** install nmap from https://nmap.org/download.html (check "Add to PATH"), then use `venv\Scripts\activate` in step 3.

---

## How to use

1. **Dashboard tab** → click **🔍 Scan Network**. Wait 10–30 seconds.
2. **Devices tab** → review the table:
   - 🟢 Green = trusted (safe)
   - 🔴 Red = unknown (investigate)
3. **Trust a device** you recognize → select the row → click **✅ Trust**. It turns green.
4. **Repeat weekly** — any new red row = check the vendor/MAC. All green = network clean.

**Every run after first install:**

```bash
cd ~/wifi-intruder-detector
source venv/bin/activate
sudo python3 main.py
```

`sudo` is needed because nmap requires raw network access — without it, 0 devices are found.

---

## Troubleshooting

| Problem | Fix |
|---|---|
| `nmap: command not found` | `sudo apt install nmap -y` |
| `ModuleNotFoundError: PySide6` | `source venv/bin/activate && pip install -r requirements.txt` |
| Scan finds 0 devices | Forgot `sudo` — run `sudo python3 main.py` |
| Wrong subnet detected | Fix in Settings tab, or `ip -4 route show default` to find yours |
| `qt.qpa.plugin: xcb` error | `sudo apt install libxcb-cursor0 libxcb-xinerama0 -y` |

---

## Tech stack

Python 3.9+ · [PySide6](https://doc.qt.io/qtforpython-6/) · [python-nmap](https://pypi.org/project/python-nmap/) · [nmap](https://nmap.org/)

---

## Uninstall

```bash
cd ~
rm -rf wifi-intruder-detector
```

---

## Author

**Abdul Hamid** — IT student, Mount Kenya University (Coast Campus)

GitHub: [@AbdulHamid172](https://github.com/AbdulHamid172)

---

**⚠️ Only scan networks you own.**
