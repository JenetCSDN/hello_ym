# -*- coding:UTF-8 -*-
'''
header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
        }

'''
# -*- coding:UTF-8 -*-
# https://price.pcauto.com.cn/cars/nb16/
# https://price.pcauto.com.cn/cars/sg23445/    具体
# https://price.pcauto.com.cn/cars/sg14102-o1-1/
# https://price.pcauto.com.cn/cars/sg23445-o1-1/


from contextlib import closing
import requests
from bs4 import BeautifulSoup
import re

# 太平洋汽车
class downloader_series(object):

    def __init__(self):
        self.server = 'https://price.pcauto.com.cn'
        #self.target = 'https://price.pcauto.com.cn/cars/nb16/'  东南
        #self.target = 'https://price.pcauto.com.cn/cars/nb34/'  现代
        self.target = 'https://price.pcauto.com.cn/cars/nb3/'
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
        }

        self.series = []
        self.series_urls = []
        self.series_nums = 0

        self.pic_page_url = []
        self.pic_urls = []
        self.pic_years = []

    # series_url
    def get_series_url(self):
        #req = requests.get(self.target)
        req = requests.get(self.target, params={'uid': '484t24oz', 'num': '6', 'encode': 'gbk', 'type': 'pn'},
                           headers=self.header, timeout=0.5)
        req.encoding = req.apparent_encoding
        html = req.text
        # 车系列
        div_bf = BeautifulSoup(html, 'lxml')
        div = div_bf.find_all('div', class_='tb')
        print('len', len(div))
        #for i in range(len(div) - 1):
            #print(i)
        a_bf = BeautifulSoup(str(div[1]), 'lxml')
        a = a_bf.find_all('a', class_='')

        self.series_nums = len(a)
        #现代self.series_nums = 33
        cnt = 0
        for each in a:
            cnt += 1
            str1 = str(each.p)
            self.series.append(str1.split('"')[1])
            self.series_urls.append(self.server + each.get('href')[:-1] + '-o1-1/')
            # print(self.server + each.get('href')[:-1] + '-o1-1/')
        print(cnt)

    def get_page(self):
        for url in self.series_urls:
            page = []
            req = requests.get(url)
            req.encoding = req.apparent_encoding
            html = req.text
            div_bf = BeautifulSoup(html, 'html.parser')
            div = div_bf.find_all('div', class_='pcauto_page')
            div_a_bf = BeautifulSoup(str(div), 'html.parser')
            a = div_a_bf.find_all('a')
            page.append(url)
            num_page = 0
            if (len(a)):
                num_page = int(str(a).split('</a>, <a')[-2].split('>')[1])
                print(num_page)
            for i in range(2, num_page+1):
                page.append(url + 'p%d.html' % i)
            self.pic_page_url.append(page)

    def get_download_url(self):
        # 获取各个系列中的每一辆车的src
        for i in range(self.series_nums):
            year = []
            pic = []
            vmt = 0
            vnt = 0
            for pic_url in self.pic_page_url[i]:
                req = requests.get(url=pic_url)
                req.encoding = req.apparent_encoding
                html = req.text
                div_bf = BeautifulSoup(html, 'html.parser')
                div = div_bf.find_all('ul', class_='ulPic clearfix')
                div_a_bf = BeautifulSoup(str(div), 'html.parser')

                # 获取车辆的年份
                p = div_a_bf.find_all('a', target='_blank')
                for each in p:
                    vmt += 1
                    str1 = str(each.p)
                    if (str1 == 'None'):
                        str1 = 'a'
                    else:
                        str1 = str1.split('"')[1].split('款')[0]
                    year.append(str1)
                    if (vmt == 600):
                        break

                #获取图片url
                a = div_a_bf.find_all('a', target='_blank')
                for each in a:
                    vnt += 1
                    src = 'https://price.pcauto.com.cn' + each.get('href')
                    #src = each.find('img').attrs['#src']
                    src = self.get_big_pic(src)
                    pic.append(src)
                    if (vnt == 600):
                        break

            self.pic_years.append(year)
            self.pic_urls.append(pic)

            #print(self.pic_urls)
            print('vmt:', vmt)
            print('vnt:', vnt)

    def get_big_pic(self, url):
        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
        }
        req = requests.get(url)
        req.encoding = req.apparent_encoding
        pattern = re.compile(".*picurl02='.*?'")
        data = re.findall(pattern, req.text)
        src = 'http:' + data[0].split("'")[1]
        return src

    def pic_download(self, i, j, url):
        with closing(requests.get(url)) as r:
            filename = './picture4/' + '本田_' + self.series[i] + '_' + self.pic_years[i][j] + '_'
            with open(filename + '%d.jpg' % j, 'ab+') as f:
                for chunk in r.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
                        f.flush()

if __name__ == '__main__':
    dl = downloader_series()
    dl.get_series_url()
    dl.get_page()

    dl.get_download_url()

    for i in range(dl.series_nums):
        j = 0
        for each in dl.pic_urls[i]:
            #print(each)
            dl.pic_download(i, j, each)
            j += 1

