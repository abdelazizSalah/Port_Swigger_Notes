# Lab: Blind SQL injection with time delays and information retrieval

- In this lab we need to use the knowleadge we got from Blind SQLi time based to retrieve the administrator credentials.

# Solution steps
- So now using the same payload from [Lab13](../Lab13-Visual_Error_BSQLi/writeup.md)
    - ' || (SELECT pg_sleep(10)) --
- we can just decrease the sleep amount, and then we can check, if the system sleep, then we know that the query is correct otherwise we know that it is not correct. 
- to do so, we need to look for the case condition in the [cheatsheet](https://portswigger.net/web-security/sql-injection/cheat-sheet)
- Since we know that it is postgreSQL, so we should use this command: 
    - SELECT CASE WHEN (YOUR-CONDITION-HERE) THEN pg_sleep(10) ELSE pg_sleep(0) END 
- So, first we need to check if the users table exist: 
    - IZNnt2wURennW4cW' || (SELECT CASE WHEN (1=1) THEN pg_sleep(3) ELSE pg_sleep(10) END from users where username='administrator' )--
- Now we need to iterate to get the password, but now we will base our solution on time not on status