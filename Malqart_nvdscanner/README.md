# 🔍 Malqart NVD Scanner

> **An `msfconsole`-style live CVE scanner for the Malqart offensive framework**  
> Port scan → Banner grab → CPE match → **Live NVD lookup** for known vulnerabilities.

This module brings **real-time, up-to-date vulnerability intelligence** from the **NVD (NIST)** directly into your Malqart workflow, combining the **speed and simplicity** of `TNSCANNER` with the **live data** of modern vulnerability research.

Perfect for **penetration testers**, **bug bounty hunters**, and **security consultants** who need to quickly identify potential attack vectors based on live CVE data.

---

## 🔥 Features

- **Fast Port Scanning**  
  Multi-threaded scan of common ports (configurable) for quick reconnaissance.
- **Service Banner Grabbing**  
  Identifies service versions (e.g., `Apache httpd 2.4.49`, `OpenSSH_7.2`) from open ports.
- **CPE Generation**  
  Transforms service banners into standardized **Common Platform Enumerations (CPE)** for precise vulnerability matching.
- **Live NVD CVE Lookup**  
  Queries the official **NVD API v2.0** in real-time to fetch relevant CVEs, CVSS scores, and severity levels for identified services.
- **Malqart-Style Interactive Console**  
  Unified UX with other Malqart modules:
  ```text
  MalqartNVD > set TARGET 192.168.1.100
  MalqartNVD > run
  ```
- **Caching**  
  Avoids duplicate NVD API calls for the same service within a single session.
- **NVD API Key Support**  
  Optional but **highly recommended** for higher rate limits (free to obtain).
- **Minimal Dependencies**  
  Uses Python standard library + `requests` (common in pentest distros).

---

## 🚀 Quick Start

### 1. Install Dependency
```bash
# Install requests (if not already present from other Malqart modules)
pip3 install requests
```

### 2. Get a Free NVD API Key (Recommended)
- Visit: https://nvd.nist.gov/developers/request-an-api-key
- Register (free).
- Obtain your API key (e.g., `12345678-1234-1234-1234-123456789012`).
- This increases your rate limit from **5 req/30s** to **50 req/30s**.

### 3. Run the Scanner
```bash
# Download the script
wget https://your-repo/Malqart_nvdscanner.py -O malqart-nvd.py
chmod +x malqart-nvd.py
./malqart-nvd.py
```

### 4. Example Workflow
```text
MalqartNVD > set TARGET 192.168.1.100
[*] TARGET => 192.168.1.100

MalqartNVD > set NVD_API_KEY your-api-key-here
[*] NVD_API_KEY => Set

MalqartNVD > run
[*] Scanning 192.168.1.100 on 24 ports...

[+] Open ports on 192.168.1.100:
  22/tcp open
    Banner: SSH-2.0-OpenSSH_7.2p2 Ubuntu-4ubuntu2.8
    CPE: cpe:2.3:a:openssh:openssh:7.2:*:*:*:*:*:*:*
      [NVD] Querying cpe:2.3:a:openssh:openssh:7.2:*:*:*:*:*:*:*...
      🚨 CVE-2016-6210 | CVSS: 5.5 (Medium)
         A vulnerability in sshd in OpenSSH before 6.9 allows remote...
  80/tcp open
    Banner: Apache/2.4.18 (Ubuntu)
    CPE: cpe:2.3:a:apache:http_server:2.4.18:*:*:*:*:*:*:*
      [NVD] Querying cpe:2.3:a:apache:http_server:2.4.18:*:*:*:*:*:*:*...
      🚨 CVE-2018-1312 | CVSS: 9.8 (Critical)
         The Apache HTTP Server before 2.4.34 allows a remote...

[*] Scan completed. 2 potential vulnerability(ies) found via NVD.
```

---

## 🧰 Commands Reference

| Command | Description |
|--------|-------------|
| `set TARGET <ip>` | Target IP address or hostname (required) |
| `set NVD_API_KEY <key>` | Optional NVD API key (get from nvd.nist.gov) |
| `set THREADS <num>` | Number of concurrent scan threads (default: 100) |
| `set TIMEOUT <sec>` | Timeout for each port connection (default: 1.0) |
| `set VERBOSE <true/false>` | Show NVD query status (default: false) |
| `show options` | Display current configuration |
| `run` / `exploit` | Start the port scan and CVE lookup |
| `exit` | Quit the console |

---

## 📦 Requirements

- **Python 3.6+**
- **`requests` library** (`pip3 install requests`)
- **Internet access** (for NVD API calls)

---

## ⚠️ Legal & Ethical Use

> **For authorized security assessments only.**

✅ **DO**:
- Test only systems you **own** or have **explicit written permission** to assess  
- Use during **bug bounty** programs within defined scope  
- Respect rate limits and NVD API usage guidelines  

❌ **DON’T**:
- Target external assets without consent  
- Ignore legal boundaries or scope  
- Use for malicious purposes  

> **You are solely responsible for your actions. The author assumes no liability.**

---

## 🔗 Part of the Malqart Offensive Framework

| Module | Purpose |
|-------|--------|
| `Malqart_shell_module.py` | Generate & obfuscate reverse shells (6+ formats, 5 obfuscation methods) |
| `Malqart_clickjacker.py` | Multi-target clickjacking PoC generator |
| `Malqart_403_bypasser.py` | Bypass 403/401 protected paths (40+ techniques) |
| `Malqart_cvss.py` | Score vulnerabilities with NIST-grade accuracy |
| **`Malqart_nvdscanner.py`** | **Live CVE lookup from NVD based on service banners** |

---

## 🌐 Inspired By

- **[TNSCANNER](https://github.com/cybereagle2001/TNSCANNER)** – For its **fast, beginner-friendly port scanning** and vulnerability identification concept  
- **[NVD (NIST)](https://nvd.nist.gov/)** – For providing the **official, up-to-date vulnerability database**
---

## 📬 Feedback & Contributions

Found a missing CPE mapping? Want more scan options?

- ⭐ **Star the repo**  
- 🐞 **Open an issue** for bugs or new CPE rules  
- 🛠️ **Submit a PR** to enhance banner parsing or output formats
---
## Author
Oussama Ben Hadj Dahman @cybereagle2001
> **Made with ❤️ for the offensive security community.**  
> **Malqart — Where speed meets precision.**
