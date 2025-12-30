# Lab 3: Blind OS command injection with output redirection

- We will try to write a file and read it using the browser. 
- The vulnerability is at the feedback again.
- and we can write in this folder: 
  - > /var/www/images
- and we should see the whoami output
- so this should be our payload:
  - &  whoami> /var/www/images/whoami.txt &
    - peter-uBkJoW -> current user