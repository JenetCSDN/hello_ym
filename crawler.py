from bs4 import BeautifulSoup
from lxml import html
import xml
import requests

url = "https://movie.douban.com/chart"

f = requests.get(url)

soup = BeautifulSoup(f.content, "lxml")

for k in soup.find_all('div', class_="pl2"):
    a = k.find_all('span')
    print(a[0].string)