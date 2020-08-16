#!/data/conda/bin/python

import requests
from bs4 import BeautifulSoup as bs
import mysql.connector 
from  mysql.connector import Error
import socket, hashlib, sys, datetime

urls=[]
link = sys.argv[1]

class Crawling:
    """This class is used to get data from any url 
    save it in database and further use its 
    data to get more link to study and save in database"""
    
    def my_conn(self):
        # MySQL connection
        try:
            myconnection = mysql.connector.connect(
            database = 'crawler',
            host = 'localhost',
            user = 'crawler',
            password = 'passw0rd')
        except mysql.connector.Error as error:
            print(f"Failed to insert into MySQL table .. Exiting ... {error}")
            sys.exit(1)

    # get mdsum of url
    def Mdsum(self,link):
        return hashlib.md5(link.encode('utf-8')).hexdigest()

    # Delete first row of tmp_site table
    def del_first_row(self):
        cursor = myconnection.cursor()
        cursor.execute("delete from tmp_site limit 1")
        cursor.close()

    # Get url Data 
    def link_url(self,link):
        url=requests.get(link)
        url_content=url.content
        url_soup=bs(url_content,"html.parser")
        return url_soup

    # Get url Domain
    def Domain(self,link):
        domain=link.split("//")[-1].split("/")[0]
        return domain

    # Get Url Title
    def Title(self,link):
        url_soup=link_url(link)
        title=str(url_soup.title.get_text())
        return title

    # Get Other urls in link
    def urls_list(self,link):
        global urls
        url_soup=link_url(link)
        new_urls=list(set([b for b in [a['href'] for a in url_soup.find_all('a', href=True) if a.text] if b.startswith('http')]))
        urls=list(set(urls+new_urls))
        return urls

    # Domain IP
    def Domain_ip(self,domain):
        return socket.gethostbyname(domain)

    # Insert Link data in site_data table (main table)
    def link_data(self,link):
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

        # Main logic start here 
    def __init__(self,link):
        self.link=link
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
    pass
