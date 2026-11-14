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
- Scans every device: **IP · MAC · hostname · vendor**
- **Unknown devices highlighted in red**
- **Trust** recognized devices — they turn green and stop being flagged
- Trusted list saved locally (`known_devices.json`)
- **Hostname resolution** per device (when the device advertises one)
- **Sortable table** — click any column header
- **First-seen / last-seen** timestamps per device
- **Desktop notification** when unknown devices appear
- **Export scan results to CSV**
- Dark UI with sidebar (Dashboard · Devices · Settings · About)

---

## Requirements

- **Python 3.9+**
- **nmap** installed at OS level (not pip)
- **~80 MB** for PySide6 dependencies

---

## Install (Linux)

    sudo apt update
    sudo apt install nmap python3 python3-venv python3-pip git libnotify-bin -y

    cd ~
    git clone https://github.com/AbdulHamid172/wifi-intruder-detector.git
    cd wifi-intruder-detector

    python3 -m venv venv
    source venv/bin/activate

    pip install -r requirements.txt

**On macOS:** `brew install nmap` before step 2.

**On Windows:** install nmap from https://nmap.org/download.html (check "Add to PATH"), then use `venv\Scripts\activate` in step 3.

---

## How to use

1. **Dashboard tab** → click **🔍 Scan Network**. Wait 10–30 seconds.
2. **Devices tab** → review the table:
   - 🟢 Green = trusted (safe)
   - 🔴 Red = unknown (investigate)
3. **Trust a device** you recognize → select the row → click **✅ Trust**. It turns green.
4. **Export** any scan → **📤 Export CSV** for a timestamped record.
5. **Repeat weekly** — any new red row = check the vendor/MAC. All green = network clean.

**Every run after first install:**

    cd ~/wifi-intruder-detector
    source venv/bin/activate
    sudo venv/bin/python main.py

`sudo` is needed because nmap requires raw network access — without it, 0 devices are found.

---

## Troubleshooting

| Problem | Fix |
|---|---|
| `nmap: command not found` | `sudo apt install nmap -y` |
| `ModuleNotFoundError: PySide6` | `source venv/bin/activate && pip install -r requirements.txt` |
| Scan finds 0 devices | Forgot `sudo` — run `sudo venv/bin/python main.py` |
| Wrong subnet detected | Fix in Settings tab, or `ip -4 route show default` to find yours |
| `qt.qpa.plugin: xcb` error | `sudo apt install libxcb-cursor0 libxcb-xinerama0 -y` |
| No desktop notification | `sudo apt install libnotify-bin -y` |
| All devices show "Unknown vendor" | Normal — modern phones randomize their MAC for privacy. Trust your own devices to stop them being flagged. |

---

## Tech stack

Python 3.9+ · PySide6 · python-nmap · nmap

---

## Uninstall

    cd ~
    rm -rf wifi-intruder-detector

---

## Author

**Abdul Hamid** — IT student, Mount Kenya University (Coast Campus)

GitHub: [@AbdulHamid172](https://github.com/AbdulHamid172)

---

**⚠️ Only scan networks you own.**
