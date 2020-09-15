#!/data/conda/bin/python

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
        password = 'Astgjdous_12')
except mysql.connector.Error as error:
        print("Failed to insert into MySQL table .. Exiting ... {}".format(error))
        sys.exit(1)


# get mdsum of url
def Mdsum(link):
    return hashlib.md5(link.encode('utf-8')).hexdigest()


# Dlete first row of tmp_site table
def del_first_row():
    cursor = myconnection.cursor()
    cursor.execute("delete from tmp_site limit 1")
    cursor.close()


# Get url Data 
def link_url(link):
    try:
        url=requests.get(link,timeout=3)
        if url:
            url_content=url.content
            url_soup=bs(url_content,"html.parser")
            return url_soup
    except Exception as e:
        print(f"Unable to connect {link}")
    work_url()    
        


# Get url Domain
def Domain(link):
    if not isinstance(link,str):
        link = str(link)
    domain = link.split("//")[-1].split("/")[0]
    return domain


# Get Url Title
def link_title(link):
    url_soup=link_url(link)
    if url_soup:
        title_text = url_soup.title
        if not title_text:
            title = "No title"
        else:
            title=str(url_soup.title.get_text())   
        return title
    else:
        title = "No title"


# Get Other urls in link
def urls_list(link):
    global urls
    url_soup=link_url(link)
    if url_soup:
        new_urls=list(set([b for b in [a['href'] for a in url_soup.find_all('a', href=True) if a.text] if b.startswith('http') and not b.startswith('https://download') and not b.startswith('https://download')]))
        urls=list(set(urls+new_urls))
        return urls
    else:
        return None


# Domain IP
def Domain_ip(domain):
    return socket.gethostbyname(domain)


# Work on temp table
def work_url():
    try:
        cursor = myconnection.cursor()
        cursor.execute("select site from tmp_site limit 1")
        link=cursor.fetchall()[0][0]
        print(link," :    Going to process is")
        print("Deleteing ---- ",link)
        del_first_row()
        link_data(link)
    except mysql.connector.Error as error:
        print(" Because of MySQL insert error...",error)
    finally:
        cursor.close()


# Insert Link data in site_data
def link_data(link):
    domain=Domain(link)
    title=link_title(link)
    pAddress=Domain_ip(domain)
    if link.startswith('https://download') and link.startswith('http://download'):
        pass 
    urls = urls_list(link)
    number_of_urls = len(urls)    
#    print(f'{link}-{domain}-{title}-{ip}-{number_of_urls}')
    try:
        cursor = myconnection.cursor()
        link_query = """ insert into site_data (link,domain,title,IpAddress,number_of_urls) values (%s, %s, %s, %s, %s) """
        print(link_query)
        cursor.execute(link_query,(link,domain,title))
        myconnection.commit()
        print("Insert values for Link :", link)
#        if link.startswith('https://download') and link.startswith('http://download'):
#            pass
#        urls=urls_list(link)
#        if urls:
#            print(len(urls))
#            urls_query(urls,link)
#        work_url()
        if urls:
            print(len(urls))
            urls_query(urls)
        work_url()
    except mysql.connector.Error as error:
        print(" Because of MySQL insert error. Exit...",error)
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
            print("Insert values for Link :", url)
        except mysql.connector.Error as error:
            print(" Because of MySQL insert error...",error)
        finally:
            cursor.close()

# Main logic start here 
if __name__ == "__main__":
   link_data(link)
