#!/usr/bin/env python3
import os
import sys
import socket
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path # For robust path handling

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False
    print("[-] 'requests' not found. Certificate Transparency queries will be disabled.")
    print("    Install with: pip3 install requests")

# Default SecLists path relative to the script location
DEFAULT_SECLISTS_DIR = Path(__file__).parent / "MalqartDatabase" / "Discovery" / "Subdomains"

class SubdomainEnumeratorSession:
    def __init__(self):
        self.target_domain = None
        # Default to a common SecLists list if it exists, otherwise fallback
        default_list_path = DEFAULT_SECLISTS_DIR / "subdomains-top1million-5000.txt"
        if default_list_path.is_file():
            self.wordlist_path = str(default_list_path)
        else:
            self.wordlist_path = "subdomains.txt" # Fallback if SecLists not found
        self.threads = 50
        self.timeout = 3.0
        self.output_file = "malqart_subdomains.txt"
        self.include_ct_logs = False  # Requires 'requests'
        self.verbose = False

    def show_options(self):
        print("\nModule options:")
        print(f"  TARGET_DOMAIN    => {self.target_domain}")
        print(f"  WORDLIST         => {self.wordlist_path}")
        print(f"  THREADS          => {self.threads}")
        print(f"  TIMEOUT          => {self.timeout}")
        print(f"  OUTPUT_FILE      => {self.output_file}")
        print(f"  INCLUDE_CT_LOGS  => {self.include_ct_logs} (requires 'requests')")
        print(f"  VERBOSE          => {self.verbose}\n")

    def resolve_subdomain(self, subdomain):
        """Attempt to resolve a subdomain."""
        full_domain = f"{subdomain}.{self.target_domain}"
        try:
            socket.gethostbyname(full_domain)
            return full_domain
        except socket.gaierror:
            return None

    def enum_from_wordlist(self):
        """Enumerate subdomains using a wordlist."""
        wordlist_path_obj = Path(self.wordlist_path)

        if not wordlist_path_obj.is_file():
            print(f"[-] Wordlist file '{self.wordlist_path}' not found.")
            # Attempt to list common SecLists subdomain files as a hint
            if DEFAULT_SECLISTS_DIR.is_dir():
                print(f"[*] Hint: SecLists subdomain lists are available in '{DEFAULT_SECLISTS_DIR}'")
                print("    Common files include:")
                # List a few common ones to suggest
                common_lists = ["subdomains-top1million-5000.txt", "subdomains-10000.txt", "subdomains-1000.txt"]
                for cl in common_lists:
                    if (DEFAULT_SECLISTS_DIR / cl).is_file():
                        print(f"      - {cl}")
            return []

        print(f"[*] Loading wordlist: {wordlist_path_obj}")
        try:
            with open(wordlist_path_obj, "r", encoding="utf-8", errors="ignore") as f:
                # Use set to avoid duplicates if present in the list, then back to list
                subdomains = list(set(line.strip() for line in f if line.strip()))
        except Exception as e:
            print(f"[-] Error reading wordlist '{wordlist_path_obj}': {e}")
            return []

        print(f"[*] Loaded {len(subdomains)} unique subdomains from wordlist.")
        print(f"[*] Enumerating subdomains for: {self.target_domain}")

        found = []
        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            future_to_sub = {executor.submit(self.resolve_subdomain, sub): sub for sub in subdomains}
            for future in as_completed(future_to_sub):
                result = future.result()
                if result:
                    found.append(result)
                    print(f"  [+] {result}")
                elif self.verbose:
                    sub = future_to_sub[future]
                    print(f"  [-] {sub}.{self.target_domain}")

        return found

    def enum_from_ct_logs(self):
        """Enumerate subdomains using Certificate Transparency logs via crt.sh."""
        if not HAS_REQUESTS:
            print("[-] 'requests' library not available. Cannot query Certificate Transparency logs.")
            return []

        print(f"[*] Querying Certificate Transparency logs for: {self.target_domain}")
        try:
            # crt.sh API query
            url = f"https://crt.sh/?q=%25.{self.target_domain}&output=json"
            headers = {"User-Agent": "Malqart-Subdomain-Enum/1.0"}
            resp = requests.get(url, headers=headers, timeout=15)
            if resp.status_code != 200:
                print(f"[-] CT log query failed with status {resp.status_code}")
                return []

            import json
            data = json.loads(resp.text)
            subdomains = set()
            for entry in data:
                name = entry.get("name_value", "")
                if name and name.endswith(f".{self.target_domain}"):
                    # Handle multi-line entries (SANs)
                    for n in name.split("\n"):
                        n = n.strip()
                        if n.endswith(f".{self.target_domain}") and not n.startswith("*"):
                            subdomains.add(n)

            unique_found = list(subdomains)
            print(f"  [+] Found {len(unique_found)} unique subdomains via CT logs.")
            for sub in unique_found:
                print(f"  [+] {sub}")
            return unique_found

        except requests.exceptions.RequestException as e:
            print(f"[-] Error querying CT logs: {e}")
            return []
        except json.JSONDecodeError:
            print("[-] Error parsing CT log response.")
            return []

    def run_enum(self):
        if not self.target_domain:
            print("[-] TARGET_DOMAIN not set. Use 'set TARGET_DOMAIN example.com'.")
            return

        all_found = set()

        # 1. Wordlist enumeration
        wordlist_found = self.enum_from_wordlist()
        all_found.update(wordlist_found)

        # 2. Certificate Transparency enumeration (if enabled and requests available)
        if self.include_ct_logs:
            ct_found = self.enum_from_ct_logs()
            all_found.update(ct_found)
        else:
            if self.include_ct_logs and not HAS_REQUESTS:
                print("[*] Skipping CT log enumeration (requests not available).")

        # 3. Output results
        if all_found:
            print(f"\n[*] Total unique subdomains found: {len(all_found)}")
            with open(self.output_file, "w") as f:
                for sub in sorted(all_found):
                    f.write(sub + "\n")
            print(f"[*] Results saved to: {self.output_file}")
        else:
            print(f"\n[*] No subdomains found for {self.target_domain}.")

