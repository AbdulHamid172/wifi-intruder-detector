from scanner import scan_network, detect_subnet

devices = scan_network(detect_subnet())
print(f"\nFound {len(devices)} device(s):\n")
for mac, info in devices.items():
    print(f"{info['ip']:<15} {mac}  host={info['hostname']!r:<25} vendor={info['vendor']}")
