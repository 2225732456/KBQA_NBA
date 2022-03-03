import requests
import os
import re
from bs4 import BeautifulSoup
import bs4
import urllib.request
class getGameDate:
    def __init__(self):
        self.url = []
        self.coach = []
        self.player = []
    def getSchedule(self,url):
        global flag
        gameDate = []
        url = "https://nba.hupu.com" + url
        count = True

        res = requests.get(url)
        res.raise_for_status()
        res.encoding = res.apparent_encoding
        html = res.text
        soup = BeautifulSoup(html, "html.parser")

        for tr in soup.find("tbody").children:
            if isinstance(tr, bs4.element.Tag):
                tds = tr('td')
                if len(tds) == 1:
                    time = tds[0].string  #比赛日期
                    time = time.split(u'\xa0')[0]
                    count = False
                else:
                    if count == False:
                        teams = tds[1].find_all("a")
                        team_one = teams[0].string
                        teams_two = teams[1].string
                        text = team_one + "VS" + teams_two

                        dateUrl = tds[2].find('a')['href']
                        self.url.append(dateUrl)
                    count = False

        for temp in soup.find_all('div', {'class', 'a'}):
            url = temp("b")[1].find('a')['href']
            break
        return url,gameDate

    def main(self):
        global flag
        gameDates = []  #二元数组
        url = "/schedule/2020-12-23"  #起始日期（起始网页）
        while True:
            url,gameDate = self.getSchedule(url)
            gameDates.append(gameDate)
            if url == "/schedule/2021-03-03":
                break
