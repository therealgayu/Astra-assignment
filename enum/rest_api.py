import requests

def enumerate_via_rest_api(target_url, timeout=10):
    """
    Attempts WordPress user enumeration via the REST API.
    Returns a list of dicts: [{"username": str, "evidence": str}, ...]
    Returns an empty list if nothing found or on error.
    """
    endpoint = f"{target_url.rstrip('/')}/wp-json/wp/v2/users"
    results = []

    try:
        response = requests.get(endpoint, timeout=timeout)
    except requests.exceptions.RequestException as e:
        print(f"[!] Network error reaching {endpoint}: {e}")
        return results

    if response.status_code != 200:
        print(f"[!] REST API returned status {response.status_code}, trying fallback...")
        # fallback for sites with "Plain" permalinks
        fallback_endpoint = f"{target_url.rstrip('/')}/?rest_route=/wp/v2/users"
        try:
            response = requests.get(fallback_endpoint, timeout=timeout)
        except requests.exceptions.RequestException as e:
            print(f"[!] Network error reaching fallback: {e}")
            return results

    if response.status_code != 200:
        print(f"[!] Fallback also failed with status {response.status_code}")
        return results

    try:
        users = response.json()
    except ValueError:
        print("[!] Response was not valid JSON")
        return results

    if not isinstance(users, list):
        print("[!] Unexpected response format")
        return results

    for user in users:
        username = user.get("slug") or user.get("name")
        if username:
            results.append({
                "username": username,
                "evidence": endpoint
            })

    return results


if __name__ == "__main__":
    import sys
    target = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8080"
    found = enumerate_via_rest_api(target)
    if found:
        print(f"[+] Found {len(found)} user(s) via REST API:")
        for u in found:
            print(f"    - {u['username']}")
    else:
        print("[-] No users found via REST API.")