# Lab: File path traversal, traversal sequences blocked with absolute path bypass

- Here the traversal is blocked, so when we use this payload:
  - ../../../etc/passwd
- we will get an error.
- so the solution is to use the absolute path
  - /etc/passwd

![Lab_Solved](Lab_Solved.png)