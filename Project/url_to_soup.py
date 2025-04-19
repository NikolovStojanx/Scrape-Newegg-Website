import json
import random
import requests
from bs4 import BeautifulSoup


def get_soup_from_url(url):
    try:
        with open("./data/data.json", "r") as file:
            proxies = json.load(file)
    except:
        pass



    for attempt in range(20):
        proxy_choice = random.choice(proxies)
        proxy_url = f"http://{proxy_choice['username']}:{proxy_choice['password']}@{proxy_choice['smartproxy']}:{proxy_choice['port']}"

        try:
            print(f"Attempt {attempt + 1}: Trying proxy {proxy_url}")
            response = requests.get(url, proxies={
                'http': proxy_url,
                'https': proxy_url
            }, timeout=6)

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                return soup
            else:
                print(f"Attempt {attempt + 1}: Received status code {response.status_code}")
        except requests.RequestException as e:
            print(f"Attempt {attempt + 1}: Error with proxy {proxy_url} — {e}")

    print("All attempts failed.")
    return None


