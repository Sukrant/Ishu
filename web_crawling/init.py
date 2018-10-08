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
