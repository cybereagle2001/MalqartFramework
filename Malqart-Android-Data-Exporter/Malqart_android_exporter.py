#!/usr/bin/env python3
import os
import sys
import shutil
import time
from pathlib import Path

class AndroidDataExporterSession:
    def __init__(self):
        self.source_dir = None
        self.output_dir = "malqart_android_dbs"
        self.include_wal = False  # Include SQLite WAL files
        self.include_shm = False  # Include SQLite SHM files

    def show_options(self):
        print("\nModule options:")
        print(f"  SOURCE_DIR  => {self.source_dir}")
        print(f"  OUTPUT_DIR  => {self.output_dir}")
        print(f"  INCLUDE_WAL => {self.include_wal}")
        print(f"  INCLUDE_SHM => {self.include_shm}\n")

    def find_databases(self, path):
        """Find potential database files recursively."""
        db_extensions = ['.db', '.sqlite', '.sqlite3', '.db3', '.db-shm', '.db-wal']
        found = []
        for root, dirs, files in os.walk(path):
            for f in files:
                if any(f.lower().endswith(ext) for ext in db_extensions):
                    # Filter out WAL/SHM if not requested
                    if f.lower().endswith('.wal') and not self.include_wal:
                        continue
                    if f.lower().endswith('.shm') and not self.include_shm:
                        continue
                    found.append(os.path.join(root, f))
        return found

    def run_export(self):
        if not self.source_dir:
            print("[-] SOURCE_DIR not set. Use 'set SOURCE_DIR /path/to/android/data'.")
            return

        if not os.path.isdir(self.source_dir):
            print(f"[-] SOURCE_DIR '{self.source_dir}' is not a directory or does not exist.")
            return

        print(f"[*] Searching for databases in: {self.source_dir}")
        databases = self.find_databases(self.source_dir)

        if not databases:
            print("[*] No database files found in the specified directory.")
            return

        print(f"[*] Found {len(databases)} potential database file(s).")
        print(f"[*] Exporting to: {self.output_dir}")

        os.makedirs(self.output_dir, exist_ok=True)

        copied_count = 0
        for db_path in databases:
            rel_path = os.path.relpath(db_path, self.source_dir)
            dest_path = os.path.join(self.output_dir, rel_path)
            dest_dir = os.path.dirname(dest_path)

            os.makedirs(dest_dir, exist_ok=True)

            try:
                shutil.copy2(db_path, dest_path)
                print(f"  [+] Copied: {rel_path}")
                copied_count += 1
            except Exception as e:
                print(f"  [-] Failed to copy {rel_path}: {e}")

        print(f"\n[*] Export completed. {copied_count} database file(s) copied to '{self.output_dir}'.")

        # Print the tree structure of the output directory
        print(f"\n[*] Final directory structure of '{self.output_dir}':")
        print_tree(Path(self.output_dir))

# ========== CONSOLE ==========
def print_tree(path, prefix="", is_last=True):
    """
    Prints a tree-like structure of the given path.
    Mimics the 'tree' command output.
    """
    if not path.exists():
        print(f"{prefix}{'└── ' if is_last else '├── '}<directory does not exist>")
        return

    contents = sorted(path.iterdir(), key=lambda x: (x.is_file(), x.name))
    pointers = ["├── ", "└── "]

    for i, item in enumerate(contents):
        is_last_item = i == len(contents) - 1
        current_pointer = pointers[is_last_item]
        print(f"{prefix}{current_pointer}{item.name}")

        if item.is_dir():
            extension = "    " if is_last_item else "│   "
            print_tree(item, prefix=prefix + extension, is_last=is_last_item)

def main():
    session = AndroidDataExporterSession()
    print("Malqart Android Data Exporter v1.0 — Export Databases from Android Data Dir")
    print("⚠️  Requires local access to Android data directory (e.g., adb pull output)\n")

    while True:
        try:
            cmd = input("MalqartAndroid > ").strip()
            if not cmd:
                continue

            parts = cmd.split()
            action = parts[0].lower()

            if action in ["exit", "quit"]:
                print("[*] Exiting Malqart Android Data Exporter.")
                break

            elif action in ["help", "?"]:
                print("""
Commands:
  set SOURCE_DIR </path/to/android/data>  → Source Android data directory (required)
  set OUTPUT_DIR </path/to/export>        → Destination directory (default: malqart_android_dbs)
  set INCLUDE_WAL <true/false>            → Include SQLite WAL files (default: false)
  set INCLUDE_SHM <true/false>            → Include SQLite SHM files (default: false)
  show options                            → Display current settings
  run / exploit                           → Start export process
  exit                                    → Quit
""")

            elif action == "set":
                if len(parts) < 3:
                    print("[-] Usage: set <OPTION> <VALUE>")
                    continue
                opt = parts[1].upper()
                val = ' '.join(parts[2:])
                if opt == "SOURCE_DIR":
                    session.source_dir = val
                elif opt == "OUTPUT_DIR":
                    session.output_dir = val
                elif opt == "INCLUDE_WAL":
                    session.include_wal = val.lower() in ("1", "true", "yes", "on")
                elif opt == "INCLUDE_SHM":
                    session.include_shm = val.lower() in ("1", "true", "yes", "on")
                else:
                    print("[-] Valid options: SOURCE_DIR, OUTPUT_DIR, INCLUDE_WAL, INCLUDE_SHM")
                    continue
                print(f"[*] {opt} => {val}")

            elif action == "show" and len(parts) > 1 and parts[1].lower() == "options":
                session.show_options()

            elif action in ["run", "exploit"]:
                session.run_export()

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
