
# 🖧 lanShare

**lanShare** is a lightweight Python tool for discovering devices on your local network using mDNS (Multicast DNS). Devices running lanShare will broadcast their presence and basic system information, allowing you to see other active lanShare users on the same LAN.

---

## 🚀 Features

- 🌐 **mDNS Device Discovery:**  
  Broadcast your device and discover other lanShare-enabled devices on your local network using mDNS.
- 🏷️ **Custom Display Name:**  
  Set and update your display name, which is visible to others on the network.
- 🖥️ **System Metadata Sharing:**  
  Automatically shares your device hostname, OS, and version with other users.
- 🔄 **Real-Time Updates:**  
  Devices are shown as soon as they join or leave the network.
- ⚙️ **Easy Configuration:**  
  Stores your display name in a simple `config.json` file for persistence.
- ✅ **Cross-Platform Ready:**  
  Works on **Linux**, **Windows**, and **Mac** (Python 3.8+).  
  *(Note: Current development/testing is focused on a single platform.)*

---

## 🔧 Installation

### 1. Clone the repository

```bash
git clone https://github.com/Suryakiran46/lanShare.git
cd lanShare
```

### 2. (Optional) Create and activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🧪 Usage

### Register and broadcast your device

```bash
python mDNS.py
```
- On first run, you will be prompted to enter a display name.
- Your device will now be discoverable to other lanShare users on the LAN.

### Change your display name

```bash
python mDNS.py --rename
```
- Updates your display name and re-broadcasts your device.

---

## ⚙️ Configuration

- The application creates a `config.json` file to store your display name.
- You can update your name anytime using the `--rename` flag.

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
Currently, lanShare only discovers and displays devices running lanShare with mDNS enabled. Chat and other features are under development.
---
