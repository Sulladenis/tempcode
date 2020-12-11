import requests
from bs4 import BeautifulSoup
from concurrent.futures import ProcessPoolExecutor, as_completed
import settings

def get_URLs(url, num):
    return [url+f"?p={i}" for i in range(1, num)]

def get_urls(url):
    urls = []
    htmlpage = requests.get(url)
    soup = BeautifulSoup(htmlpage.text, 'html.parser')
    items = soup.find_all("a", {"class": "thumb zoom"})
    for item in items:
        if item['href'].count('https') == 0:
            urls.append(settings.URL+item['href'])
    return set(urls)

def get_all_urls():
    num = search()
    URLs = get_URLs(settings.URL, num)
    with ProcessPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(get_urls, url) for url in URLs]
        all_urls = []
        for future in enumerate(as_completed(futures)):
            all_urls.extend(future[1].result())
            print('extend ', future[0] )
    return all_urls

def search(mn=0, mx=10000):
    while (mx - mn) != 1:
        num = int((mx - mn) / 2 + mn)
        print(mn, mx, num)
        pref = f"?p={num}"
        urls = get_urls(settings.URL+pref)
        if len(urls) > 15:
            mn = num
        if len(urls) < 15:
            mx = num
    return num
