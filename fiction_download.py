# -*- coding:UTF-8 -*-

import requests

from bs4 import BeautifulSoup


if __name__ == '__main__':
    target = 'https://www.biqukan.com/1_1094/'         #'https://www.biqukan.com/1_1094/'
    req = requests.get(url=target)
    if req.encoding == 'ISO-8859-1':
        req.encoding = req.apparent_encoding

    html = req.text

    #print(html)
    bf = BeautifulSoup(html, 'lxml')

    #texts = bf.find_all('div', class_='showtxt')
    #print(texts)
    #print(texts[0].text.replace('\xa0'*8, ' '))


    div = bf.find_all('div', class_='listmain')

    a_bf = BeautifulSoup(str(div), 'lxml')
    a = a_bf.find_all('a')

    server = 'http://www.biqukan.com/'
    for each in a[13:]:
        print(each.string, server + each.get('href'))
