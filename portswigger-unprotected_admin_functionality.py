import requests
import itertools

url = 'https://0ae6000b044148e08176938900c800f5.web-security-academy.net/'

with open('common.txt', 'r') as file:
    wordlist = file.read().splitlines()

loading_chars = itertools.cycle(['|', '/', '-', '\\'])

def loading_animation():
    print('\r' + next(loading_chars), end='')

def discover_resources(words, url):

   for word in words:

        target_url = url + word
        
        try:
            request = requests.get(target_url)
            loading_animation()
            if request.status_code != 404:
                print('URL -> ' + target_url)
        except requests.RequestException:
            pass

discover_resources(wordlist, url)