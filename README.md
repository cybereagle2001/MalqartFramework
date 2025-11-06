# 🛡️ Malqart Framework

> **The Unified Offensive Toolkit for Modern Penetration Testing**  
> *Where reconnaissance meets precision, and evasion meets control.*  
> **Crafted for security researchers, pentesters, and CTF players who value both function and form.**
<img width="912" height="342" alt="image" src="https://github.com/user-attachments/assets/13018521-1fde-45be-ba81-84920d95d374" />

---

## 🚀 Overview

The **Malqart Framework** is a modular, `msfconsole`-style collection of offensive security tools designed for speed, accuracy, and seamless integration. Inspired by the philosophies of **ShellForge**, **RouterSploit**, and **TNSCANNER**, it brings together essential functionalities—from reverse shell generation to vulnerability scanning—under one cohesive, interactive console.

> **Named after Melqart**, the Phoenician god of the underworld and merchants—symbolizing the **duality** of modern offensive security: stealthy yet powerful, hidden yet functional.

---

## ✨ Features

- **Modular Architecture**: Independent tools (e.g., `shell`, `clickjacker`, `403_bypasser`) housed in dedicated Git repositories for easy maintenance and updates.
- **`msfconsole`-Style UX**: Unified interactive prompt (`malqart >`) with `use`, `set`, `run`, `show` commands across all modules.
- **Integrated SecLists & Libraries**: Centralized `MalqartDatabase` for wordlists and a `MalqartDatabase_config.py` for easy setup and access.
- **Extensible Design**: Easy to add new modules following the established patterns.
- **Git-Based Management**: Core launcher (`malqart.py`) orchestrates updates for individual module repositories.

---

## 📦 Modules

| Module | Purpose | Key Features |
|--------|---------|--------------|
| `Malqart_shell_module` | Reverse Shell Generation | 6+ formats (PHP, PNG, PY, SH), 5 obfuscation methods, 5 bypass techniques |
| `Malqart_clickjacker` | Clickjacking PoC Generator | Multi-target, polyglot files, auto-server & browser launch |
| `Malqart_403_bypasser` | 403/401 Path Bypass | 40+ real-world techniques (headers, paths, verbs), parallel execution |
| `Malqart_cvss` | CVSS Scoring | v3.1/v4.0, interactive/paste mode, auto-prefix handling |
| `Malqart_nvdscanner` | Live CVE Scanner | Port scan → Banner → CPE → NVD API lookup |
| `Malqart_subdomain_enum` | Subdomain Enumeration | Wordlist & CT logs (`crt.sh`), SecLists integration |
| `Malqart_android_exporter` | Android Data Extractor | Export databases from local data directory structures |

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.6+**
- **Git**
- **Netcat** (`nc`) for shell listeners

### Installation

1.  **Clone the Framework:**
    ```bash
    git clone https://github.com/cybereagle2001/MalqartFramework.git
    cd MalqartFramework
    ```

2.  **Install Dependencies & Download SecLists:**
    ```bash
    # Run the integrated setup (from MalqartFramework directory)
    python3 MalqartDatabase_config.py
    # Then uncomment the setup lines in the script and run again:
    # if __name__ == "__main__":
    #     setup_framework()
    ```
    Or follow the specific instructions in each module's README for dependencies (e.g., `pip3 install requests cvss`).

3.  **Launch the Framework:**
    ```bash
    chmod +x malqart.py
    ./malqart.py
    # Or
    python3 malqart.py
    ```

### Example Workflow

```text
malqart > use subdomain_enum
[*] Launching Malqart-Subdomain-Enumerator/Malqart_subdomain_enum.py...
MalqartSubEnum > set TARGET_DOMAIN target.com
MalqartSubEnum > run
...

MalqartSubEnum > back
malqart > use 403_bypasser
[*] Launching Malqart_403_Forbidden_Module/Malqart_403_bypasser.py...
Malqart403 > set URL https://target.com/internal-api
Malqart403 > run
...

Malqart403 > back
malqart > use shell
[*] Launching Malqart_shell_module/Malqart_shell_module.py...
MalqartShell > use php
MalqartShell > set IP 192.168.1.10
MalqartShell > set PORT 4444
MalqartShell > run
[+] Payload saved as: shell.php
MalqartShell > exit

malqart > exit
```

---

## 🧠 Philosophy

- **Speed & Accuracy**: Optimized for efficiency without sacrificing precision.
- **Modularity**: Each tool is a self-contained module, easy to update or replace.
- **Integration**: Tools are designed to work together, feeding output from one into the input of another.
- **`msfconsole` UX**: Familiar, interactive command-line interface for streamlined workflows.
- **ShellForge Inspiration**: Emphasis on payload generation, obfuscation, and bypass techniques.
- **TNSCANNER / RouterSploit Inspiration**: Focus on networked device and vulnerability identification.

---

## 📚 Commands Reference

| Command | Description |
|--------|-------------|
| `help` | Show available commands |
| `list_modules` | List all available modules |
| `use <module_name>` | Launch a specific module |
| `update_modules` | Pull latest changes from all module repositories |
| `setup` | Install required libraries and download SecLists starter pack |
| `exit` / `quit` | Exit the framework |

---

## 🛡️ Legal & Ethical Use

> **This framework is for authorized security assessments only.**

✅ **DO**:
- Use only on systems you **own** or have **explicit written permission** to assess
- Follow responsible disclosure practices
- Comply with all applicable laws and regulations
- Use for educational, research, or bug bounty purposes within scope

❌ **DON'T**:
- Deploy against systems without authorization
- Use for malicious or illegal activities
- Ignore legal boundaries or scope limitations
- Cause harm or disruption

> **You are solely responsible for your actions. The author assumes no liability.**

---

## 🤝 Contributing

Found a bug? Have an idea for a new module or enhancement?

- ⭐ **Star** the repo if you find it useful
- 🐞 Open an **Issue** for bugs or feature requests
- 🛠️ Submit a **Pull Request** for new modules or improvements

---
## Original Author
Oussama Ben Hadj Dahman @cybereagle2001

## 📜 License

This project is licensed under the MIT License - see the `LICENSE` file for details.

---

## 🙏 Acknowledgements

- **[ShellForge](https://github.com/Wael-Rd/ShellForge)** – For the gold standard in shell generation and evasion philosophy
- **[TNSCANNER](https://github.com/cybereagle2001/TNSCANNER)** – For the initial inspiration and beginner-friendly approach
- **[SecLists](https://github.com/danielmiessler/SecLists)** – For the essential wordlists
- **[Metasploit Framework](https://github.com/rapid7/metasploit-framework)** – For the legendary interactive console design
---

> **Made with ❤️ for the offensive security community by Oussama Ben Hadj Dahman (@cybereagle2001).**  
> **Malqart — Where deception meets precision. Where access denied is just the beginning.**
