#!/usr/bin/env python3
import sys

# Dependency check
try:
    from cvss import CVSS3, CVSS4
except ImportError:
    print("[-] Required library 'cvss' not found.")
    print("[*] Install with: pip3 install cvss")
    print("[*] Or on Kali/Debian: sudo apt install python3-cvss")
    sys.exit(1)

class CVSSSession:
    def __init__(self):
        self.version = "3.1"  # Only "3.1" or "4.0"
        self.vector = None
        self.mode = "interactive"  # "interactive" or "paste"

    def show_options(self):
        print("\nModule options:")
        print(f"  VERSION => {self.version}")
        print(f"  MODE    => {self.mode}")
        print(f"  VECTOR  => {self.vector or 'Not set (interactive mode)'}\n")

    def validate_and_score(self, vector: str):
        """Validate and score based on VERSION, auto-adding CVSS prefix if missing."""
        if self.version == "3.1":
            if not vector.startswith("CVSS:3.1/"):
                full_vector = f"CVSS:3.1/{vector}"
            else:
                full_vector = vector
            try:
                c = CVSS3(full_vector)
                base_score = c.scores()[0]
                severity = c.severities()[0]
                return True, base_score, severity
            except Exception as e:
                return False, str(e), None

        elif self.version == "4.0":
            if not vector.startswith("CVSS:4.0/"):
                full_vector = f"CVSS:4.0/{vector}"
            else:
                full_vector = vector
            try:
                c = CVSS4(full_vector)
                base_score = c.scores()[0]
                severity = c.severities()[0]
                return True, base_score, severity
            except Exception as e:
                return False, str(e), None

        else:
            return False, "Unsupported CVSS version. Use '3.1' or '4.0'.", None

    def interactive_v3(self):
        print("\n--- Building CVSS v3.1 Vector ---")
        q = {
            "AV": ("Attack Vector", {"N": "Network", "A": "Adjacent", "L": "Local", "P": "Physical"}),
            "AC": ("Attack Complexity", {"L": "Low", "H": "High"}),
            "PR": ("Privileges Required", {"N": "None", "L": "Low", "H": "High"}),
            "UI": ("User Interaction", {"N": "None", "R": "Required"}),
            "S": ("Scope", {"U": "Unchanged", "C": "Changed"}),
            "C": ("Confidentiality Impact", {"N": "None", "L": "Low", "H": "High"}),
            "I": ("Integrity Impact", {"N": "None", "L": "Low", "H": "High"}),
            "A": ("Availability Impact", {"N": "None", "L": "Low", "H": "High"}),
        }
        parts = []
        for key, (desc, opts) in q.items():
            print(f"\n{desc}:")
            for code, text in opts.items():
                print(f"  [{code}] {text}")
            while True:
                ans = input(f"Select {key}: ").strip().upper()
                if ans in opts:
                    parts.append(f"{key}:{ans}")
                    break
                print("[-] Invalid. Try again.")
        return "/".join(parts)

    def interactive_v4(self):
        print("\n--- Building CVSS v4.0 Vector ---")
        q = {
            "AV": ("Attack Vector", {"N": "Network", "A": "Adjacent", "L": "Local", "P": "Physical"}),
            "AC": ("Attack Complexity", {"L": "Low", "H": "High"}),
            "AT": ("Attack Requirements", {"N": "None", "P": "Present"}),
            "PR": ("Privileges Required", {"N": "None", "L": "Low", "H": "High"}),
            "UI": ("User Interaction", {"N": "None", "P": "Passive", "A": "Active"}),
            "VC": ("Vulnerable System Confid.", {"H": "High", "L": "Low", "N": "None"}),
            "VI": ("Vulnerable System Integrity", {"H": "High", "L": "Low", "N": "None"}),
            "VA": ("Vulnerable System Avail.", {"H": "High", "L": "Low", "N": "None"}),
            "SC": ("Subsequent System Confid.", {"H": "High", "L": "Low", "N": "None"}),
            "SI": ("Subsequent System Integrity", {"S": "Safe", "H": "High", "L": "Low", "N": "None"}),
            "SA": ("Subsequent System Avail.", {"S": "Safe", "H": "High", "L": "Low", "N": "None"}),
        }
        parts = []
        for key, (desc, opts) in q.items():
            print(f"\n{desc}:")
            for code, text in opts.items():
                print(f"  [{code}] {text}")
            while True:
                ans = input(f"Select {key}: ").strip().upper()
                if ans in opts:
                    parts.append(f"{key}:{ans}")
                    break
                print("[-] Invalid. Try again.")
        return "/".join(parts)

    def run(self):
        if self.mode == "paste":
            if not self.vector:
                print("[-] VECTOR not set. Use 'set VECTOR AV:N/AC:L/...'")
                return
            final_vector = self.vector
        else:
            # Interactive mode
            if self.version == "3.1":
                final_vector = self.interactive_v3()
            elif self.version == "4.0":
                final_vector = self.interactive_v4()
            else:
                print("[-] Unsupported VERSION. Set to '3.1' or '4.0'.")
                return

        print(f"\n[+] Input vector: {final_vector}")
        ok, score_or_err, severity = self.validate_and_score(final_vector)

        if ok:
            print(f"\n✅ CVSS {self.version} Base Score: {score_or_err}")
            print(f"   Severity: {severity}")
        else:
            print(f"\n❌ Error: {score_or_err}")

# ========== CONSOLE ==========
def main():
    sess = CVSSSession()
    print("Malqart CVSS Calculator v1.0 — Offline, Accurate, Malqart-Style")
    print("Supports CVSS v3.1 and v4.0. Type 'help' for commands.\n")

    while True:
        try:
            cmd = input("MalqartCVSS > ").strip()
            if not cmd:
                continue

            parts = cmd.split()
            action = parts[0].lower()

            if action in ["exit", "quit"]:
                print("[*] Exiting.")
                break

            elif action in ["help", "?"]:
                print("""
Commands:
  set VERSION <3.1|4.0>        → CVSS version (default: 3.1)
  set MODE <interactive|paste> → Input method
  set VECTOR <AV:N/AC:L/...>   → Full CVSS vector (for paste mode)
  show options                 → Show current config
  run / exploit                → Calculate score
  exit                         → Quit
""")

            elif action == "set":
                if len(parts) < 3:
                    print("[-] Usage: set <OPTION> <VALUE>")
                    continue
                opt = parts[1].upper()
                val = ' '.join(parts[2:])
                if opt == "VERSION":
                    if val in ["3.1", "4.0"]:
                        sess.version = val
                    else:
                        print("[-] VERSION must be '3.1' or '4.0'")
                        continue
                elif opt == "MODE":
                    if val.lower() in ["interactive", "paste"]:
                        sess.mode = val.lower()
                    else:
                        print("[-] MODE must be 'interactive' or 'paste'")
                        continue
                elif opt == "VECTOR":
                    sess.vector = val
                else:
                    print("[-] Valid options: VERSION, MODE, VECTOR")
                    continue
                print(f"[*] {opt} => {val}")

            elif action == "show" and len(parts) > 1 and parts[1].lower() == "options":
                sess.show_options()

            elif action in ["run", "exploit"]:
                sess.run()

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
