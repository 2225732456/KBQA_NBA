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
import xlrd
class getDate:
    def __init__(self):
        self.url = []
        self.coach = []
        self.player = []
        self.base_url = 'http://www.stat-nba.com'
        self.team_list_dir = r'F:\11803990125刘澳\QuestionData\team.xls'
        self.team_list = []
        res = self.getFile()
        for i in range(0,len(res)):
            self.team_list.append(res[i][0])
    def getFile(self):
        lines = [] #一行内容
        workbook = xlrd.open_workbook(self.team_list_dir)  # 读xls文件
        xls_sheet = workbook.sheets()[0]  #第一个sheet
        for i in range(1,xls_sheet.nrows):  #按行读取内容
            lines.append(xls_sheet.row_values(i))
        return lines

    def insertOne(self,value, sheet):
        row = [value] * 3
        sheet.append(row)
    def getdate(self):
        for url in self.coach:
            print(url)
            team_list = {}
            res = requests.get(url)
            res.raise_for_status()
            res.encoding = res.apparent_encoding
            html = etree.HTML(res.text)
            try:
                #姓名
                name = html.xpath("//*[@id='background']/div[4]/div[2] /text()")[0]
                name = re.sub("[\s\t\n\r\xa0\u3000]", "",name)
            except IndexError as e:
                print("IndexError Details : " + str(e))
                pass
            try:
                content= html.xpath("//*[@class='row'] /text()")
                for i in range(0,len(content)):
                    content[i] = re.sub("[\s\t\n\r\xa0\u3000]", "",content[i])
                for i in range(0,len(self.team_list)):
                    for j in range(0,len(content)):
                        for k in range(0,len(content[j])):
                            if content[j][k:k + 2] == self.team_list[i]:
                                team_list.setdefault(self.team_list[i], []).append(content[j][k-5:k])
            except IndexError as e:
                print("IndexError Details : " + str(e))
                pass
            print(name,team_list)
            with open(r"F:\11803990125刘澳\QuestionData\playerAndteam.txt",'a',encoding='utf-8') as file:
                text = ''
                for cur in team_list:
                    temp = ''
                    for line in team_list[cur]:
                        temp = temp + line + ','
                    text =  text + cur + ':' + temp[:-1] + ';'
                text = name.split('/')[0] + ' ' + text
                file.write(text + '\n')
            file.close()

    def main(self):
        file_coach = open(r"F:\11803990125刘澳\QuestionData\playerurl.txt", encoding='utf-8')
        start_urls = file_coach.read().split('\n')
        self.coach = start_urls
        self.getdate()

myDate = getDate()
myDate.main()