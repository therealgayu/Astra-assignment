import os
import sys
import json
from dotenv import load_dotenv

load_dotenv()

from agent.orchestrator import run_enumeration
from agent.summarizer import generate_summary


def main():
    target = os.getenv("TARGET_URL", "http://localhost:8080")
    if len(sys.argv) > 1:
        target = sys.argv[1]

    print(f"[+] Target: {target}")
    print("[+] Starting WordPress user enumeration...\n")

    users_found, techniques_used = run_enumeration(target)

    print()
    if users_found:
        print(f"[+] Found usernames:")
        for u in users_found:
            print(f"    - {u['username']} (evidence: {u['evidence']})")
    else:
        print("[-] No usernames found.")

    print("\n[AI Agent] Generating summary...")
    summary = generate_summary(target, users_found, techniques_used)
    print(f"[AI Agent] Summary:\n{summary}\n")

    result = {
        "target": target,
        "techniques_used": techniques_used,
        "users": users_found,
        "ai_summary": summary,
    }

    with open("results.json", "w") as f:
        json.dump(result, f, indent=2)

    print("[✓] Enumeration complete. Results saved to results.json")


if __name__ == "__main__":
    main()