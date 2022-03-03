#创建知识图谱
from py2neo import Graph, Node, Relationship
import pandas as pd
import re
import os
import xlrd
from xlrd import open_workbook
import xlwt
import datetime
class BasketballGraph(object):
    def __init__(self):
        # 根据运行的函数选择对应的数据文件
        self.data_dir = r'F:\bishe\att\data\player.txt'
        # self.data_dir = r'F:\bishe\att\data_1\playerdate.xlsx'   #球员信息csv
        # self.data_dir = r'F:\11803990125刘澳\QuestionData\team.xls'  #球队信息csv
        # self.data_dir = r'F:\11803990125刘澳\QuestionData\coachdate.xlsx'  #教练数据csv
        # self.data_dir = r'F:\11803990125刘澳\QuestionData\coachAndteamList.xlsx'    #教练和球队关系的csv
        # self.data_dir = r'F:\11803990125刘澳\QuestionData\playerAndteamList.xlsx'   #球员和球队关系的csv
        # self.data_dir = r'F:\11803990125刘澳\QuestionData\honner\MingRenTang.txt'
        self.graph = Graph("http://localhost:7474", username="neo4j", password="neo4j")  # neo4j

    def getFile(self):
        lines = [] #一行内容
        # workbook = xlrd.open_workbook(self.data_dir)  # 读xls文件
        # xls_sheet = workbook.sheets()[0]  #第一个sheet
        # for i in range(1,xls_sheet.nrows):  #按行读取内容
        #     lines.append(xls_sheet.row_values(i))
        lines = open(self.data_dir,encoding='utf-8').read().split('\n')  #读txt类型的数据文件
        print(lines)
        return lines

    def creat_node_league(self):   #创建league结点
        node = Node("league",name='NBA')
        print(node)
        self.graph.create(node)
        return None

    def creat_node_team(self,lines):   #创建球队结点
        count = 0
        nodes = []
        for line in lines:
            nodes.append(line[0])
        print(nodes)
        for node_name in nodes:
            node = Node("team",name=node_name)
            self.graph.create(node)
            count += 1
            print(count,len(nodes))
        return

    def create_node_player(self, nodes):   #创建球员结点
        count = 0
        for node_name in nodes:
            if "'" in node_name:
                node_name = node_name.replace("'","")
            node = Node('Player', name=node_name)
            print(node)
            print(self.graph)
            self.graph.create(node)
            count += 1
            print(count, len(nodes))
        return

    def create_node_coach(self, lines):  # 创建教练结点
        count = 0
        nodes = []
        for line in lines:
            nodes.append(line[0].split('/')[0])
        print(nodes)
        for node_name in nodes:
            node = Node("coach", name=node_name)
            self.graph.create(node)
            count += 1
            print(count, len(nodes))
        return

    def create_relationship_teamAndleague(self, lines):
        count = 0
        edges = []
        for line in lines:
            team_name = line[0].split('/')[0]
            edges.append(team_name)
        for edge in edges:
            q = edge
            query = "match (n:team{name:'%s'}),(m:league{name:'NBA'}) create (n)-[r:加入]->(m)" % (q)
            try:
                self.graph.run(query)
                count += 1
            except Exception as e:
                print(e)
        print(edges)
        return

    def create_relationship_teamAndplayer(self, edges):
        count = 0
        for edge in edges:
            name = edge[0]
            if "'" in name:
                name = name.replace("'","")
            Lists = edge[1].split(';')
            times ,teams = [],[]
            for cur in Lists:
                if len(cur.split(':')) >= 2:
                    teams.append(cur.split(':')[0])
                    times.append(cur.split(':')[1])
            for i in range(0,len(times)):
                team = teams[i] + '队'
                time = times[i]
                query = "match (n:player{name:'%s'}),(m:team{name:'%s'}) create (n)-[r:签约]->(m)" % (
                    name,team)
                print(name,team)
                try:
                    self.graph.run(query)
                    count += 1
                except Exception as e:
                    print(e)
        return

    def create_relationship_teamAndcoach(self, edges):
        count = 0
        for edge in edges:
            name = edge[0]
            if "'" in name:
                name = name.replace("'","")
            ttList = edge[1].split(";")
            teams = []
            for tt in ttList:
                if tt.split(':')[0] not in teams:
                    teams.append(tt.split(':')[0])
            for team in teams:
                if len(team) != 0 and team != '不详':
                    team = team + '队'
                    query = "match (n:coach{name:'%s'}),(m:team{name:'%s'}) create (n)-[r:执教]->(m)" % (
                    name,team)
                    print(name,team)
                    try:
                        self.graph.run(query)
                        count += 1
                        print(count)
                    except Exception as e:
                        print(e)
        return

    def add_node_player(self,lines):   # 球员属性添加
        for edge in lines:
            name = edge[0].split('/')[0]  #球员名字
            player_pos = edge[1] #球场位置
            height = edge[2] #身高
            weight = edge[3] #体重
            birthday = edge[4] #出生日期
            if type(birthday) is not str:
                delta = datetime.timedelta(days=birthday)
                birthday = str((datetime.datetime.strptime('1899-12-30', '%Y-%m-%d') + delta)).split(' ')[0]

            birthplace = edge[5] #出生地
            player_num = edge[6] #球衣号码
            if type(player_num) is float:
                player_num = str(int(player_num))
            select_des = edge[7] #选秀情况
            contract = edge[8] #薪水
            query = "match (n:player{name:'%s'}) set n = {name:'%s',player_pos:'%s',height:'%s',weight:'%s',birthday:'%s',birthplace:'%s',player_num:'%s',select_des:'%s',contract:'%s'}" % \
                    (name,name,player_pos,height,weight,birthday,birthplace,player_num,select_des,contract)
            try:
                self.graph.run(query)
            except Exception as e:
                print(e)
    def add_node_coach(self,lines):   # 球员属性添加
        for edge in lines:
            name = edge[0].split('/')[0]
            if "'" in name:
                name = name.replace("'","")
            birthday = edge[1]
            birthplace = edge[2]
            career = edge[3]
            normalGame = edge[4]
            playoff = edge[5]
            final = edge[6]
            champion = edge[7]
            if type(birthday) is not str:
                delta = datetime.timedelta(days=birthday)
                birthday = str((datetime.datetime.strptime('1899-12-30', '%Y-%m-%d') + delta)).split(' ')[0]
            print(name,name,birthday,birthplace,career,normalGame,playoff,final,champion)
            query = "match (n:coach{name:'%s'}) set n = {name:'%s',birthday:'%s',birthplace:'%s',career:'%s',normalGame:'%s',playoff:'%s',final:'%s',champion:'%s'}" % \
                    (name,name,birthday,birthplace,career,normalGame,playoff,final,champion)
            try:
                self.graph.run(query)
            except Exception as e:
                print(e)

    def add_node_team(self,lines):   # 球队属性添加
        for edge in lines:
            name = edge[0] + '队'
            position = edge[1]
            introduce = edge[3]
            query = "match (n:team{name:'%s'}) set n = {name:'%s',team_position:'%s',team_introduce:'%s'}" % (name,name,position,introduce)
            print(name,position,introduce)
            try:
                self.graph.run(query)
            except Exception as e:
                print(e)

    def add_relationship_teamAndleague(self,lines):  #添加关系属性
        for edge in lines:
            team_name = edge[0]
            add_time = edge[2]
            query = "match r=(n:team{name:'%s'})-[p:加入]->(m:league{name:'NBA'}) set p.add_time='%s'" % (team_name,add_time)   #球队加入联盟
            print(team_name,add_time)
            try:
                self.graph.run(query)
            except Exception as e:
                print(e)
    def add_relationship_teamAndplayer(self,edges):  #添加关系属性
        count = 0
        for edge in edges:
            name = edge[0]
            if "'" in name:
                name = name.replace("'", "")
            Lists = edge[1].split(';')
            times, teams = [], []
            for cur in Lists:
                if len(cur.split(':')) >= 2:
                    teams.append(cur.split(':')[0])
                    times.append(cur.split(':')[1])
            for i in range(0, len(times)):
                team = teams[i] + '队'
                time = times[i]
                query = "match r=(n:player{name:'%s'})-[p:签约]->(m:team{name:'%s'}) set p.playTime='%s'" % (name,team,time)   #签约时间
                print(name,team,time)
                try:
                    self.graph.run(query)
                except Exception as e:
                    print(e)

    def add_relationship_teamAndcoach(self,lines):  #添加关系属性
        for edge in lines:
            name = edge[0]
            if "'" in name:
                name = name.replace("'","")
            teamList = edge[1].split(';')
            times ,teams= [],[]
            for cur in teamList:
                if len(cur.split(':')) >= 2:
                    times.append(cur.split(':')[1])
                    teams.append(cur.split(':')[0])
            for i in range(0,len(times)):
                team = teams[i] + '队'
                teachTime = times[i]
                print(name,team,teachTime)
                query = "match r=(n:coach{name:'%s'})-[p:执教]->(m:team{name:'%s'}) set p.teachTime='%s'" % (name,team,teachTime)   #签约合同
                try:
                    self.graph.run(query)
                except Exception as e:
                    print(e)
    def creat_node_honour(self):
        lines = ["MVP","FMVP","DPOY","ROY","SMOY","MIP","AMVP","COY","名人堂","总冠军"]
        # for line in lines:
        #     node = Node("honour", name=line)
        #     self.graph.create(node)
        return

    def creat_relationship_honourAndleague(self):
        lines = ["MVP", "FMVP", "DPOY", "ROY", "SMOY", "MIP", "AMVP", "COY", "名人堂", "总冠军"]
        for honour in lines:
            query = "match (n:league{name:'NBA'}),(m:honour{name:'%s'}) create (n)-[r:设立]->(m)" % (
                honour)
            try:
                self.graph.run(query)
            except Exception as e:
                print(e)

    def creat_relationship_playerAndhonour(self,lines):
        dict = {}
        for edge in lines:
            name = edge.split(' ')[1]
            time = edge.split(' ')[0]
            dict.setdefault(name,[]).append(time)
            #创建关系
        for cur in dict:
            name = cur
            time = ','.join(dict[cur])
            query = "match (n:player{name:'%s'}),(m:honour{name:'名人堂'}) create (n)-[r:获得]->(m)" % (
                name)
            print(name,time)
            try:
                self.graph.run(query)
            except Exception as e:
                print(e)
            #设置属性
            query = "match r=(n:player{name:'%s'})-[p:获得]->(m:honour{name:'名人堂'}) set p.getTime='%s'" % (
            name, time)  # 签约合同
            print(name,time)
            try:
                self.graph.run(query)
            except Exception as e:
                print(e)
