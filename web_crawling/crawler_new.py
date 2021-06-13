#!/data/conda/bin/python

import requests
from bs4 import BeautifulSoup as bs
import mysql.connector 
from  mysql.connector import Error
import socket, hashlib, sys, datetime

urls=[]
if len(sys.argv) != 2:
    print(f"""You didn't provide URL to work On  
    ./crawler_new.py google.com""")
    sys.exit()
link = sys.argv[1]


import requests
from bs4 import BeautifulSoup as bs
import mysql.connector
from  mysql.connector import Error
import socket, hashlib, sys, datetime
class Crawling:
    """ Doc for Crawling class """
    
    def __init__(self,link):
        self.link = link
        self.domain=self.link.split("//")[-1].split("/")[0]
        self.domain_ip=socket.gethostbyname(self.domain)
        self.title=self.Title()
        self.url_list=self.urls_list()
    # Get url Data
    def link_url(self):
        url=requests.get(self.link)
        url_content=url.content
        url_soup=bs(url_content,"html.parser")
        return url_soup
    # Get Url Title
    def Title(self):
        url_soup=self.link_url()
        title=str(url_soup.title.get_text())
        return title
    # Get Other urls in link
    def urls_list(self):
	    urls=[]
	    url_soup=self.link_url()
	    if url_soup:
	        new_urls=list(set([b for b in [a['href'] for a in url_soup.find_all('a', href=True) if a.text] if b.startswith('http') and not b.startswith('https://download') and not b.startswith('https://download')]))
	        urls=list(set(urls+new_urls))
	        return urls
	    else:
	        return None

    def my_conn(self):
        # MySQL connection
        try:
            myconnection = mysql.connector.connect(
            database = 'crawler',
            host = 'localhost',
            user = 'crawler',
            password = 'Astgjdous_12')
        except mysql.connector.Error as error:
            print(f"Failed to insert into MySQL table .. Exiting ... {error}")
            sys.exit(1)

    # get mdsum of url
    def Mdsum(self,link):
        return hashlib.md5(link.encode('utf-8')).hexdigest()

    # Delete first row of tmp_site table
    def del_first_row(self):
        myconnection = my_conn()
        cursor = myconnection.cursor()
        cursor.execute("delete from tmp_site limit 1")
        cursor.close()

    # Insert Link data in site_data table (main table)
    def link_data(self,link):
        myconnection = my_conn()
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
            urls_query(urls,link)
        except mysql.connector.Error as error:
            print(" Because of MySQL insert error. Exit...",error)
            sys.exit(2)
        finally:
            cursor.close()

    # Insert Url list data in tmp_site
    def urls_query(self,urls,link):
        myconnection = my_conn()
        for url in urls:
            mdsum=Mdsum(url)
            try:
                cursor = myconnection.cursor()
                link_query = """ insert into tmp_site (site,parent_link,mdsum) values (%s, %s, %s) """
                cursor.execute(link_query,(url,link,mdsum))
                myconnection.commit()
                print("Insert values for Link :", link)
            except mysql.connector.Error as error:
                print(" Because of MySQL insert error...",error)
            finally:
                cursor.close()
    def start(self,link):
        myconnection = my_conn()
        if self.link:
            link_data(link)
        else:
            try:
                cursor = myconnection.cursor()
                cursor.execute("select site from tmp_site limit 1")
                link=cursor.fetchall()[0]
                print(link," :    Going to process is")
                print("Deleteing ---- ",link)
                del_first_row()
                link_data(link)
            except mysql.connector.Error as error:
                print(" Because of MySQL insert error...",error)
            finally:
                cursor.close()

if __name__=='__main__':
    link = Crawling(link)
