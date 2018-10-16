import requests
from bs4 import BeautifulSoup as bs
import datetime
import MySQLdb
import socket


class crawler:

    def __init__(self, link, domain,time,IPs,number_urls,internal_url,external_url,inter_link):
        self.link=link
        self.domain=domain
        self.time=time
        self.IPs=IPs
        self.number_urls=number_urls
        self.internal_url=internal_url
        self.external_url=external_url
        self.inter_link=inter_link

    def request_url(self):
        self.url=requests.get(self.link)
        self.url_content=self.url.content
        self.url_soup=bs(self.url_content)

    def domain(self):
        self.domain=self.link.split("//")[-1].split("/")[0]
        return self.domain

    def time(self):
        self.time=datetime.datetime.now().strftime("%d:%m:%Y %H:%M:%S")
        return self.time

    def title(self):
        self.title=str(self.url_soup.title.get_text())

    def urls(self):
        self.urls=list(set([b for b in [a['href'] for a in self.url_soup.find_all('a', href=True) if a.text] if b.startswith('http')]))
        self.urls