# ========== CONSOLE ==========
def main():
    session = SubdomainEnumeratorSession()
    print("Malqart Subdomain Enumerator v1.1 — Fast & Malqart-Style")
    print("Uses wordlists (integrated SecLists) and Certificate Transparency logs (optional)\n")

    while True:
        try:
            cmd = input("MalqartSubEnum > ").strip()
            if not cmd:
                continue

            parts = cmd.split()
            action = parts[0].lower()

            if action in ["exit", "quit"]:
                print("[*] Exiting Malqart Subdomain Enumerator.")
                break

            elif action in ["help", "?"]:
                print("""
Commands:
  set TARGET_DOMAIN <domain>     → Target domain (e.g., example.com) (required)
  set WORDLIST </path/to/file>   → Path to subdomain wordlist (default: SecLists or subdomains.txt)
  set THREADS <num>              → Number of concurrent threads (default: 50)
  set TIMEOUT <sec>              → DNS query timeout (default: 3.0)
  set OUTPUT_FILE <file>         → Output filename (default: malqart_subdomains.txt)
  set INCLUDE_CT_LOGS <true/false> → Query crt.sh (requires 'requests') (default: false)
  set VERBOSE <true/false>       → Show failed attempts (default: false)
  show options                   → Display current settings
  run / exploit                  → Start enumeration
  exit                           → Quit
""")

            elif action == "set":
                if len(parts) < 3:
                    print("[-] Usage: set <OPTION> <VALUE>")
                    continue
                opt = parts[1].upper()
                val = ' '.join(parts[2:])
                if opt == "TARGET_DOMAIN":
                    session.target_domain = val
                elif opt == "WORDLIST":
                    session.wordlist_path = val
                elif opt == "THREADS":
                    session.threads = int(val)
                elif opt == "TIMEOUT":
                    session.timeout = float(val)
                elif opt == "OUTPUT_FILE":
                    session.output_file = val
                elif opt == "INCLUDE_CT_LOGS":
                    session.include_ct_logs = val.lower() in ("1", "true", "yes", "on")
                elif opt == "VERBOSE":
                    session.verbose = val.lower() in ("1", "true", "yes", "on")
                else:
                    print("[-] Valid options: TARGET_DOMAIN, WORDLIST, THREADS, TIMEOUT, OUTPUT_FILE, INCLUDE_CT_LOGS, VERBOSE")
                    continue
                print(f"[*] {opt} => {val}")

            elif action == "show" and len(parts) > 1 and parts[1].lower() == "options":
                session.show_options()

            elif action in ["run", "exploit"]:
                session.run_enum()

            else:
                print(f"[-] Unknown command. Type 'help'.")

        except KeyboardInterrupt:
            print("\n[*] Use 'exit' to quit.")
        except EOFError:
            print("\n[*] Exiting.")
            break
        except ValueError as e:
            print(f"[-] Invalid value: {e}")
        except Exception as e:
            print(f"[-] Error: {e}")

if __name__ == "__main__":
    main()
