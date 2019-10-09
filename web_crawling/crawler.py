#!/usr/bin/python3.5 

import requests
from bs4 import BeautifulSoup as bs
import datetime
import mysql.connector 
from  mysql.connector import Error
import sys

try:
    myconnection = mysql.connector.connect(
        database = 'crawler',
        host = 'localhost',
        user = 'crawler',
        password = 'passw0rd')
except mysql.connector.Error as error:
        print("Failed to insert into MySQL table .. Exiting ... {}".format(error))
        sys.exit(1)

link = sys.argv[1]

def link_url(link):
    url=requests.get(link)
    url_content=url.content
    url_soup=bs(url_content,"html.parser")
    return url_soup

def domain(link):
    domain=link.split("//")[-1].split("/")[0]
    return domain

def title(link):
    url_soup=link_url(link)
    title=str(url_soup.title.get_text())
    return title

def urls(url_soup):
    url_soup=link_url(link)
    urls=list(set([b for b in [a['href'] for a in url_soup.find_all('a', href=True) if a.text] if b.startswith('http')]))
    return urls 

def link_data(link):
    Domain=domain(link)
    Title=title(link)
    try:
        cursor = myconnection.cursor()
        link_query = """ insert into site_data (link,Domain,Title) values (%s, %s, %s) """
        cursor.execute(link_query,(link,Domain,Title))
        myconnection.commit()
        print("Insert values for Link :", link)
    except mysql.connector.Error as error:
        print(" Because of MySQL insert error. Exit...")
        sys.exit(2)
    finally:
        cursor.close()

if __name__ == "__main__":
    link_data(link)
