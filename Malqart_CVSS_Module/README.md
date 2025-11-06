# 🧮 Malqart CVSS Calculator

> **An `msfconsole`-style, offline CVSS scoring module for the Malqart offensive framework**  
> Build, validate, and score **CVSS v3.1** and **v4.0** vectors instantly — no internet, no guesswork.

Perfect for **penetration testers**, **bug bounty hunters**, **CTF players**, and **ISO/IEC 27001-compliant security consultants** who need **accurate, report-ready risk scores** during engagements.

---

## 🔥 Features

- **Malqart-Style Console UX**  
  Unified interface with `Malqart_shell_module.py`, `Malqart_clickjacker.py`, and `Malqart_403_bypasser.py`:
  ```text
  MalqartCVSS > set VERSION 3.1
  MalqartCVSS > set MODE paste
  MalqartCVSS > set VECTOR AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H
  MalqartCVSS > run
  ```

- **Dual Input Modes**  
  - **`paste`**: Enter raw or full vectors (auto-prefixes `CVSS:3.1/` if missing)  
  - **`interactive`**: Guided, step-by-step metric selection (CTF-friendly)

- **Full CVSS Support**  
  - ✅ **CVSS v3.1**  
  - ✅ **CVSS v4.0**

- **Auto-Prefix Handling**  
  Works with **both**:
  - `AV:N/AC:L/...` → auto becomes `CVSS:3.1/AV:N/AC:L/...`  
  - `CVSS:3.1/AV:N/AC:L/...` → used as-is  
  → **No more “missing mandatory prefix” errors!**

- **Instant Severity Output**  
  Returns **numeric score** + **textual severity** (`Critical`, `High`, `Medium`, `Low`, `None`)

- **Offline & Lightweight**  
  Uses the official **`cvss` Python library** (same engine as NIST)

---

## 🚀 Quick Start

### Install Dependency
```bash
# One-time setup
pip3 install cvss
# OR on Kali/Debian:
sudo apt install python3-cvss
```

### Run the Module
```bash
wget https://your-repo/Malqart_cvss.py -O malqart-cvss.py
chmod +x malqart-cvss.py
./malqart-cvss.py
```

### Example: Paste Mode (Report Writing)
```text
MalqartCVSS > set VERSION 3.1
MalqartCVSS > set MODE paste
MalqartCVSS > set VECTOR AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H
MalqartCVSS > run

[+] Input vector: AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H
✅ CVSS 3.1 Base Score: 9.8
   Severity: Critical
```

### Example: Interactive Mode (CTF Triage)
```text
MalqartCVSS > set VERSION 4.0
MalqartCVSS > set MODE interactive
MalqartCVSS > run
--- Building CVSS v4.0 Vector ---
Attack Vector:
  [N] Network
  [A] Adjacent
  [L] Local
  [P] Physical
Select AV: N
...
✅ CVSS 4.0 Base Score: 8.6
   Severity: High
```

---

## 🧰 Commands Reference

| Command | Description |
|--------|-------------|
| `set VERSION <3.1\|4.0>` | CVSS version (strict — only `3.1` or `4.0`) |
| `set MODE <interactive\|paste>` | Input method |
| `set VECTOR <AV:N/...>` | Raw or full CVSS vector |
| `show options` | Display current configuration |
| `run` / `exploit` | Calculate and display score |
| `exit` | Quit console |

---

## 📦 Requirements

- **Python 3.6+**
- **`cvss` library** (`pip3 install cvss`)

> ⚠️ Unlike other Malqart modules, this one requires **one external dependency** — but it’s the **official CVSS calculator**, ensuring **100% score accuracy**.

---

## ⚠️ Legal & Ethical Use

> **For authorized security assessments only.**

✅ **DO**:  
- Use during **penetration tests**, **bug bounty programs**, or **internal audits**  
- Include scores in **ISO/IEC 27001-aligned risk reports**  
- Validate findings before disclosure  

❌ **DON’T**:  
- Use in malicious contexts  
- Misrepresent risk severity  
- Ignore organizational policies  

> **You are solely responsible for your actions. The author assumes no liability.**

---

## 🔗 Part of the Malqart Offensive Framework

| Module | Purpose |
|-------|--------|
| `Malqart_shell_module.py` | Generate & obfuscate reverse shells (6+ formats) |
| `Malqart_clickjacker.py` | Multi-target clickjacking PoC generator |
| `Malqart_403_bypasser.py` | Bypass 403/401 protected paths (40+ techniques) |
| **`Malqart_cvss.py`** | **Score vulnerabilities with NIST-grade accuracy** |

> 💡 **Pro Tip**: Chain modules!  
> Bypass 403 → Upload shell → Calculate CVSS score → Report with confidence.

---

## 🌐 Inspired By
- **[OFFLINE_CVSS_CALCULATOR](https://github.com/cybereagle2001/OFFLINE_CVSS_CALCULATOR)** – For its **practical, offline-first approach**  
- **Metasploit Framework** – For its **console-driven, module-based UX**

---

## 📬 Feedback & Contributions

Found a bug? Want **JSON/CSV export** or **temporal/environmental metrics**?

- ⭐ **Star the repo**  
- 🐞 **Open an issue**  
- 🛠️ **Submit a PR**
---

## Author 
Oussama Ben Hadj Dahman @cybereagle2001

> **Made with ❤️ for the offensive security community.**  
> **Malqart — Precision tools for modern red teams.**
