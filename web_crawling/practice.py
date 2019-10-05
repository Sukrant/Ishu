/usr/bin/pythonm
curl -s https://en.wikipedia.org/wiki/Main_Page| sed -n 's/.*href="\([^"]*\).*/\1/p'| grep ^http| sort -u
>>> import requests
>>> from bs4 import BeautifulSoup as bs
>>> url=requests.get("http://www.google.com")
>>> url.status_code
200
>>> url_content=url.content
>>> type(url_content)
<type 'str'>
>>> url_soup = bs(url_content)
>>> type(url_soup)
<class 'bs4.BeautifulSoup'>
>>> samples=url_soup.find_all("a", "item-title")
>>> samples[0]
/usr/bin/pythonm
curl -s https://en.wikipedia.org/wiki/Main_Page| sed -n 's/.*href="\([^"]*\).*/\1/p'| grep ^http| sort -u
>>> import requests
>>> from bs4 import BeautifulSoup as bs
>>> url=requests.get("http://www.google.com")
>>> url.status_code
200
>>> url_content=url.content
>>> type(url_content)
<type 'str'>
>>> url_soup = bs(url_content)
>>> type(url_soup)
<class 'bs4.BeautifulSoup'>
>>> samples=url_soup.find_all("a", "item-title")
>>> samples[0]
ssirohi@ssirohilinux:~/Videos/770/29951/296/Python/web_crawling$ 
/usr/bin/pythonm
curl -s https://en.wikipedia.org/wiki/Main_Page| sed -n 's/.*href="\([^"]*\).*/\1/p'| grep ^http| sort -u
MySQL [mysql]> create user 'crawler'@'localhost' identified by 'geekpills';
Query OK, 0 rows affected (0.04 sec)
MySQL [mysql]> grant all privileges on web_crawling.* to 'geekpills'@'localhost';
ERROR 1133 (42000): Unknown error 1133
MySQL [mysql]> grant all privileges on web_crawling.* to 'crawler'@'localhost';
Query OK, 0 rows affected (0.03 sec)
MySQL [web_crawling]> create table crawler ( link text not null, title varchar(255), domain varchar(255) not null, md5sum text not null, date DATE not null, number_links smallint,  number_internal_links smallint, number_external_links smallint) ; 
Query OK, 0 rows affected (0.28 sec)
>>> import requests
>>> from bs4 import BeautifulSoup as bs
>>> url=requests.get("http://www.google.com")
>>> url_content=url.content
>>> url_soup = bs(url_content)
>>> link='https://dba.stackexchange.com/questions/43119/mysql-set-my-cnf-location-at-server-start'
>>> url=requests.get(link)
*****domain=link.split("//")[-1].split("/")[0]
*****IPs=socket.gethostbyname_ex(domain)[-1]
socket.gethostbyname(list(set([b for b in [a['href'] for a in url_soup.find_all('a', href=True) if a.text] if b.startswith('http')]))[7].split("//")[-1])
*****title=str(url_soup.title.get_text())
*****time=datetime.datetime.now().strftime("%d:%m:%Y %H:%M:%S")
*****urls=list(set([b for b in [a['href'] for a in url_soup.find_all('a', href=True) if a.text] if b.startswith('http')]))

