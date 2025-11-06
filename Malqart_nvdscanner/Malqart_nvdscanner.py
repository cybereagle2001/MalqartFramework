#!/usr/bin/env python3
import socket
import sys
import re
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import json  # for parsing NVD response

try:
    import requests
    from urllib.parse import quote
except ImportError:
    print("[-] 'requests' is required. Install with: pip3 install requests")
    sys.exit(1)

# ========= CPE MAPPING RULES (Lightweight, Expandable) =========
# Format: (regex, vendor, product)
CPE_RULES = [
    # Web Servers
    (r"(Apache httpd) ([\d\.]+)", "apache", "http_server"),
    (r"(nginx)/([\d\.]+)", "f5", "nginx"),
    (r"(Apache Tomcat)/([\d\.]+)", "apache", "tomcat"),
    # SSH
    (r"(OpenSSH)_([\d\.]+)", "openssh", "openssh"),
    # FTP
    (r"(vsftpd) ([\d\.]+)", "vsftpd", "vsftpd"),
    # Databases
    (r"(PostgreSQL) ([\d\.]+)", "postgresql", "postgresql"),
    (r"(MySQL) ([\d\.]+)", "oracle", "mysql"),
    # PHP
    (r"(PHP)/([\d\.]+)", "php", "php"),
    # SMB/Samba
    (r"(Samba) ([\d\.]+)", "samba", "samba"),
    # Generic
    (r"SSH-2.0-dropbear_([\d\.]+)", "dropbear_ssh", "dropbear_ssh"),
]

# ========= SESSION CLASS =========
class NVDScannerSession:
    def __init__(self):
        self.target = None
        self.ports = [21, 22, 23, 25, 53, 80, 110, 139, 143, 443, 445, 993, 995, 1433, 3306, 3389, 5432, 5900, 6379, 8000, 8080, 8443, 9200, 27017]
        self.threads = 100
        self.timeout = 1.0
        self.verbose = False
        self.nvd_api_key = None
        self.cache = {}  # {cpe: [cve_data]}

    def show_options(self):
        print("\nModule options:")
        print(f"  TARGET      => {self.target}")
        print(f"  PORTS       => {len(self.ports)} common ports")
        print(f"  THREADS     => {self.threads}")
        print(f"  TIMEOUT     => {self.timeout}")
        print(f"  VERBOSE     => {self.verbose}")
        print(f"  NVD_API_KEY => {'Set' if self.nvd_api_key else 'Not set (rate limits apply)'}\n")

    def banner_to_cpe(self, banner):
        """Convert banner string to CPE 2.3 formatted string."""
        for pattern, vendor, product in CPE_RULES:
            match = re.search(pattern, banner, re.IGNORECASE)
            if match:
                version = match.groups()[-1]
                # Normalize version string
                version = re.split(r'[^\d\.]', version)[0]
                if version:
                    return f"cpe:2.3:a:{vendor}:{product}:{version}:*:*:*:*:*:*:*"
        return None

    def fetch_cves_from_nvd(self, cpe):
        """Fetch CVEs from NVD API v2.0 by CPE name."""
        if cpe in self.cache:
            return self.cache[cpe]

        url = f"https://services.nvd.nist.gov/rest/json/cves/2.0?cpeName={quote(cpe)}"
        headers = {"User-Agent": "Malqart-NVD-Scanner/1.0"}
        if self.nvd_api_key:
            headers["apiKey"] = self.nvd_api_key

        try:
            if self.verbose:
                print(f"    [NVD] Querying {cpe}...")
            resp = requests.get(url, headers=headers, timeout=10)
            if resp.status_code == 429:
                print("    [!] NVD rate limit exceeded. Use 'set NVD_API_KEY' for higher limits.")
                return []
            elif resp.status_code != 200:
                if self.verbose:
                    print(f"    [!] NVD API error: {resp.status_code}")
                return []

            data = resp.json()
            total_results = data.get("totalResults", 0)
            if total_results == 0:
                self.cache[cpe] = []
                return []

            cves = []
            for vuln in data.get("vulnerabilities", []):
                cve_id = vuln["cve"]["id"]
                metrics = vuln["cve"].get("metrics", {})
                # Prefer v3.1, fallback to v3.0
                cvss_data = None
                for ver in ["cvssMetricV31", "cvssMetricV30"]:
                    if ver in metrics:
                        for m in metrics[ver]:
                            if m["type"] == "Primary":
                                cvss_data = m["cvssData"]
                                break
                        if cvss_data:
                            break

                score = "N/A"
                severity = "N/A"
                if cvss_data:
                    score = cvss_data.get("baseScore", "N/A")
                    severity = cvss_data.get("baseSeverity", "N/A")

                description = vuln["cve"]["descriptions"][0].get("value", "No description") if vuln["cve"].get("descriptions") else "No description"
                cves.append({
                    "id": cve_id,
                    "score": score,
                    "severity": severity,
                    "description": description[:120] + "..." if len(description) > 120 else description
                })
            self.cache[cpe] = cves
            return cves
        except requests.exceptions.Timeout:
            print(f"    [!] NVD query for {cpe} timed out.")
            return []
        except Exception as e:
            if self.verbose:
                print(f"    [!] NVD fetch error: {e}")
            return []

    def grab_banner(self, ip, port):
        """Attempt to grab service banner."""
        try:
            with socket.create_connection((ip, port), timeout=self.timeout) as sock:
                # Send a small probe for HTTP
                if port in [80, 443, 8080, 8443]:
                    sock.send(b"HEAD / HTTP/1.0\r\n\r\n")
                sock.settimeout(self.timeout)
                banner = sock.recv(1024).decode('utf-8', errors='ignore')
                return banner.strip()
        except Exception:
            return ""

    def scan_port(self, ip, port):
        """Scan a single port and grab banner."""
        try:
            with socket.create_connection((ip, port), timeout=self.timeout):
                banner = self.grab_banner(ip, port)
                return port, True, banner
        except Exception:
            return port, False, ""

    def run_scan(self):
        """Execute the full scan."""
        if not self.target:
            print("[-] TARGET not set. Use 'set TARGET <ip>'.")
            return

        print(f"[*] Scanning {self.target} on {len(self.ports)} ports...")
        open_ports = []

        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            futures = {executor.submit(self.scan_port, self.target, p): p for p in self.ports}
            for future in as_completed(futures):
                port, is_open, banner = future.result()
                if is_open:
                    open_ports.append((port, banner))

        open_ports.sort()
        print(f"\n[+] Open ports on {self.target}:")

        total_cves = 0
        for port, banner in open_ports:
            print(f"  {port}/tcp open")
            if banner:
                print(f"    Banner: {banner[:100]}")
                cpe = self.banner_to_cpe(banner)
                if cpe:
                    print(f"    CPE: {cpe}")
                    cves = self.fetch_cves_from_nvd(cpe)
                    if cves:
                        for cve in cves:
                            print(f"      🚨 {cve['id']} | CVSS: {cve['score']} ({cve['severity']})")
                            print(f"         {cve['description']}")
                        total_cves += len(cves)
                    else:
                        print("      → No CVEs found in NVD for this CPE")
                else:
                    print("    → CPE not recognized from banner")
            else:
                print("    Banner: <none>")

        print(f"\n[*] Scan completed. {total_cves} potential vulnerability(ies) found via NVD.")