if __name__ == '__main__':
    Mysystem = BasketballGraph()
    lines = Mysystem.getFile()

    # Mysystem.creat_node_league()  #创建league结点
    # Mysystem.create_node_coach(lines)   #创建教练结点
    # Mysystem.creat_node_team(lines)   #创建球队结点
    Mysystem.create_node_player(lines)   #创建球员结点
    # Mysystem.creat_node_honour()  #创建荣誉结点

    # Mysystem.create_relationship_teamAndleague(lines)  #创建nba和球队关系
    # Mysystem.create_relationship_teamAndplayer(lines)  #创建球队和球员关系
    # Mysystem.create_relationship_teamAndcoach(lines)   #创建球队和教练关系
    # Mysystem.add_node_player(lines)  #为球员添加属性
    # Mysystem.add_node_coach(lines)  #添加教练属性
    # Mysystem.add_node_team(lines)    #添加球队属性
    # Mysystem.add_relationship_teamAndleague(lines)  #添加加入关系的属性
    # Mysystem.add_relationship_teamAndcoach(lines)  #添加执教关系的属性
    # Mysystem.add_relationship_teamAndplayer(lines)   #添加球员签约球队关系的属性

    # Mysystem.creat_relationship_playerAndhonour(lines)  #创建球员获得荣誉关系
    # Mysystem.creat_relationship_honourAndleague()   #创建联盟设立荣誉关系