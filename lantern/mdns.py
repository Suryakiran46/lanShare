import socket
import platform
import json
import os
import time
from pathlib import Path
from zeroconf import Zeroconf, ServiceInfo

zeroconf = None
current_info = None

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

def run_mdns(stop_event, status ="Active"):
    global zeroconf, current_info
    user_name = get_display_name()
    if not user_name:
        print("Error: Username not set in config.json.")
        return

    device_name = socket.gethostname()
    os_name = platform.system()
    os_version = platform.version()

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 80))
    ip_address = s.getsockname()[0]
    s.close()
    
    desc = {
        "name": user_name,
        "device": device_name,
        "os": f"{os_name} {os_version}",
        "status": "Active"
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
    current_info = info
    print(f"[+] Registering mDNS service as '{user_name}._lantern._tcp.local.' pointing to {ip_address}")
    zeroconf.register_service(info)
    try:
        while not stop_event.is_set():
            time.sleep(1)
    finally:
        print("\n[-] Shutting down mDNS...")
        zeroconf.unregister_service(info)
        zeroconf.close()

def update_status(new_status):
    global zeroconf, current_info
    if not zeroconf or not current_info:
        print("Zeroconf or service not initialized.")
        return

    # Copy existing props
    props = {k.decode() if isinstance(k, bytes) else k: v.decode() if isinstance(v, bytes) else v
             for k, v in current_info.properties.items()}

    props["status"] = new_status  # Update status

    new_info = ServiceInfo(
        type_=current_info.type,
        name=current_info.name,
        addresses=current_info.addresses,
        port=current_info.port,
        properties=props,
        server=current_info.server
    )

    zeroconf.update_service(new_info)
    current_info = new_info 
    print(f"[+] mDNS status updated to '{new_status}'")
