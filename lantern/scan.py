from zeroconf import Zeroconf, ServiceBrowser
import socket
import time
import os

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def run_scan(stop_event, refresh_interval=2):
    devices = {}
    class MyListener:
        def __init__(self, zeroconf):
            self.zeroconf = zeroconf
        def add_service(self, zeroconf, type, name):
            info = zeroconf.get_service_info(type, name)
            if info and info.addresses:
                ip = socket.inet_ntoa(info.addresses[0])
                props = {k.decode(): v.decode() for k, v in info.properties.items()}
                devices[name] = {
                    "name": props.get("name", "Unknown"),
                    "ip": ip,
                    "status": "Active"
                }
        def remove_service(self, zeroconf, type, name):
            if name in devices:
                devices[name]["status"] = "Inactive"
        def update_service(self, zeroconf, type, name):
            pass
    zeroconf = Zeroconf()
    listener = MyListener(zeroconf)
    browser = ServiceBrowser(zeroconf, "_lantern._tcp.local.", listener)
    try:
        while not stop_event.is_set():
            clear_terminal()
            print("----- Devices on Network -----")
            if not devices:
                print("No devices available.")
            else:
                print(f"{'Name':<12} {'IP Address':<15} {'Status'}")
                print("-" * 35)
                for dev in devices.values():
                    print(f"{dev['name']:<12} {dev['ip']:<15} {dev['status']}")
            print("\n(Type commands below. Use 'stopscan' to stop scanning.)")
            time.sleep(refresh_interval)
    finally:
        zeroconf.close()
