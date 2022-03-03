import requests
import os
import pickle
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
        self.base_url = 'http://www.stat-nba.com'
    def One_People_Honour(self):
        url = 'http://www.stat-nba.com/award/item3.html'
        response = requests.get(url)
        response.raise_for_status()
        response.apparent_encoding
        response.encoding = 'utf-8'
        html = response.text
        soup = BeautifulSoup(html, "html.parser")
        contents = []
        for tbody in soup.find_all('tbody'):
            for tr in tbody:
                if isinstance(tr, bs4.element.Tag):
                    tds = tr('td')
                    contents.append([tds[0].string, tds[1].find('a').string])
                    print(tds[0].string, tds[1].find('a').string)
        with open(r"F:\11803990125刘澳\QuestionData\honner\CMOY.txt",'a',encoding='utf-8') as file:
            for cur in contents:
                file.write(cur[0] + ' ' + cur[1] + '\n')
        file.close()
    def Champion(self):
        urls = "http://www.stat-nba.com/award/item12isnba1season"
        year = 1950
        end = '.html'
        dict = {}
        for year in range(1950,2020):
            url = urls + str(year) + end
            response = requests.get(url)
            response.raise_for_status()
            response.apparent_encoding
            response.encoding = 'utf-8'
            html = response.text
            soup = BeautifulSoup(html, "html.parser")
            for tbody in soup.find_all('tbody')[:-1]:
                for tr in tbody:
                    if isinstance(tr, bs4.element.Tag):
                        tds = tr('td')
                        name = tds[0]
                        print(name)
                        if name[0] and name[-1] == '☆':
                            name = name[1:-1]
                        dict.setdefault(name,[]).append(year)
        with open(r"F:\11803990125刘澳\QuestionData\honner\All_star.txt", 'a',encoding='utf-8') as fw:
            for cur in dict:
                text = cur + ' ' +','.join(dict[cur])
                print(text)
                #fw.write(text + '\n')
        fw.close()
    def getAllhonour(self):
        base_url = 'http://www.stat-nba.com/query_award.php?page='
        page = 1
        end = '&crtcol=i5&order=1#label_show_result'
        dict = {}
        for page in range(0,64):
            url = base_url + str(page) + end
            response = requests.get(url)
            response.raise_for_status()
            response.apparent_encoding
            response.encoding = 'utf-8'
            html = response.text
            soup = BeautifulSoup(html, "html.parser")
            for tbody in soup.find_all('tbody'):
                for tr in tbody:
                    temp = []
                    if isinstance(tr, bs4.element.Tag):
                        tds = tr('td')
                        name = tds[1].string
                        for td in tds[2:]:
                            if td.string == ' ':
                                temp.append(str(0))
                            else:
                                temp.append(td.string)
                        dict.setdefault(name,[]).append(temp)
        with open(r"F:\11803990125刘澳\QuestionData\honner\All_honour.txt", 'a', encoding='utf-8') as fw:
            for cur in dict:
                text = cur + ',' + ','.join(dict[cur][0])
                print(text)
                fw.write(text + '\n')
        fw.close()
myDate = getDate()
myDate.getAllhonour()