#!/usr/bin/env python3
# MalqartFramework/malqart.py
import subprocess
import sys
import os
from pathlib import Path

# Define module mappings: name -> relative path to the main script within its repo
MODULES = {
    "shell": "Malqart_shell_module/Malqart_shell_module.py",
    "clickjacker": "Malqart-Clickjacker-Module/Malqart_clickjacker.py",
    "403_bypasser": "Malqart_403_Forbidden_Module/Malqart_403_bypasser.py",
    "cvss": "Malqart_CVSS_Module/Malqart_cvss.py",
    "nvdscanner": "Malqart_nvdscanner/Malqart_nvdscanner.py",
    "android_exporter": "Malqart-Android-Data-Exporter/Malqart_android_exporter.py",
    "subdomain_enum": "Malqart-Subdomain-Enumerator/Malqart_subdomain_enum.py",
    "url_enumeration" : "Malqart_URI_ENUM_Module/Malqart_uri_enum.py",
    # Add more mappings as you create new modules in their own repos
    "bruteforcer" : "Malqart_Bruteforcer_Module/Malqart_bruteforcer.py"
}

def main():
    print("Malqart Framework v2.0 — Unified Offensive Toolkit (Git-Based)")
    print("Inspired by ShellForge, msfconsole and TNSCANNER.")
    print("Modules are loaded from separate Git repositories.")
    print("""
MMMMMMMMMMMMMMMMMMMMMMMMMMMMOOOOWMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMMMMMMMN'    'NMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMMMMMMMX  cdddNMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMMMMMMMX  0Mk0MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMMMMMMMX  0Mx0MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM by cybereagle2001 MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMMMMMMMX  0M0,0MMMMMMMMMMMMMWMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMMMMMMMX  0MK  'ok0NNNNNNXk;lXWMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMWx,...'dWMMMMMMMMMMWKoo0X  lMN.                ....,;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;cllxx0KXMMMMMMMMMMMM
MMo cNWWd ;d..........   oX   NMocccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccllxOXWMMMM
MM, xMMMX..o             dX   XMXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX0Od:cxWMMM
MMX:.,:;..OXOOOOOOOOOko:;kX  ,MW.                                                                     ..,;:coxO0NMMMMMMM
MMMMNOOOXMMMMMMMMMMMMMMMMMX  kMW  .;oxOKKKKOxc..ldOO0NNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMMMMMMMX  kMW.dWMMMMMMMMMMMNXMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMMMMMMMX  kMOkMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMMMMMMMX  kMx0MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMMMMMMMX  o0kkWMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMMMMMMMX.    .XMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMMMMMMMMNddddNMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMMMMXXXWMMMNXXXMMWXXXXXXXXMMNXXXMMMMMMMMNXXXXXXXXWMWXXXXXXXXXMWXXXXXXXXXMMNXXXXXXXXXMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMMMM.  'KMk.  'MX.        MMl  .MMMMMMMc         XMx        .Mx         KM,        .MMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMMMM.   .;    'M0  .xxx   MMl  .MMMMMMM.  ;xxo   XMx  'xxc  .Mx   ddd   KMkdd,  'ddxMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMMMM.  '  .'  'M0  'MMM   MMl  .MMMMMMM.  oMMX   XMx  :MMO  .Mx   0KK   KMMMMl  :MMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMMMM.  0O;Kd  'M0  .'''   MMl  .MMMMMMM.  oMMX   XMx  .,,.  .Mx       .oWMMMMl  :MMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMMMM.  0MMMd  'M0  .ccc   MMl  .MMMMMMM.  oMMX   XMx  .cc;  .Mx   dx'  ,NMMMMl  :MMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMMMM.  0MMMd  'M0  'MMM   MMl  .xxxxxXM.  ;l..   XMx  :MMO  .Mx   WMM   0MMMMl  :MMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMMMM.  0MMMd  'M0  'MMM   MMl        xMc        ,NMx  :MMO  .Mx   WMM   0MMMMl  :MMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMMMMKKKWMMMNKKXMWKKKMMMKKKMMNKKKKKKKKNMMXKKo. .0MMMNKKXMMWKKKMNKKKMMMKKKWMMMMNKKXMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMWKNMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
    """)
    print("Type 'help' for commands or 'use <module>' to launch a module.\n")

    while True:
        try:
            cmd_input = input("malqart > ").strip()
            if not cmd_input:
                continue

            parts = cmd_input.split()
            command = parts[0].lower()

            if command in ["exit", "quit"]:
                print("[*] Shutting down Malqart Framework.")
                break

            elif command == "help":
                print("""
Available Commands:
    help                                    -> Show this help
    list_modules                            -> List available modules
    use <module_name>                       -> Launch a specific module
    update_modules                          -> Pull latest changes from module repos (if git present)
    exit / quit                             -> Exit the framework

Available Modules:
    shell          -> Generate reverse shells (PHP, Python, etc.)
    clickjacker    -> Multi-target clickjacking PoC generator
    403_bypasser   -> Bypass 403/401 forbidden paths
    cvss           -> Calculate CVSS v3.1/v4.0 scores
    nvdscanner     -> Live CVE lookup from NVD based on banners
    android_exporter -> Export databases from Android data directories
    subdomain_enum -> Enumerate subdomains via wordlist/CT logs
    URL_Enumeration -> Enumerate URL on a website (similar to dirb / gobuster)
    bruteforcer    -> Brute Force Attack on protocol / web page
                """)

            elif command == "list_modules":
                print("\nAvailable Modules:")
                for name in sorted(MODULES.keys()):
                    print(f"  - {name}")
                print("")

            elif command == "update_modules":
                print("[*] Updating module repositories...")
                base_path = Path(__file__).parent
                for module_name, script_path_str in MODULES.items():
                    repo_dir = base_path / script_path_str
                    # Navigate to the parent directory of the script (the repo root)
                    repo_root = repo_dir.parent
                    if repo_root.is_dir():
                        print(f"  Updating {module_name} ({repo_root})...")
                        try:
                            # Run 'git pull' in the repository directory
                            result = subprocess.run(
                                ["git", "pull"],
                                cwd=repo_root,
                                capture_output=True,
                                text=True,
                                timeout=30 # Add a timeout to prevent hanging
                            )
                            if result.returncode == 0:
                                print(f"    [+] Updated {module_name}")
                                if result.stdout.strip():
                                    print(f"         Output: {result.stdout.strip()}")
                            else:
                                print(f"    [-] Failed to update {module_name}: {result.stderr.strip()}")
                        except subprocess.TimeoutExpired:
                            print(f"    [-] Timeout updating {module_name}")
                        except Exception as e:
                            print(f"    [-] Error updating {module_name}: {e}")
                    else:
                        print(f"    [-] Repository directory for {module_name} not found: {repo_root}")
                print("[*] Update process completed.")

            elif command == "use":
                if len(parts) < 2:
                    print("[-] Usage: use <module_name>")
                    continue

                module_name = parts[1].lower()
                if module_name in MODULES:
                    script_rel_path = MODULES[module_name]
                    script_path = Path(__file__).parent / script_rel_path

                    if script_path.is_file():
                        print(f"[*] Launching {script_rel_path}...")
                        # Launch the selected module script as a subprocess
                        try:
                            # Change working directory to the module's repo root for relative path consistency
                            module_repo_root = script_path.parent
                            subprocess.run([sys.executable, str(script_path.name)], cwd=module_repo_root, check=True)
                        except subprocess.CalledProcessError as e:
                            print(f"[-] Module {script_rel_path} exited with code {e.returncode}")
                        except KeyboardInterrupt:
                            print(f"\n[!] Module {script_rel_path} interrupted.")
                    else:
                        print(f"[-] Module script '{script_rel_path}' not found in framework directory.")
                else:
                    print(f"[-] Module '{module_name}' not found. Use 'list_modules' to see available ones.")

            else:
                print(f"[-] Unknown command: {command}. Type 'help'.")

        except KeyboardInterrupt:
            print("\n[*] Use 'exit' to quit.")
        except EOFError:
            print("\n[*] Exiting.")
            break

if __name__ == "__main__":
    main()
