from zeroconf import Zeroconf, ServiceBrowser
import socket

_devices = []

def get_live_devices():
    return _devices.copy()

class MyListener:
    def add_service(self, zeroconf, type, name):
        info = zeroconf.get_service_info(type, name)
        if info and info.addresses:
            ip = socket.inet_ntoa(info.addresses[0])
            props = {k.decode(): v.decode() for k, v in info.properties.items()}
            dev = {
                "name": props.get("name", "Unknown"),
                "ip": ip,
                "status": "Active"
            }
            # Avoid duplicates
            for existing in _devices:
                if existing["ip"] == dev["ip"]:
                    existing.update(dev)
                    return
            _devices.append(dev)
    def update_service(self,zeroconf, type,name):
        #Handles a warning
        self.add_service(zeroconf,type,name)
def start_scan():
    zeroconf = Zeroconf()
    ServiceBrowser(zeroconf, "_lanShare._tcp.local.", MyListener())