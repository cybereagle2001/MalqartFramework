# MalqartFramework/MalqartDatabase_config.py
# MalqartFramework/MalqartDatabase_config.py
from pathlib import Path

# Assuming this script is in the main MalqartFramework directory,
# and modules are subdirectories next to MalqartDatabase
MALQART_DB_PATH = Path(__file__).parent / "MalqartDatabase"

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

# Example usage within a module:
# path = get_wordlist_path("Discovery/Subdomains", "subdomains-top1million-5000.txt")
# if path:
#    print(f"Using wordlist: {path}")
