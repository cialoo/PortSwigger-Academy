# PortSwigger Academy

This repository serves as a live progress tracker.

##

## Academy Progress Metrics

<img width="739" height="231" alt="image" src="https://github.com/user-attachments/assets/5921dc32-2282-4bd9-bc52-9c97a7c33a6f" />

##

## Lab automation

**Lab: Blind SQL injection with conditional responses (Practitioner)**

Because manual brute-forcing of a 20-character password would be miserable, I initially tried using the "Intruder" tool in Burp Suite. However, since I am using the Community Edition, the execution is artificially rate-limited and takes way too long. To bypass this performance ceiling, I decided to build my own custom automation script in Python.

Prerequisites to extract from the HTTP requests (e.g., using Burp Suite):
1. **Target URL** with a category filter: 'web-security-academy.net/filter?category=Gifts'
2. **TrackingId** cookie value from GET request: 'WRZcL3blKj8g33lD'
3. **Session** cookie value from GET request: 'nL2y3jQS7RGGszFBzSetHZfPfGPrOgOq'

By copying these 3 elements into the Python script, it dynamically treats the application response as a "Boolean Oracle" (checking for the "Welcome back" string) to exfiltrate the full administrator password character-by-character.

The script is available here: https://github.com/cialoo/PortSwigger-Academy/blob/main/portswigger-blind_sqli_oracle.py

##
