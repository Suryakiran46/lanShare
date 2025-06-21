from zeroconf import Zeroconf, ServiceBrowser
import socket
import time

devices = {}

class MyListener:
    def __init__(self, zeroconf):
        self.zeroconf = zeroconf

    def print_devices(self):
        print("\n----- Devices on Network -----")
        if not devices:
            print("No devices available.")
        else:
            print(f"{'Name':<12} {' IP Address':<15} {' Status'}")
            print("-" * 35)
            for dev in devices.values():
                print(f"{dev['name']:<12} {dev['ip']:<15} {dev['status']}")
            print()

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
            self.print_devices()

    def remove_service(self, zeroconf, type, name):
        if name in devices:
            devices[name]["status"] = "Inactive"
            self.print_devices()

    def update_service(self, zeroconf, type, name):
        pass

zeroconf = Zeroconf()
print("[*] Scanning for LANShare services...")
listener = MyListener(zeroconf)
browser = ServiceBrowser(zeroconf, "_lanShare._tcp.local.", listener)

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\n[-] Stopping discovery")
    zeroconf.close()
