# Lab: Blind SQL injection with time delays
- The main goal of this lab is to cause 10 seconds delay

- First we need to check the [cheatsheet](https://portswigger.net/web-security/sql-injection/cheat-sheet) to see what are the possible commands for different db to perform this time delay.
- Second, since we do not know which DB we are dealing with, so we will need to try out all possible combinations
- so we will need to do this payload: 
    - ' || (SELECT pg_sleep(10)) --
- then you will see this after you get the response: 
    - ![Lab-Solved](Lab-Solved.png)