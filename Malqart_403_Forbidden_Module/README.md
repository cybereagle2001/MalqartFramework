# 🛠️ Malqart 403 Bypasser Module

> **An `msfconsole`-style 403 Forbidden bypass tester**  
> Inspired by **ShellForge’s evasion philosophy** and real-world bug bounty techniques.  

Test **40+ bypass methods** against protected paths (`/admin`, `/backup`, `/debug`) in seconds—with categorized payloads, parallel execution, and success highlighting.

---

## 🔥 Features

- **40+ Real-World Bypass Techniques**  
  Includes all tricks from your curl payload list:
  - Path normalization: `/%2e/`, `..;/`, `?`, `#`, `/*`
  - HTTP verb abuse: `POST`, `TRACE`, `PUT`, `DEBUG`
  - Header injection: `X-Original-URL`, `X-Rewrite-URL`, `X-Forwarded-For`, `X-Host`
  - Encoding tricks: URL encode, double encode, mixed case
- **Categorized Payloads**  
  Grouped into: **Path Manipulation**, **HTTP Methods**, **Header Injection**, **Encoding**
- **Malqart-Style Interactive Console**  
  Uniform UX with `Malqart_shell_module.py` and `Malqart_clickjacker.py`
  ```text
  Malqart403 > set URL https://target.com/admin
  Malqart403 > run
  ```
- **Smart Output**  
  - 🟢 **Green**: `200/201/204` → **Confirmed Success**  
  - 🟡 **Yellow**: `301/302/401` → **Worth Investigating**  
  - ❌ **Hidden**: `403/404` by default (use `VERBOSE true` to see all)
- **Results Export**  
  Save working bypasses to `malqart_403_bypass_results.txt`
- **Zero External Dependencies**  
  Only requires `requests` (preinstalled in Kali, Parrot, etc.)

---

## 🚀 Quick Start

### Install Dependencies (if needed)
```bash
pip3 install requests
```

### Run the Module
```bash
wget https://your-repo/Malqart_403_bypasser.py -O malqart-403.py
chmod +x malqart-403.py
./malqart-403.py
```

### Example Workflow
```text
Malqart403 > set URL https://shop.target.com/internal-api
[*] URL => https://shop.target.com/internal-api

Malqart403 > set VERBOSE false
Malqart403 > set SAVE_OUTPUT true

Malqart403 > run
[✅ SUCCESS] Path: /internal-api..;/    | GET  | https://shop.target.com/internal-api..;/ → 200
[⚠️  INTERESTING] Header: X-Original-URL | GET  | https://shop.target.com/internal-api → 302

[+] Results saved to: malqart_403_bypass_results.txt
```

---

## 🧰 Commands Reference

| Command | Description |
|--------|-------------|
| `set URL <https://target.com/path>` | Target endpoint (required) |
| `set THREADS <num>` | Concurrent requests (default: 15) |
| `set TIMEOUT <sec>` | Per-request timeout (default: 8) |
| `set FOLLOW_REDIRECT <true/false>` | Follow 3xx redirects |
| `set VERBOSE <true/false>` | Show all attempts (including 403/404) |
| `set SAVE_OUTPUT <true/false>` | Save non-403 results to file |
| `set OUTPUT_FILE <file.txt>` | Custom output filename |
| `show options` | Display current config |
| `run` / `exploit` | Launch bypass tests |
| `exit` | Quit console |

---

## 📊 Payload Coverage (Inspired by ShellForge & Real Bug Bounties)

| Category | Techniques |
|--------|-----------|
| **Path Manipulation** | `/%2e/`, `..;/`, `;`, `?`, `#`, `/*`, `.html`, `.php`, trailing `/`, double slash |
| **HTTP Methods** | `POST`, `PUT`, `TRACE`, `OPTIONS`, `DEBUG`, `PATCH` (+ `Content-Length: 0`) |
| **Header Injection** | `X-Original-URL`, `X-Rewrite-URL`, `X-Forwarded-For`, `X-Host`, `X-Forwarded-Host`, `Referer` |
| **Encoding & Case** | URL encode, double URL encode, uppercase, lowercase, mixed case |

> ✅ All payloads from your curl script are implemented and expanded.

---

## ⚠️ Legal & Ethical Use

> **For authorized penetration testing only.**

✅ **DO**:
- Test only systems you **own** or have **written permission** to assess  
- Use during **bug bounty** programs within defined scope  
- Respect `robots.txt`, rate limits, and WAF rules  

❌ **DON’T**:
- Target external assets without explicit consent  
- Use in production without approval  
- Ignore legal boundaries  

> **You are solely responsible for your actions. The author assumes no liability.**

---

## 📦 Requirements

- **Python 3.6+**
- **`requests`** library (install via `pip3 install requests` if not present)

---

## 🌐 Part of the Malqart Offensive Framework

| Module | Purpose |
|-------|--------|
| `Malqart_shell_module.py` | Reverse shell generation (6+ formats, 5 obfuscation methods) |
| `Malqart_clickjacker.py` | Multi-target clickjacking PoC generator |
| `Malqart_403_bypasser.py` | 403/401/forbidden path bypass tester |

> Future vision: Unified `malqart` console with `use shell`, `use clickjacker`, `use 403bypasser`.

---

## 💡 Inspired By

- **Assetnote & PentesterLab wordlists** – Real-world 403 bypass patterns  
- **Metasploit Framework** – Console-driven, module-based UX

---

## 📬 Feedback & Contributions

Love it? Found a missing bypass?
- ⭐ **Star the repo**  
- 🐞 **Open an issue** for bugs or new techniques  
- 🛠️ **Submit a PR** to add headers, paths, or WAF fingerprints

---

## Author
Oussama Ben Hadj Dahaman @cybereagle2001

> **Made with ❤️ for red teams, pentesters, and bug bounty hunters.**  
> **Malqart — Where access denied is just the beginning.**
