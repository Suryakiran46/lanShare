
# 🖧 lantern

**lantern** is a lightweight Python CLI tool for discovering devices on your local network using mDNS (Multicast DNS). Devices running lantern broadcast their presence and system information, allowing you to see other active lantern users on the same LAN in real-time.

---

## 🚀 Features

- 🌐 **mDNS Device Discovery:**  
  Broadcast your device and discover other lantern-enabled devices on the LAN using mDNS.
- 🏷️ **Custom Display Name:**  
  Set and update your display name via the CLI; the name is visible to others on the network.
- 🖥️ **System Metadata Sharing:**  
  Shares your device hostname, OS, and version with other users.
- 🔄 **Real-Time Updates:**  
  Devices appear and disappear in the live-updating device list as they join or leave the network.
- ⚙️ **Interactive CLI:**  
  Use the `lantern` command to enter an interactive shell with commands to start mDNS, scan devices, rename, and exit.
- ✅ **Cross-Platform Ready:**  
  Works on Linux, Windows, and Mac (Python 3.8+).  
  *(Current development/testing is focused on Linux.)*
- 💾 **Persistent Configuration:**  
  Stores your display name in a `config.json` file for persistence.

---

## 🔧 Installation

### 1. Clone the repository

```bash
git clone https://github.com/Suryakiran46/lantern.git
cd lantern
```

### 2. (Optional) Create and activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies and the CLI tool

If you’re using the included `pyproject.toml`:

```bash
pip install -e .
```

This will make the `lantern` command available globally in your environment.

---

## 🧪 Usage

Start the CLI by running:

```bash
lantern
```

You will enter the `lantern>` prompt where you can run commands:

- `start` – Start broadcasting your device on the LAN via mDNS.
- `scan` – Discover other lantern devices on the LAN with a live-updating list.
- `stopscan` – Stop the live device scan.
- `rename` – Change your display name and restart mDNS broadcasting.
- `exit` or `Ctrl+D` – Exit the CLI and stop all background services.

### Example session

```
lantern> start
Starting mDNS service in background...
[+] Registering mDNS service as 'YourName._lantern._tcp.local.' pointing to 192.168.1.x

lantern> scan
Starting device scan (type 'stopscan' to stop)...
----- Devices on Network -----
Name         IP Address      Status
-----------------------------------
YourName     192.168.1.x     Active
OtherDevice  192.168.1.y     Active

(Type commands below. Use 'stopscan' to stop scanning.)

lantern> rename
Enter your display name: NewName
Restarting mDNS with new display name...
[+] Registering mDNS service as 'NewName._lantern._tcp.local.' pointing to 192.168.1.x

lantern> stopscan
Stopping device scan...

lantern> exit
Exiting lantern CLI.
```

---

## ⚙️ Configuration

- The CLI stores your display name in a `config.json` file in the current directory.
- The display name is used for mDNS broadcasting and shown to other devices.
- You can update your display name anytime using the `rename` command in the CLI.

---

## 🛣️ Roadmap

- 💬 **Upcoming:**  
  LAN chat system for real-time messaging between detected devices.
- 🌐 **Future:**  
  - Cross-platform chat support  
  - File sharing  
  - Security improvements

---

## 🤝 Contributing

Contributions and suggestions are welcome! Please open an issue or submit a pull request.

---

**Note:**  
Currently, lantern only discovers and displays devices running lantern with mDNS enabled. Chat and other features are under development.

---