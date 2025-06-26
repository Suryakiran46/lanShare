import cmd
import threading
from lantern.mdns import run_mdns, get_display_name, set_display_name
from lantern.scan import start_scan

class lanternShell(cmd.Cmd):
    intro = "Welcome to lantern CLI. Type help or ? to list commands.\n"
    prompt = "lantern> "

    def __init__(self):
        super().__init__()
        self.mdns_thread = None
        self.mdns_stop_event = threading.Event()
        self.scan_thread = None
        self.scan_stop_event = threading.Event()
        self.renaming = False 

    def do_start(self, arg):
        """Start mDNS service (register your device on LAN) in the background."""
        if self.mdns_thread and self.mdns_thread.is_alive():
            print("mDNS is already running.")
            return

        user_name = get_display_name()
        if not user_name:
            user_name = ""
            while not user_name:
                user_name = input("Enter your display name: ").strip()
                if not user_name:
                    print("Display name cannot be empty.")
            set_display_name(user_name)

        print("Starting mDNS service in background...")
        self.mdns_stop_event.clear()
        self.mdns_thread = threading.Thread(target=run_mdns, args=(self.mdns_stop_event,), daemon=True)
        self.mdns_thread.start()

    def do_rename(self, arg):
        """Change your display name and restart mDNS."""
        if self.renaming:
            print("A rename operation is already in progress.")
            return
        self.renaming = True
        try:
            if self.mdns_thread and self.mdns_thread.is_alive():
                print("Restarting mDNS with new display name...")
                self.mdns_stop_event.set()
                self.mdns_thread.join()

            user_name = ""
            while not user_name:
                user_name = input("Enter your display name: ").strip()
                if not user_name:
                    print("Display name cannot be empty.")
            set_display_name(user_name)

            self.mdns_stop_event.clear()
            self.mdns_thread = threading.Thread(target=run_mdns, args=(self.mdns_stop_event,), daemon=True)
            self.mdns_thread.start()
        finally:
            self.renaming = False

    def do_scan(self, arg):
        """Scan for devices on the LAN using mDNS (live refresh with prompt_toolkit)."""
        import asyncio
        from lantern.scan_cli import run_scan_prompt_toolkit
        try:
            asyncio.run(run_scan_prompt_toolkit())
        except KeyboardInterrupt:
            print("\nScan Interrupted\n")
        else:
            print("\nExited 'scan' mode returning to lantern shell\n")
        
        
    def do_stopscan(self, arg):
        """Stop the live device scan."""
        if self.scan_thread and self.scan_thread.is_alive():
            print("Stopping device scan...")
            self.scan_stop_event.set()
            self.scan_thread.join()
        else:
            print("No scan running.")

    def do_exit(self, arg):
        """Exit the CLI and stop background services."""
        print("Exiting lantern CLI.")
        if self.mdns_thread and self.mdns_thread.is_alive():
            print("Shutting down mDNS service...")
            self.mdns_stop_event.set()
            self.mdns_thread.join()
        if self.scan_thread and self.scan_thread.is_alive():
            print("Stopping device scan...")
            self.scan_stop_event.set()
            self.scan_thread.join()
        return True

    def do_EOF(self, arg):
        print()
        return self.do_exit(arg)

    def emptyline(self):
        pass

def main():
    shell=lanternShell()
    try:
        shell.cmdloop()
    except KeyboardInterrupt:
        print("\nInterrupted. Exiting...")
        shell.do_exit(None)