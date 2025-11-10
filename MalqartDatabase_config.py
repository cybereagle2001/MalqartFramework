# MalqartFramework/MalqartDatabase_config.py
import subprocess
import sys
from pathlib import Path

# Assuming this script is in the main MalqartFramework directory,
# and modules are subdirectories next to MalqartDatabase
MALQART_DB_PATH = Path(__file__).parent / "MalqartDatabase"

# Define required libraries for the framework and its modules
REQUIRED_LIBRARIES = [
    "requests", # For Malqart_nvdscanner.py, Malqart_subdomain_enum.py, Malqart_bruteforcer.py (HTTP)
    "cvss",     # For Malqart_cvss.py
    "paramiko", # For Malqart_bruteforcer.py (SSH)
    # Add more libraries as needed by other modules
    # e.g., "pysnmp", "pycryptodome" (for potential RouterSploit-style modules)
]

# Define common SecLists files to download as a starter pack
SECLISTS_STARTER_FILES = {
    "Discovery/Subdomains": [
        "subdomains-top1million-5000.txt",
        "subdomains-10000.txt",
        "subdomains-1000.txt"
    ],
    "Discovery/Web-Content": [
        "common.txt",
        "raft-large-words-lowercase.txt"
    ],
    "Passwords": [
        "10-million-password-list-top-100.txt",
        "rockyou.txt" # Add a more common one if desired, though it's large
    ],
    "Usernames": [
        "usernames.txt"
    ]
}

def get_wordlist_path(category, filename):
    """
    Get the full path to a SecLists wordlist.
    Args:
        category (str): The subdirectory under MalqartDatabase (e.g., 'Discovery/Subdomains').
        filename (str): The name of the wordlist file (e.g., 'subdomains-top1million-5000.txt').
    Returns:
        str: Full path to the file if it exists, else None.
    """
    full_path = MALQART_DB_PATH / category / filename
    if full_path.is_file():
        return str(full_path)
    else:
        print(f"[-] Wordlist {filename} not found in {category} ({full_path})")
        return None

def list_available_wordlists(category):
    """
    List available .txt wordlists in a SecLists category.
    Args:
        category (str): The subdirectory under MalqartDatabase.
    Returns:
        list: List of filenames found.
    """
    cat_path = MALQART_DB_PATH / category
    if cat_path.is_dir():
        return [f.name for f in cat_path.iterdir() if f.is_file() and f.suffix == '.txt']
    else:
        print(f"[-] Category {category} not found in MalqartDatabase ({cat_path})")
        return []

def install_libraries(libs=None):
    """
    Attempts to install required Python libraries using pip.
    Args:
        libs (list, optional): List of library names to install. Defaults to REQUIRED_LIBRARIES.
    """
    if libs is None:
        libs = REQUIRED_LIBRARIES

    print(f"[*] Attempting to install required libraries: {', '.join(libs)}")
    for lib in libs:
        try:
            # Check if library is already installed
            __import__(lib)
            print(f"  [i] {lib} is already installed.")
        except ImportError:
            print(f"  [+] Installing {lib}...")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", lib])
                print(f"  [+] Successfully installed {lib}.")
            except subprocess.CalledProcessError as e:
                print(f"  [-] Failed to install {lib}. Error: {e}")
                print(f"      Please install it manually using 'pip3 install {lib}'.")

def download_seclists_starter():
    """
    Downloads a starter pack of SecLists files using git.
    This is a basic implementation that clones the entire repo into a temporary location
    and copies only the specified starter files.
    """
    seclists_repo_url = "https://github.com/danielmiessler/SecLists.git" # Fixed trailing space
    temp_dir = MALQART_DB_PATH / "temp_seclists_download"

    if MALQART_DB_PATH.is_dir():
        print(f"[*] MalqartDatabase directory exists: {MALQART_DB_PATH}")
    else:
        print(f"[*] Creating MalqartDatabase directory: {MALQART_DB_PATH}")
        MALQART_DB_PATH.mkdir(parents=True, exist_ok=True)

    print(f"[*] Downloading SecLists starter files...")
    try:
        # Clone the entire SecLists repo into a temporary directory
        print("  [+] Cloning SecLists repository (this might take a while)...")
        subprocess.check_call(["git", "clone", seclists_repo_url, str(temp_dir)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        # Copy the specified starter files
        for category, filenames in SECLISTS_STARTER_FILES.items():
            category_path = temp_dir / category
            target_category_path = MALQART_DB_PATH / category
            target_category_path.mkdir(parents=True, exist_ok=True)

            for filename in filenames:
                source_file = category_path / filename
                target_file = target_category_path / filename
                if source_file.is_file():
                    print(f"  [+] Copying {category}/{filename}")
                    target_file.write_bytes(source_file.read_bytes()) # Simple copy
                else:
                    print(f"  [-] Starter file not found in repo: {source_file}")

        # Clean up the temporary directory
        import shutil
        print("  [+] Cleaning up temporary download directory...")
        shutil.rmtree(temp_dir)
        print("  [+] SecLists starter pack setup complete.")

    except subprocess.CalledProcessError as e:
        print(f"[-] Failed to download SecLists: {e}")
        print("    Ensure 'git' is installed and you have internet access.")
        if temp_dir.exists():
            import shutil
            shutil.rmtree(temp_dir)
    except Exception as e:
        print(f"[-] An unexpected error occurred during SecLists download: {e}")
        if temp_dir.exists():
            import shutil
            shutil.rmtree(temp_dir)

def setup_framework():
    """
    Convenience function to run both library installation and SecLists download.
    """
    print("--- Malqart Framework Setup ---")
    install_libraries()
    print("") # Add a newline for clarity
    download_seclists_starter()
    print("--- Setup Complete ---")

# Example usage within a module:
# path = get_wordlist_path("Discovery/Subdomains", "subdomains-top1million-5000.txt")
# if path:
#    print(f"Using wordlist: {path}")

if __name__ == "__main__":
     setup_framework()
