import socket
import platform
import json
import os
import time
from pathlib import Path
from zeroconf import Zeroconf, ServiceInfo



def get_config_path():
    system=platform.system()
    home=Path.home()
    if system=="Windows":
        base_dir=Path(os.environ.get("APPDATA",home))
        config_dir=base_dir / "lantern"
    elif system in ("Linux","Darwin"):
        config_dir = home / ".config" / "lantern"
    else:
        #Fallback for unknown/uncommon Oses
        config_dir = home/".lantern"
    config_dir.mkdir(parents=True,exist_ok=True)
    return config_dir/"config.json"

CONFIG_FILE = get_config_path()

def get_display_name():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            config = json.load(f)
        return config.get("username", None)
    else:
        return None

def set_display_name(new_name):
    with open(CONFIG_FILE, "w") as f:
        json.dump({"username": new_name}, f)

def run_mdns(stop_event):
    user_name = get_display_name()
    if not user_name:
        print("Error: Username not set in config.json.")
        return

    device_name = socket.gethostname()
    os_name = platform.system()
    os_version = platform.version()
    ip_address = socket.gethostbyname(device_name)
    desc = {
        "name": user_name,
        "device": device_name,
        "os": f"{os_name} {os_version}",
        "version": "1.0.0",
        "type": "lanChat"
    }
    info = ServiceInfo(
        type_="_lantern._tcp.local.",
        name=f"{user_name}._lantern._tcp.local.",
        port=8080,
        addresses=[socket.inet_aton(ip_address)],
        properties=desc,
        server=f"{user_name}.local."
    )
    zeroconf = Zeroconf()
    print(f"[+] Registering mDNS service as '{user_name}._lantern._tcp.local.' pointing to {ip_address}")
    zeroconf.register_service(info)
    try:
        while not stop_event.is_set():
            time.sleep(1)
    finally:
        print("\n[-] Shutting down mDNS...")
        zeroconf.unregister_service(info)
        zeroconf.close()
