import json
import os
from datetime import datetime

KNOWN_FILE = "known_devices.json"


def load_known():
    """Return dict {mac: {name, first_seen, last_seen}}."""
    if not os.path.exists(KNOWN_FILE):
        with open(KNOWN_FILE, "w") as f:
            json.dump({}, f, indent=2)
        return {}
    with open(KNOWN_FILE, "r") as f:
        data = json.load(f)

    # Migrate old format (mac -> "name") to new format (mac -> dict)
    migrated = {}
    for mac, val in data.items():
        mac = mac.lower()
        if isinstance(val, str):
            migrated[mac] = {
                "name": val,
                "first_seen": None,
                "last_seen": None,
            }
        elif isinstance(val, dict):
            migrated[mac] = {
                "name": val.get("name", ""),
                "first_seen": val.get("first_seen"),
                "last_seen": val.get("last_seen"),
            }
    return migrated


def save_known(known):
    with open(KNOWN_FILE, "w") as f:
        json.dump(known, f, indent=2)


def update_seen(known, macs, now=None):
    """Update last_seen for every MAC in the scan; set first_seen if new."""
    now = now or datetime.now().isoformat(timespec="seconds")
    for mac in macs:
        mac = mac.lower()
        if mac not in known:
            known[mac] = {
                "name": "",
                "first_seen": now,
                "last_seen": now,
            }
        else:
            if not known[mac].get("first_seen"):
                known[mac]["first_seen"] = now
            known[mac]["last_seen"] = now
    return known


def trust_device(known, mac, name):
    mac = mac.lower()
    now = datetime.now().isoformat(timespec="seconds")
    entry = known.get(mac, {})
    entry["name"] = name
    entry.setdefault("first_seen", now)
    entry["last_seen"] = now
    known[mac] = entry
    return known


def untrust_device(known, mac):
    known.pop(mac.lower(), None)
    return known


def friendly_time(iso_str):
    """Turn ISO timestamp into '2025-11-14 14:32' or '—'."""
    if not iso_str:
        return "—"
    try:
        return datetime.fromisoformat(iso_str).strftime("%Y-%m-%d %H:%M")
    except Exception:
        return iso_str
