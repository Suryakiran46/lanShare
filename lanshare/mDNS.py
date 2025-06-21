import socket
import platform
import json
import os
import argparse
from zeroconf import Zeroconf, ServiceInfo
import time

CONFIG_FILE = "config.json"

# --- Parse Arguments ---
parser = argparse.ArgumentParser(description="LANShare mDNS registration")
parser.add_argument('--rename', action='store_true', help='Rename your display name')
args = parser.parse_args()

# --- Load or Set Display Name ---
def get_display_name():
    if os.path.exists(CONFIG_FILE) and not args.rename:
        with open(CONFIG_FILE, "r") as f:
            config = json.load(f)
            return config.get("username", "Unknown")
    else:
        new_name = input("Enter your display name: ").strip()
        with open(CONFIG_FILE, "w") as f:
            json.dump({"username": new_name}, f)
        return new_name

user_name = get_display_name()

# --- System Information ---
device_name = socket.gethostname()
os_name = platform.system()
os_version = platform.version()
ip_address = socket.gethostbyname(device_name)

# --- mDNS Properties ---
desc = {
    "name": user_name,
    "device": device_name,
    "os": f"{os_name} {os_version}",
    "version": "1.0.0",
    "type": "lanChat"
}

info = ServiceInfo(
    type_="_lanShare._tcp.local.",
    name=f"{user_name}._lanShare._tcp.local.",
    port=8080,
    addresses=[socket.inet_aton(ip_address)],
    properties=desc,
    server=f"{user_name}.local."
)

# --- Register Service ---
zeroconf = Zeroconf()
print(f"[+] Registering mDNS service as '{user_name}._lanShare._tcp.local.' pointing to {ip_address}")
zeroconf.register_service(info)

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\n[-] Shutting down mDNS...")
    zeroconf.unregister_service(info)
    zeroconf.close()
