# 2FA bypass using a brute-force attack
- Here we need to use Macros to be able to get newly generated CSRF with every new request, which allows us to automate this process.

## Steps: 
1. Open Burp, and get the intercept on
2. login with the given credentials 
   - You should notice two requests
     - Get login
       - In the response (HTML), you will find the csrf token, which is used when the POST request is sent.
     - POST login
3. Then you will be forwarded to login2 page in which you should insert 2FA code, insert any value and capture it with proxy
   - You should notice 
     - GET login2
     - POST login2
4. Go to Settings -> Sessions -> Macros
   1. Add macro
   2. Select the 4 requests:
      1. GET login
      2. POST login
      3. GET login2
      4. POST login2
   3. press ok
   4. configure GET login item
   5. press add custom parameter
      1. scroll down until csrf, and hover over it
      2. press ok
   6. config GET login2 
   7. press add custom parameter
      1. scroll down until csrf, and hover over it
      2. press ok
   8. press Add at Session handling rules
   9. press Add rules
      1.  Execute macro and select the previous macro
    10.  press Scope, and select all URLs or he provided URL
    11.  Go back and send the POST login2 to the intruder
    12.  Go to Resource pool, and set the max concurrent requests = 1
    13.  run the attack, and wait until you find the response with 302
    14.  copy the session cookie in the session and go to the home page, and then go to the login page, you should find that you already  logged in. 
    15.  Now the lab is done :)