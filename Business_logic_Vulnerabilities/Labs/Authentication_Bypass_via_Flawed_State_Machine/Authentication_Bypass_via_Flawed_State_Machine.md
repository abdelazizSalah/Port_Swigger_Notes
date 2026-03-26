[Solved](./image.png)

- This lab taught me that I should not follow the sequence provided by the application, and to try to get out from it. 

## Lab solution
1. Open burp and investigate every request
2. Log in as wiener
   1. you will notice that we call the **/login** endpoint.
   2. after authentication you will notice that there is a GET request to the **/role-selector** endpoint, in which it defines which role you want to use -> here is the problem, because the application assumes that you will follow the same order given by it. 
   3. So all you need is to remove the role-selection and to call the home instead
      1. GET / ...
3. Then you will find that you can see the admin panel and all you need to do is to remove carlos :)