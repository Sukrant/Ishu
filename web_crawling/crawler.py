#!/usr/bin/python3.5 

import requests
from bs4 import BeautifulSoup as bs
import datetime
import mysql.connector 
import sys

mydb = mysql.connector.connect(
  host="localhost",
  user="crawler",
  passwd="passw0rd"
)

link=sys.argv[1]

def link_url(link):
    url=requests.get(link)
    url_content=url.content
    url_soup=bs(url_content,"html.parser")
    return url_soup

def domain(link):
    domain=link.split("//")[-1].split("/")[0]
    return domain

def time():
    time=datetime.datetime.now().strftime("%d:%m:%Y %H:%M:%S")
    return time 

def title(link):
    url_soup=link_url(link)
    title=str(url_soup.title.get_text())
    return title

def urls(url_soup):
    urls=list(set([b for b in [a['href'] for a in url_soup.find_all('a', href=True) if a.text] if b.startswith('http')]))
    return urls 

if __name__ == "__main__":
    print("Link : ",link)
    print("Time :",time())
    print("Domain :", domain(link))
    print("Title :", title(link))
