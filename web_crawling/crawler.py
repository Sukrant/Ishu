#!/usr/bin/python3.5 

import requests
from bs4 import BeautifulSoup as bs
import mysql.connector 
from  mysql.connector import Error
import socket, hashlib, sys, datetime


urls=[]
# First variables
link = sys.argv[1]

# MySQL connection
try:
    myconnection = mysql.connector.connect(
        database = 'crawler',
        host = 'localhost',
        user = 'crawler',
        password = 'passw0rd')
except mysql.connector.Error as error:
        print("Failed to insert into MySQL table .. Exiting ... {}".format(error))
        sys.exit(1)

# get mdsum of url
def Mdsum(link):
    return hashlib.md5(link.encode('utf-8')).hexdigest()

# Get url Data 
def link_url(link):
    url=requests.get(link)
    url_content=url.content
    url_soup=bs(url_content,"html.parser")
    return url_soup

# Get url Domain
def Domain(link):
    domain=link.split("//")[-1].split("/")[0]
    return domain

# Get Url Title
def Title(link):
    url_soup=link_url(link)
    title=str(url_soup.title.get_text())
    return title

# Get Other urls in link
def urls_list(link):
    global urls
    url_soup=link_url(link)
    new_urls=list(set([b for b in [a['href'] for a in url_soup.find_all('a', href=True) if a.text] if b.startswith('http')]))
    urls=list(set(urls+new_urls))
    return urls

# Domain IP
def Domain_ip(domain):
    return socket.gethostbyname(domain)

# Insert Link data in site_data
def link_data(link):
    domain=Domain(link)
    title=Title(link)
    ip=Domain_ip(domain)
    try:
        cursor = myconnection.cursor()
        link_query = """ insert into site_data (link,domain,title) values (%s, %s, %s) """
        cursor.execute(link_query,(link,domain,title))
        myconnection.commit()
        print("Insert values for Link :", link)
        urls=urls_list(link) 
        print(len(urls))
    except mysql.connector.Error as error:
        print(" Because of MySQL insert error. Exit...")
        sys.exit(2)
    finally:
        cursor.close()

# Insert Url list data in tmp_site
def urls_query(urls,link):
    for url in urls:
        mdsum=Mdsum(url)
        try:
            cursor = myconnection.cursor()
            link_query = """ insert into tmp_site (site,parent_link,mdsum) values (%s, %s, %s) """
            cursor.execute(link_query,(url,link,mdsum))
            myconnection.commit()
            print("Insert values for Link :", link)
        except mysql.connector.Error as error:
            print(" Because of MySQL insert error. Exit...")
            sys.exit(3)
        finally:
            cursor.close()

# Main logic start here 
if __name__ == "__main__":
    link_data(link)
    urls_query(urls,link)
