import requests
from bs4 import BeautifulSoup as bs
import datetime
import MySQLdb
import socket


class crawler:
    def __init__(self,link):
        self.link=link
        self.url=requests.get(self.link)
        self.url_content=self.url.content
        self.url_soup=bs(self.url_content)
    def domain(self):
        domain=self.link.split("//")[-1].split("/")[0]
        return domain
    def time(self):
        time=datetime.datetime.now().strftime("%d:%m:%Y %H:%M:%S")
        return time
    def title(self):
        title=str(self.url_soup.title.get_text())
        return title
    def urls(self):
        urls=list(set([b for b in [a['href'] for a in self.url_soup.find_all('a', href=True) if a.text] if b.startswith('http')]))
        return urls
