import json
import os

KNOWN_FILE = "known_devices.json"


def load_known():
    if not os.path.exists(KNOWN_FILE):
        with open(KNOWN_FILE, "w") as f:
            json.dump({}, f, indent=2)
        return {}
    with open(KNOWN_FILE, "r") as f:
        data = json.load(f)
    return {k.lower(): v for k, v in data.items()}


def save_known(known):
    with open(KNOWN_FILE, "w") as f:
        json.dump(known, f, indent=2)