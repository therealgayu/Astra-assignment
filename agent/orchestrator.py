import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from enumeration.rest_api import enumerate_via_rest_api
from enumeration.author_archive import enumerate_via_author_archive


def run_enumeration(target_url):
    """
    Agent loop: tries techniques in order of reliability/stealth.
    Returns (users_found, techniques_used)
    """
    techniques_used = []

    print("[AI Agent] Selecting technique...")
    print("  -> Trying REST API enumeration.")
    techniques_used.append("rest_api")
    users = enumerate_via_rest_api(target_url)

    if users:
        return users, techniques_used

    print("[AI Agent] REST API yielded nothing. Falling back.")
    print("  -> Trying author archive enumeration.")
    techniques_used.append("author_archive")
    users = enumerate_via_author_archive(target_url)

    return users, techniques_used


if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8080"
    found, techniques = run_enumeration(target)

    if found:
        print(f"[+] Found {len(found)} user(s) using: {', '.join(techniques)}")
        for u in found:
            print(f"    - {u['username']}")
    else:
        print("[-] No users found with any technique.")