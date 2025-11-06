# 🦅 Malqart Clickjacker Module

> Crafted for security researchers, pentesters, and CTF players who value both function and form.
> **An `msfconsole`-style interactive Clickjacking Proof-of-Concept (PoC) generator**  
> Built for red teams, pentesters, and bug bounty hunters who demand control, speed, and style.

<img width="1280" height="709" alt="image" src="https://github.com/user-attachments/assets/17a8b11d-60a4-4ebb-a06c-ecd20448df93" />

*Example output: Multiple targets tested in a single, elegant interface*
---

## 🔥 Features

- **Interactive Malqart Console**: Unified UX with `Malqart_shell_module.py` (`use`, `set`, `run`, `show`)
- **Multi-Target Support**: Test **multiple vulnerable URLs** in a single PoC
- **Auto Web Server**: Serves your PoC instantly on `localhost` with zero config
- **Auto Browser Launch**: Opens PoC in your default browser (toggleable)
- **Night-Sky Theme**: Visually distinct, professional UI with dark cosmic styling
- **Input Sanitization**: Automatically prepends `https://` to raw domains
- **Zero Dependencies**: Pure Python 3 (uses only standard library)

---

## 🚀 Quick Start

### Run Directly
```bash
wget https://your-repo/Malqart_clickjacker.py -O malqart-clickjacker.py
chmod +x malqart-clickjacker.py
./malqart-clickjacker.py
```

### Example Workflow
```text
MalqartClickjacker > set TARGETS admin.vuln.com,https://app.target.com
[*] TARGETS => admin.vuln.com, https://app.target.com

MalqartClickjacker > set OUTPUT clickjacking_attack.html
[*] OUTPUT => clickjacking_attack.html

MalqartClickjacker > set AUTOLAUNCH true
[*] AUTOLAUNCH => true

MalqartClickjacker > run
[+] Clickjacking PoC saved: /home/user/clickjacking_attack.html
[i] Serving PoC at: http://localhost:8003/clickjacking_attack.html
[i] Press Ctrl+C to stop the server.
```

> ✅ Your browser opens automatically with a **multi-iframe PoC**—each iframe embedding a target site. If the target lacks `X-Frame-Options` or `Content-Security-Policy: frame-ancestors`, it’s **vulnerable to clickjacking**.

---

## 🧰 Commands Reference

| Command | Description |
|--------|-------------|
| `set TARGETS url1,url2,...` | Comma-separated target URLs (auto-sanitized) |
| `set OUTPUT file.html` | Output filename (`.html` appended if missing) |
| `set AUTOLAUNCH true/false` | Auto-open browser after generation |
| `set PORT 8080` | Force server to use specific port |
| `show options` | Display current configuration |
| `run` or `exploit` | Generate PoC + start local server |
| `exit` / `quit` | Exit console |

> 💡 Input like `example.com, https://admin.local` becomes `https://example.com, https://admin.local`

---

## 🎨 PoC Design Philosophy

- **Professional Aesthetic**: Deep navy (`#0b0c2a`) background with icy text (`#e0f7ff`)
- **Clear Target Labeling**: Each iframe shows its URL and index
- **Security Warning Banner**: Educates testers on impact
- **Responsive Iframes**: 95% width, 400px height — ideal for desktop testing

---

## ⚠️ Legal & Ethical Use

> **This tool is for authorized security assessments only.**

✅ **DO**:
- Test only systems you own or have explicit written permission to assess
- Use during penetration tests, bug bounty programs, or internal red team ops
- Report findings responsibly

❌ **DON’T**:
- Target external systems without authorization
- Use for phishing, social engineering, or malicious framing
- Deploy in production without consent

> **You are solely responsible for your actions. The author assumes no liability.**

---

## 📦 Requirements

- **Python 3.6+**
- Standard library only (`http.server`, `socket`, `threading`, etc.)
- Optional: `webbrowser` support (enabled by default; fails gracefully if missing)

---

## 🌐 Inspired By

- **Metasploit Framework** – For its legendary console-driven workflow  
- **Modern Clickjacking Research** – From OWASP to real-world bug bounty writeups

---

## 🧩 Part of the Malqart Framework

Malqart Clickjacker is designed to work **alongside** `Malqart_shell_module.py` as part of a unified offensive toolkit:

| Module | Purpose |
|-------|--------|
| `Malqart_shell_module.py` | Reverse shell generation & obfuscation |
| `Malqart_clickjacker.py` | Clickjacking PoC & server automation |

Future versions may integrate both into a **single Malqart console** with `use shell` / `use clickjacker` workflows.

---

## 📬 Feedback & Contributions

Found a bug? Want decoy buttons or lure overlays?

- ✨ **Star** the repo if you find it useful  
- 🐞 Open an **Issue** for bugs or feature requests  
- 🛠️ Submit a **Pull Request** for new templates or bypasses

---

## Author
Oussama Ben Hadj Dahman @cybereagle2001

> **Made with ❤️ for the offensive security community.**  
> **Malqart — Where deception meets precision.**
