#!/usr/bin/env python3
import os
import sys
import requests
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

try:
    from MalqartDatabase_config import get_wordlist_path
    DB_AVAILABLE = True
except ImportError:
    print("[-] MalqartDatabase_config.py not found. Wordlist integration unavailable.")
    DB_AVAILABLE = False

class URIEnumeratorSession:
    def __init__(self):
        self.target_url = None
        self.wordlist_path = "common.txt" # Default common web content list
        self.threads = 50
        self.timeout = 10.0
        self.status_codes = [200, 204, 301, 302, 403, 500] # Default codes to show
        self.extensions = "" # e.g., "php,html,js" - empty means no extension fuzzing
        self.output_file = "malqart_uri_enum_results.txt"
        self.verbose = False
        self.rate_limit = 0 # Requests per second, 0 = no limit

    def show_options(self):
        print("\nModule options:")
        print(f"  TARGET_URL    => {self.target_url}")
        print(f"  WORDLIST      => {self.wordlist_path}")
        print(f"  THREADS       => {self.threads}")
        print(f"  TIMEOUT       => {self.timeout}")
        print(f"  STATUS_CODES  => {','.join(map(str, self.status_codes))}")
        print(f"  EXTENSIONS    => {self.extensions or 'None'}")
        print(f"  OUTPUT_FILE   => {self.output_file}")
        print(f"  VERBOSE       => {self.verbose}")
        print(f"  RATE_LIMIT    => {self.rate_limit} req/s\n")

    def load_wordlist(self):
        """Load a wordlist from the specified path, using MalqartDatabase if available."""
        wordlist_path_obj = Path(self.wordlist_path)

        # Try to resolve using MalqartDatabase if available and file doesn't exist locally
        if DB_AVAILABLE and not wordlist_path_obj.is_file():
            resolved_path = get_wordlist_path("Discovery/Web-Content", self.wordlist_path)
            if resolved_path:
                wordlist_path_obj = Path(resolved_path)

        if not wordlist_path_obj.is_file():
            print(f"[-] Wordlist file '{self.wordlist_path}' not found (resolved to: {wordlist_path_obj}).")
            if DB_AVAILABLE:
                print(f"[*] Hint: SecLists web content lists are available in 'MalqartDatabase/Discovery/Web-Content/'")
            return []

        print(f"[*] Loading wordlist: {wordlist_path_obj}")
        try:
            with open(wordlist_path_obj, "r", encoding="utf-8", errors="ignore") as f:
                # Use set to avoid duplicates if present in the list, then back to list
                paths = list(set(line.strip() for line in f if line.strip()))
        except Exception as e:
            print(f"[-] Error reading wordlist '{wordlist_path_obj}': {e}")
            return []

        # Handle extensions
        if self.extensions:
            ext_list = [ext.strip() for ext in self.extensions.split(',')]
            expanded_paths = []
            for p in paths:
                if p.startswith('/'):
                    p = p[1:] # Remove leading slash for joining
                for ext in ext_list:
                    if ext.startswith('.'):
                        ext = ext[1:] # Remove leading dot if present
                    expanded_paths.append(f"{p}.{ext}")
            paths = expanded_paths

        print(f"[*] Loaded {len(paths)} unique paths from wordlist (including extensions).")
        return paths

    def make_request(self, session, path):
        """Make a single HTTP request."""
        url = f"{self.target_url.rstrip('/')}/{path.lstrip('/')}"
        try:
            start_time = time.time()
            resp = session.get(url, timeout=self.timeout)
            end_time = time.time()
            response_time = end_time - start_time
            return url, resp.status_code, len(resp.content), response_time
        except requests.exceptions.RequestException as e:
            if self.verbose:
                print(f"  [-] Error for {url}: {e}")
            return url, None, 0, 0

    def run_enum(self):
        if not self.target_url:
            print("[-] TARGET_URL not set. Use 'set TARGET_URL http://example.com'.")
            return

        paths = self.load_wordlist()
        if not paths:
            return

        print(f"[*] Enumerating URIs on: {self.target_url}")
        print(f"[*] Using {self.threads} threads, {self.timeout}s timeout.")
        if self.rate_limit > 0:
            print(f"[*] Rate limiting to {self.rate_limit} requests per second.")

        found_items = []
        # Use a requests session for connection pooling
        with requests.Session() as session:
            # Set a common User-Agent
            session.headers.update({"User-Agent": "Malqart-URI-Enum/1.0"})

            # Calculate delay between requests if rate limiting is enabled
            delay = 1.0 / self.rate_limit if self.rate_limit > 0 else 0

            with ThreadPoolExecutor(max_workers=self.threads) as executor:
                # Submit all tasks
                future_to_path = {
                    executor.submit(self.make_request, session, path): path
                    for path in paths
                }

                # Process completed tasks
                for future in as_completed(future_to_path):
                    url, status_code, content_length, response_time = future.result()

                    if status_code in self.status_codes:
                        item_str = f"{status_code} - {content_length} bytes - {url} (Time: {response_time:.2f}s)"
                        print(f"  [+] {item_str}")
                        found_items.append(item_str)
                    elif self.verbose:
                        print(f"  [-] {status_code} - {url}")

                    # Apply rate limit delay if necessary
                    if delay > 0:
                        time.sleep(delay)

        # Save results
        if found_items:
            print(f"\n[*] Found {len(found_items)} item(s).")
            with open(self.output_file, "w") as f:
                for item in found_items:
                    f.write(item + "\n")
            print(f"[*] Results saved to: {self.output_file}")
        else:
            print("\n[*] No items found matching the status codes.")


