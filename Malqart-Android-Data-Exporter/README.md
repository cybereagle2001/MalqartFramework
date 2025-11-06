# 📱 Malqart Android Data Exporter

> **An `msfconsole`-style module for extracting databases from Android application data directories**  
> Part of the **Malqart offensive framework**, inspired by the simplicity of **TNSCANNER** and the modular design of **ShellForge**.

This module simulates the core logic of an Android database extraction tool. It **recursively searches** a specified local directory (e.g., an `adb pull` output, a mounted system image, or an extracted backup) for common database file types (`.db`, `.sqlite`, etc.) and **exports them to a clean output directory**.

> ⚠️ **Important**: This script operates on **local filesystems only**. It does **not** connect to Android devices. You must first obtain the data directory using `adb` or other extraction methods.

---

## 🔥 Features

- **Malqart-Style Interactive Console**  
  Unified UX with other Malqart modules (`set`, `run`, `show options`):
  ```text
  MalqartAndroid > set SOURCE_DIR /path/to/android/data
  MalqartAndroid > set OUTPUT_DIR /home/user/extracted_dbs
  MalqartAndroid > run
  ```

- **Recursive Database Search**  
  Finds `.db`, `.sqlite`, `.sqlite3`, `.db3`, and other common database extensions within the source directory structure.

- **Configurable Output**  
  Specify the destination directory for extracted databases.

- **SQLite WAL/SHM Control**  
  Option to include or exclude SQLite Write-Ahead Log (`.wal`) and Shared Memory (`.shm`) files.

- **File Preservation**  
  Uses `shutil.copy2` to maintain original file metadata during export.

- **Clear Progress Feedback**  
  Shows which files are being copied and reports the total count upon completion.

- **No External Dependencies**  
  Built with Python standard library only (`os`, `shutil`, `pathlib`).

---

## 🚀 Quick Start

### 1. Prepare Android Data Directory

You need to have a local copy of the Android application's data directory. This is typically done using `adb` on a rooted device or an emulator:

```bash
# Example: Pull data for app 'com.example.app' (requires root or backup/restore)
adb root # (if device is rooted)
adb pull /data/data/com.example.app /path/to/local/android_backup/com.example.app

# Or, use 'adb backup' and then extract the backup file if root is not available
# This step is done outside of Malqart.
```

### 2. Run the Malqart Module

```bash
# Make sure you have Python 3 installed
wget https://your-repo/Malqart_android_exporter.py -O malqart-android-exporter.py
chmod +x malqart-android-exporter.py
./malqart-android-exporter.py
```

### 3. Example Workflow

```text
MalqartAndroid > set SOURCE_DIR /home/user/android_backups/com.example.app
[*] SOURCE_DIR => /home/user/android_backups/com.example.app

MalqartAndroid > set OUTPUT_DIR /home/user/malqart_exports/example_app_dbs
[*] OUTPUT_DIR => /home/user/malqart_exports/example_app_dbs

MalqartAndroid > set INCLUDE_WAL true
[*] INCLUDE_WAL => true

MalqartAndroid > run
[*] Searching for databases in: /home/user/android_backups/com.example.app
[*] Found 4 potential database file(s).
[*] Exporting to: /home/user/malqart_exports/example_app_dbs
  [+] Copied: databases/main.db
  [+] Copied: databases/main.db-wal
  [+] Copied: databases/cache.db
  [+] Copied: databases/user_data.sqlite

[*] Export completed. 4 database file(s) copied to '/home/user/malqart_exports/example_app_dbs'.
```

---

## 🧰 Commands Reference

| Command | Description |
|--------|-------------|
| `set SOURCE_DIR </path/to/android/data>` | Source Android data directory (e.g., from `adb pull`) (required) |
| `set OUTPUT_DIR </path/to/export>` | Destination directory for exported databases (default: `malqart_android_dbs`) |
| `set INCLUDE_WAL <true/false>` | Include SQLite WAL files (default: `false`) |
| `set INCLUDE_SHM <true/false>` | Include SQLite SHM files (default: `false`) |
| `show options` | Display current configuration |
| `run` / `exploit` | Start the export process |
| `exit` | Quit the console |

---

## 📦 Requirements

- **Python 3.6+**
- **Local access** to the Android data directory (e.g., via `adb pull`)

---

## ⚠️ Legal & Ethical Use

> **This module is for authorized analysis of data you own or have explicit permission to access.**

✅ **DO**:
- Use only on **devices or data you control** or have **explicit written permission** to analyze  
- Ensure compliance with **applicable laws and privacy regulations**  
- Use for **educational**, **research**, or **authorized penetration testing** purposes  

❌ **DON'T**:
- Use to access or extract data from devices without **authorization**  
- Violate computer crime laws or privacy policies  
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
| `Malqart_nvdscanner.py` | Live CVE lookup from NVD based on service banners |
| **`Malqart_android_exporter.py`** | **Extract databases from local Android data directories** |

---
## 📬 Feedback & Contributions

Found a common database extension missing from the search? Want to add more export options?

- ⭐ **Star the repo**  
- 🐞 **Open an issue** for bugs or feature requests  
- 🛠️ **Submit a PR** to enhance file detection or output formats
---
## Author 
Oussama Ben Hadj Dahman @cybereagle2001

> **Made with ❤️ for the offensive security community.**  
> **Malqart — Where precision meets automation.**
