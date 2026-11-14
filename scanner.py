"""Scanning logic. Requires nmap installed on the system."""
import subprocess
import nmap

try:
    from mac_vendors_client import get_vendor as _get_vendor
    def get_vendor(mac):
        return _get_vendor(mac)
except Exception:
    def get_vendor(mac):
        return "Unknown vendor"


def detect_subnet():
    """Auto-detect local subnet from default route."""
    try:
        out = subprocess.check_output(
            ["ip", "-4", "route", "show", "default"],
            text=True, stderr=subprocess.DEVNULL,
        )
        iface = out.split("dev")[1].split()[0]
        addr = subprocess.check_output(
            ["ip", "-4", "addr", "show", iface], text=True
        )
        for line in addr.splitlines():
            line = line.strip()
            if line.startswith("inet "):
                ip_cidr = line.split()[1]
                ip, cidr = ip_cidr.split("/")
                base = ".".join(ip.split(".")[:3]) + ".0"
                return f"{base}/{cidr}"
    except Exception:
        pass
    return "192.168.1.0/24"


def _extract_hostname(host_data):
    """Pull the best hostname string out of an nmap host dict."""
    hostnames = host_data.get("hostnames", [])
    for entry in hostnames:
        name = (entry.get("name") or "").strip()
        if name:
            return name
    return ""


def scan_network(subnet, progress_cb=None):
    """Return dict {mac_lower: {ip, vendor, hostname}}."""
    nm = nmap.PortScanner()
    if progress_cb:
        progress_cb(f"Scanning {subnet} ... (may take ~10s)")

    # -sn  = ping/ARP sweep (no port scan)
    # -R   = always try reverse-DNS (gives us hostnames more often)
    nm.scan(hosts=subnet, arguments="-sn -R")

    devices = {}
    for host in nm.all_hosts():
        addrs = nm[host].get("addresses", {})
        mac = addrs.get("mac")
        ip = addrs.get("ipv4")
        if not mac:
            continue
        mac = mac.lower()

        hostname = _extract_hostname(nm[host])

        try:
            vendor = get_vendor(mac) or "Unknown vendor"
        except Exception:
            vendor = "Unknown vendor"

        devices[mac] = {
            "ip": ip,
            "vendor": vendor,
            "hostname": hostname,
        }

    if progress_cb:
        progress_cb(f"Scan complete — {len(devices)} device(s) found.")
    return devices