# ========== CONSOLE ==========
def main():
    session = URIEnumeratorSession()
    print("Malqart URI Enumerator v1.0 — Fast & Malqart-Style")
    print("Enumerates URIs (directories/files) using wordlists\n")

    while True:
        try:
            cmd = input("MalqartURI > ").strip()
            if not cmd:
                continue

            parts = cmd.split()
            action = parts[0].lower()

            if action in ["exit", "quit"]:
                print("[*] Exiting Malqart URI Enumerator.")
                break

            elif action in ["help", "?"]:
                print("""
Commands:
  set TARGET_URL <url>           → Target base URL (e.g., http://example.com) (required)
  set WORDLIST </path/to/file>   → Path to URI wordlist (default: common.txt)
  set THREADS <num>              → Number of concurrent threads (default: 50)
  set TIMEOUT <sec>              → HTTP request timeout (default: 10.0)
  set STATUS_CODES <code1,code2> → List of status codes to show (default: 200,204,301,302,403,500)
  set EXTENSIONS <ext1,ext2>     → Extensions to fuzz (e.g., php,html,js) (default: None)
  set OUTPUT_FILE <file>         → Output filename (default: malqart_uri_enum_results.txt)
  set VERBOSE <true/false>       → Show all attempts (default: false)
  set RATE_LIMIT <num>           → Max requests per second (0 = no limit) (default: 0)
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

                if opt == "TARGET_URL":
                    session.target_url = val
                elif opt == "WORDLIST":
                    session.wordlist_path = val
                elif opt == "THREADS":
                    session.threads = int(val)
                elif opt == "TIMEOUT":
                    session.timeout = float(val)
                elif opt == "STATUS_CODES":
                    session.status_codes = [int(code.strip()) for code in val.split(',')]
                elif opt == "EXTENSIONS":
                    session.extensions = val
                elif opt == "OUTPUT_FILE":
                    session.output_file = val
                elif opt == "VERBOSE":
                    session.verbose = val.lower() in ("1", "true", "yes", "on")
                elif opt == "RATE_LIMIT":
                    session.rate_limit = float(val)
                else:
                    print("[-] Valid options: TARGET_URL, WORDLIST, THREADS, TIMEOUT, STATUS_CODES, EXTENSIONS, OUTPUT_FILE, VERBOSE, RATE_LIMIT")
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
