import requests
import os
import re
from bs4 import BeautifulSoup
import bs4
import urllib.request
from lxml import etree
import xlwt
import pandas as pd
from openpyxl import Workbook
class getDate:
    def __init__(self):
        self.url = []
        self.coach = []
        self.player = []
        self.base_url = 'http://www.stat-nba.com'

    def insertOne(self,value, sheet):
        row = [value] * 3
        sheet.append(row)
    def getdate(self):
        for url in self.coach:
            print(url)
            res = requests.get(url)
            res.raise_for_status()
            res.encoding = res.apparent_encoding
            html = etree.HTML(res.text)
            dict = {'姓名':'无','全名:':'无','位置:':'无','身高:':'无','体重:':'无','出生日期:':'无','出生城市:':'无','球衣号码:':'无','选秀情况:':'无','当前薪金:':'无'}
            try:
                #姓名
                name = html.xpath("//*[@id='background']/div[4]/div[2] /text()",)[0]
                dict['姓名'] = re.sub("[\s\t\n]", "", name)
            except IndexError as e:
                print("IndexError Details : " + str(e))
                pass
            try:
                #全名
                for i in range(1,1):
                    all_name = re.sub("[\s\t\n\r\xa0\u3000]", "",html.xpath("//*[@id='background']/div[4]/div[3]/div[%d]/div/text()" % i)[0])
                    if all_name in dict:
                        dict[all_name] = re.sub("[\s\t\n\r\xa0\u3000]", "",html.xpath("//*[@id='background']/div[4]/div[3]/div[%d]/text()" % i)[0])
            except IndexError as e:
                print("IndexError Details : " + str(e))
                pass
            if dict['选秀情况:'][-1] == "被":
                dict['选秀情况:'] = dict['选秀情况:'] + '选中'
            print(dict)
            # with open(r"F:\bishe\att\data_1\player.txt",'a',encoding='utf-8') as file:
            #     content = ''
            #     for cur in dict:
            #         content += dict[cur] + ' '
            #     file.write(content + '\n')
            # file.close()
    def get_urls(self,url):
        res = requests.get(url)
        res.raise_for_status()
        res.encoding = res.apparent_encoding
        html = res.text
        soup = BeautifulSoup(html, "html.parser")

        for div in soup.find_all('div',{'class','playerList'}):
            for a in div:
                if isinstance(a, bs4.element.Tag):
                    url = a.find('a')['href']
                    if url.split("/")[1] == 'coach':
                        self.coach.append(self.base_url+url[1:])
                    elif url.split("/")[1] == 'player':
                        self.player.append(self.base_url + url[1:])
        return url

    def main(self):
        file_coach = open(r"F:\bishe\att\data_1\playerurl.txt", encoding='utf-8')
        start_urls = file_coach.read().split('\n')
        self.coach = start_urls
        self.getdate()

myDate = getDate()
myDate.main()