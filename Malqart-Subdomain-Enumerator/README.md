# 🔍 Malqart Subdomain Enumerator

> **An `msfconsole`-style subdomain enumeration module for the Malqart offensive framework**  
> Fast, modular, and designed to integrate seamlessly with **SecLists** for maximum effectiveness.

This module combines **wordlist-based enumeration** and **Certificate Transparency (CT) log queries** to discover subdomains associated with a target domain. It follows the **`msfconsole`-style UX** of other Malqart modules, making it intuitive for users familiar with the framework.

Perfect for **penetration testers**, **bug bounty hunters**, and **security researchers** who need a fast and reliable subdomain discovery tool that fits into their existing Malqart workflow.

---

## 🔥 Features

- **Malqart-Style Interactive Console**  
  Unified UX with other Malqart modules:
  ```text
  MalqartSubEnum > set TARGET_DOMAIN example.com
  MalqartSubEnum > set WORDLIST MalqartDatabase/Discovery/Subdomains/subdomains-top1million-5000.txt
  MalqartSubEnum > run
  ```

- **Fast Wordlist-Based Enumeration**  
  Multi-threaded DNS resolution against a provided wordlist for quick discovery.

- **Certificate Transparency (CT) Log Integration**  
  Optional querying of `crt.sh` to find subdomains registered in public TLS certificates (requires `requests` library).

- **Integrated SecLists Support**  
  Automatically looks for common SecLists subdomain wordlists in the `MalqartDatabase/Discovery/Subdomains/` directory. Provides helpful hints if the specified wordlist is not found.

- **Configurable Options**  
  Adjust `THREADS`, `TIMEOUT`, `OUTPUT_FILE`, and verbosity for different scenarios.

- **Clear Output & Reporting**  
  Displays found subdomains in real-time and saves unique results to a specified output file.

- **Minimal Dependencies**  
  Uses Python standard library (`socket`, `concurrent.futures`, `pathlib`) for core functionality. `requests` is optional for CT log queries.

---

## 🚀 Quick Start

### 1. Integrate SecLists (Recommended)

To get the most out of this module, set up the `MalqartDatabase` directory with SecLists:

```bash
# In your main Malqart directory
mkdir -p MalqartDatabase/Discovery/Subdomains

# Download or link your SecLists subdomain wordlists into the above directory
# Example: cp /path/to/subdomains-top1million-5000.txt MalqartDatabase/Discovery/Subdomains/
```

### 2. Install Dependency (Optional, for CT Logs)

To enable Certificate Transparency log queries:

```bash
pip3 install requests
```

### 3. Run the Module

```bash
# Make sure you have Python 3 installed
wget https://your-repo/Malqart_subdomain_enum.py -O malqart-subenum.py
chmod +x malqart-subenum.py
./malqart-subenum.py
```

### 4. Example Workflow

```text
MalqartSubEnum > set TARGET_DOMAIN target.com
[*] TARGET_DOMAIN => target.com

MalqartSubEnum > set WORDLIST MalqartDatabase/Discovery/Subdomains/subdomains-top1million-5000.txt
[*] WORDLIST => MalqartDatabase/Discovery/Subdomains/subdomains-top1million-5000.txt

MalqartSubEnum > set INCLUDE_CT_LOGS true
[*] INCLUDE_CT_LOGS => true

MalqartSubEnum > run
[*] Loading wordlist: /path/to/MalqartDatabase/Discovery/Subdomains/subdomains-top1million-5000.txt
[*] Loaded 499999 unique subdomains from wordlist.
[*] Enumerating subdomains for: target.com
  [+] www.target.com
  [+] mail.target.com
  [+] dev.target.com
[*] Querying Certificate Transparency logs for: target.com
  [+] Found 2 unique subdomains via CT logs.
  [+] api.target.com
  [+] staging.target.com

[*] Total unique subdomains found: 4
[*] Results saved to: malqart_subdomains.txt

MalqartSubEnum > exit
```

---

## 🧰 Commands Reference

| Command | Description |
|--------|-------------|
| `set TARGET_DOMAIN <domain>` | Target domain to enumerate (e.g., `example.com`) (required) |
| `set WORDLIST </path/to/file>` | Path to subdomain wordlist (default: SecLists list if available, otherwise `subdomains.txt`) |
| `set THREADS <num>` | Number of concurrent DNS threads (default: 50) |
| `set TIMEOUT <sec>` | DNS query timeout per request (default: 3.0) |
| `set OUTPUT_FILE <file>` | File to save discovered subdomains (default: `malqart_subdomains.txt`) |
| `set INCLUDE_CT_LOGS <true/false>` | Query `crt.sh` for subdomains (requires `requests`) (default: `false`) |
| `set VERBOSE <true/false>` | Show failed attempts during wordlist scan (default: `false`) |
| `show options` | Display current configuration |
| `run` / `exploit` | Start the enumeration process |
| `exit` | Quit the console |

---

## 📦 Requirements

- **Python 3.6+**
- **`requests` library** (optional, for Certificate Transparency log queries) (`pip3 install requests`)

---

## ⚠️ Legal & Ethical Use

> **This module is for authorized security assessments only.**

✅ **DO**:
- Use only on **domains you own** or have **explicit written permission** to assess  
- Include discovered subdomains within the scope of your testing agreement  
- Respect rate limits, especially when querying `crt.sh`  

❌ **DON'T**:
- Enumerate domains without authorization  
- Use for malicious purposes or to cause disruption  
- Ignore legal boundaries or scope limitations  

> **You are solely responsible for your actions. The author assumes no liability.**

---

## 🔗 Part of the Malqart Offensive Framework

| Module | Purpose |
|-------|--------|
| `Malqart_shell_module.py` | Generate & obfuscate reverse shells (6+ formats, 5 obfuscation methods) |
| `Malqart_clickjacker.py` | Multi-target clickjacking PoC generator |
| `Malqart_403_bypasser.py` | Bypass 403/401 protected paths (40+ techniques) |
| `Malqart_cvss.py` | Score vulnerabilities with NIST-grade accuracy |
| `Malqart_nvdscanner.py` | Live CVE lookup from NVD based on service banners |
| `Malqart_android_exporter.py` | Extract databases from local Android data directories |
| **`Malqart_subdomain_enum.py`** | **Enumerate subdomains via wordlist & CT logs** |

---

## 🌐 Thanks to
- **[SecLists](https://github.com/danielmiessler/SecLists)** – For providing the **essential wordlists** that power this module's effectiveness
---

## 📬 Feedback & Contributions

Found a more efficient DNS resolution method? Want to add support for other CT log providers?

- ⭐ **Star the repo**  
- 🐞 **Open an issue** for bugs or feature requests  
- 🛠️ **Submit a PR** to enhance enumeration techniques or output formats
---

## Author 
Oussama Ben Hadj Dahman @cybereagle2001

> **Made with ❤️ for the offensive security community.**  
> **Malqart — Where reconnaissance meets precision.**
