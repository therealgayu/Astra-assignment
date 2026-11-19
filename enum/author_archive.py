import requests

def enumerate_via_author_archive(target_url, max_id=10, timeout=10):
    """
    Attempts WordPress user enumeration via ?author=N redirect leakage.
    Returns a list of dicts: [{"username": str, "evidence": str}, ...]
    """
    results = []
    seen_usernames = set()

    for user_id in range(1, max_id + 1):
        probe_url = f"{target_url.rstrip('/')}/?author={user_id}"

        try:
            response = requests.get(probe_url, timeout=timeout, allow_redirects=True)
        except requests.exceptions.RequestException as e:
            print(f"[!] Network error on author={user_id}: {e}")
            continue

        final_url = response.url

        # If WordPress redirected to /author/<username>/, that's the leak
        if "/author/" in final_url:
            try:
                username = final_url.rstrip('/').split("/author/")[1].split("/")[0]
            except IndexError:
                continue

            if username and username not in seen_usernames:
                seen_usernames.add(username)
                results.append({
                    "username": username,
                    "evidence": f"{probe_url} -> redirected to {final_url}"
                })

    return results


if __name__ == "__main__":
    import sys
    target = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8080"
    found = enumerate_via_author_archive(target)
    if found:
        print(f"[+] Found {len(found)} user(s) via author archive:")
        for u in found:
            print(f"    - {u['username']}")
    else:
        print("[-] No users found via author archive.")