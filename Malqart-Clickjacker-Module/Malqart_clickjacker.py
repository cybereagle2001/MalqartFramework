#!/usr/bin/env python3

import os
import socket
import threading
from http.server import HTTPServer, SimpleHTTPRequestHandler
import webbrowser
import re

# Default port for the local server
PORT = 8000

def find_free_port(start_port=8000):
    """Find a free port starting from start_port."""
    port = start_port
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(('localhost', port)) != 0:
                return port
            port += 1

def start_local_server(directory, port):
    """Start a simple HTTP server in a separate thread."""
    os.chdir(directory)
    handler = SimpleHTTPRequestHandler
    httpd = HTTPServer(("localhost", port), handler)
    print(f"[+] Starting local HTTP server at http://localhost:{port}/")
    httpd.serve_forever()

def sanitize_url(url):
    url = url.strip()
    if not url:
        return None
    if not (url.startswith("http://") or url.startswith("https://")):
        url = "https://" + url
    return url

def generate_clickjacking_poc(target_urls, output_path):
    # Night sky background: deep navy with stars vibe
    background_color = "#0b0c2a"
    text_color = "#e0f7ff"  # Soft icy white
    title_color = "#4fc3f7"  # Light sky blue
    warning_color = "#81d4fa"

    iframes = ""
    for i, url in enumerate(target_urls):
        iframes += f'    <div style="margin: 20px; padding: 10px; background: rgba(15,20,40,0.6); border-radius: 8px;">\n'
        iframes += f'      <h3 style="color: {title_color};">Target #{i+1}: {url}</h3>\n'
        iframes += f'      <iframe src="{url}" width="95%" height="400" style="border: 2px solid #1e88e5; border-radius: 6px;"></iframe>\n'
        iframes += f'    </div>\n'

    poc_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Clickjacking Multi-Target PoC</title>
    <meta name="author" content="m14r41">
    <style>
        body {{
            background-color: {background_color};
            color: {text_color};
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
        }}
        h2 {{
            color: {title_color};
            text-shadow: 0 0 10px rgba(79, 195, 247, 0.7);
        }}
        p {{
            color: {warning_color};
            max-width: 800px;
            line-height: 1.5;
        }}
    </style>
</head>
<body>
    <h2>Clickjacking Vulnerability Multi-Target PoC by Cybereagle2001</h2>
    <p>This vulnerability presents a security risk, allowing for potential manipulation<br>of user interactions and unauthorized data access without user consent.</p>
    
{iframes}
</body>
</html>"""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(poc_content)
    print(f"[+] Clickjacking PoC with {len(target_urls)} targets written to: {output_path}")

def main():
    try:
        raw_input = input("Enter one or more target URLs (separate by commas or spaces): ").strip()
        if not raw_input:
            print("[-] Error: At least one URL is required.")
            return

        # Split by comma or whitespace (handle mixed input)
        urls = re.split(r'[,\s]+', raw_input)
        sanitized_urls = []

        for url in urls:
            clean_url = sanitize_url(url)
            if clean_url:
                sanitized_urls.append(clean_url)

        if not sanitized_urls:
            print("[-] No valid URLs provided.")
            return

        output_file = "clickjacking_poc.html"
        output_path = os.path.join(os.getcwd(), output_file)

        generate_clickjacking_poc(sanitized_urls, output_path)

        port = find_free_port(PORT)

        server_thread = threading.Thread(
            target=start_local_server,
            args=(os.getcwd(), port),
            daemon=True
        )
        server_thread.start()

        local_url = f"http://localhost:{port}/{output_file}"
        print(f"[i] Open this URL in your browser to test: {local_url}")

        try:
            webbrowser.open(local_url)
        except Exception:
            pass  # Safe to ignore in headless environments

        print("[i] Press Ctrl+C to stop the server.")
        try:
            server_thread.join()
        except KeyboardInterrupt:
            print("\n[+] Server stopped.")

    except Exception as e:
        print(f"[-] An error occurred: {e}")

if __name__ == "__main__":
    main()
