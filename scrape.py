from datetime import datetime
import requests
from bs4 import BeautifulSoup


class Page:
    def __init__(self, url=None):
        self.url = url
        self.soup = None
        self.date = None
        self.title = None
        self.content = None
        if self.url:
            self.get_data()

    def get_url(self, url):
        self.url = url

    def get_data(self):
        if self.url:
            self.soup = self.get_soup(self.url)
            self.date = self.get_date(self.soup)
            self.title = self.get_title(self.soup)
            self.content = self.get_content(self.soup)

    def get_soup(self, url):
        htmlpage = requests.get(url, timeout=10)
        soup = BeautifulSoup(htmlpage.text, 'html.parser')
        return soup

    def get_date(self, soup):
        html = soup.find("div", {"class": "postDate"})
        list_date = html.text.replace(',', '').split(' ')
        if list_date[0] == 'Updated:': list_date.pop(0)
        result = datetime.strptime(' '.join(list_date[:3]), '%b %d %Y')
        return result.date()

    def get_content(self, soup):
        content = soup.find("div", {"class": "postContent"})
        result = []
        for line in content.text.split('\n'):
            if bool(line) and not line.isspace():
                result.append(line.lstrip().rstrip())
        return "".join(result)

    def get_title(self, soup):
        title = soup.find("h1", {"class": "m1-article-title"})
        return title.text