# ========= CONSOLE =========
def main():
    session = NVDScannerSession()
    print("Malqart NVD Scanner v1.0 — Live CVE Lookup from NVD")
    print("Port scan → Banner → CPE → Live NVD CVE check\n")

    while True:
        try:
            cmd = input("MalqartNVD > ").strip()
            if not cmd:
                continue

            parts = cmd.split()
            action = parts[0].lower()

            if action in ["exit", "quit"]:
                print("[*] Exiting Malqart NVD Scanner.")
                break

            elif action in ["help", "?"]:
                print("""
Commands:
  set TARGET <ip>              → Target IP/hostname (required)
  set NVD_API_KEY <key>        → NVD API key (optional, get from nvd.nist.gov)
  set THREADS <num>            → Concurrent scan threads (default: 100)
  set TIMEOUT <sec>            → Per-port timeout (default: 1.0)
  set VERBOSE <true/false>     → Show NVD query status (default: false)
  show options                 → Display current settings
  run / exploit                → Start the scan
  exit                         → Quit
""")

            elif action == "set":
                if len(parts) < 3:
                    print("[-] Usage: set <OPTION> <VALUE>")
                    continue
                opt = parts[1].upper()
                val = ' '.join(parts[2:])
                if opt == "TARGET":
                    session.target = val
                elif opt == "NVD_API_KEY":
                    session.nvd_api_key = val
                elif opt == "THREADS":
                    session.threads = int(val)
                elif opt == "TIMEOUT":
                    session.timeout = float(val)
                elif opt == "VERBOSE":
                    session.verbose = val.lower() in ("1", "true", "yes", "on")
                else:
                    print("[-] Valid options: TARGET, NVD_API_KEY, THREADS, TIMEOUT, VERBOSE")
                    continue
                print(f"[*] {opt} => {val}")

            elif action == "show" and len(parts) > 1 and parts[1].lower() == "options":
                session.show_options()

            elif action in ["run", "exploit"]:
                session.run_scan()

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
