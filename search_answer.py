from py2neo import Graph
class AnswerSearching:
    def __init__(self):
        self.graph = Graph("http://localhost:7474", username="neo4j", password="neo4j")
        self.top_num = 10

    def data_recognize(self,data):
        if data['intentions'] == ['add_time']:
            if 'Player' in data.keys():
                del data["Player"]
            if 'Coach' in data.keys():
                del data["Coach"]
        elif 'Player' in data.keys() and 'Coach' in data.keys():
            del data["Player"]
        return data

    def type_search(self,date):
        count = 0
        flag = False
        for cur in date.keys():
             if cur == 'Player' or cur == 'Coach' or cur == 'Team' or cur == "Honour":
                count += 1
             if cur == 'Honour':
                 flag = True
        if count > 1 and flag:
            return "hon_mul"
        elif count > 1 and not flag:
            return "nor_mul"
        elif count == 1:
            return 'single'

    def question_parser(self, data):   #问题分析
        """
        主要是根据不同的实体和意图构造cypher查询语句
        :param data: {"Player":[], "Team":[], "Honour":[], "Coach":[]，"intention":[]}
        :return:
        """
        sqls = []  #字典为元素的列表
        data = self.data_recognize(data)
        if data:
            for intent in data["intentions"]:  #有可能包含多个意图
                sql_ = {}
                sql_["intention"] = intent   #设定一句sql的意图
                sql = []
                #判断查询类型是单节点还是符合结点
                if self.type_search(data) == 'single':
                    if data.get("Player"):  #查询结点对象为Player
                       sql = self.transfor_to_sql_single("Player", data["Player"], intent)
                    elif data.get("Team"):  #查询结点对象为Team
                        sql = self.transfor_to_sql_single("Team", data["Team"], intent)
                    elif data.get("Coach"):  #查询结点对象为Coach
                        sql = self.transfor_to_sql_single("Coach", data["Coach"], intent)
                    if sql:
                        sql_['sql'] = sql
                        if intent == 'add_time':
                            sql_['node1'] = data['Team']
                        sqls.append(sql_)
                elif self.type_search(data) == 'hon_mul':
                    if data.get('Player') and data.get('Honour'):  #查询球员和荣誉的关系
                        sql = self.transform_to_sql_mul_hon(['Honour','Player'],data['Player'],data['Honour'],intent)
                        sql_['sql'] = sql
                        sql_['node1'],sql_['node2'] = data['Player'],data['Honour']
                        sqls.append(sql_)
                    elif data.get('Coach') and data.get('Honour'):  #查询教练和荣誉的关系
                        if data["Honour"] == ['总冠军']:
                            sql = self.transfor_to_sql_single("Coach", data["Coach"], 'champion')
                            sql_['sql'] = sql
                            sql_['intention'] = 'champion'
                            sqls.append(sql_)
                        else:
                            sql = self.transform_to_sql_mul_hon(['Honour','Coach'],data['Coach'],data['Honour'],intent)
                            sql_['sql'] = sql
                            sql_['node1'],sql_['node2'] = data['Coach'],data['Honour']
                            sqls.append(sql_)
        return sqls

    def transfor_to_sql_single(self, label, entities, intent):
        """
        将问题转变为cypher查询语句
        :param label:实体标签
        :param entities:实体列表
        :param intent:查询意图
        :return:cypher查询语句
        """
        if not entities:
            return []
        sql = []

        # 查询球员荣誉
        if intent == "honour" and label == "Player":
            sql = ["MATCH (d:player)-[:获得]->(s) WHERE d.name ends with '{0}'  RETURN d.name,s.name".format(e)
                   for e in entities]
        # 查询球员效力球队
        if intent == "play_team" and label == "Player":
            sql = ["MATCH (d:player)-[:签约]->(s) WHERE d.name ends with '{0}' RETURN d.name,s.name".format(e)
                   for e in entities]
        #查询教练执教球队
        if intent == "teach_team" and label == "Coach":
            sql = ["MATCH (d:coach)-[:执教]->(s) WHERE d.name ends with '{0}' RETURN d.name,s.name".format(e)
                   for e in entities]
        #以上为对关系的查询
        #查询球员出生日期
        if intent == "birthday" and label == 'Player':
            sql = ["match (d:player) where d.name ends with '{0}' return d.name,d.birthday".format(e)
                   for e in entities]
        # 查询球员出生地址
        if intent == "birthplace" and label == 'Player':
            sql = ["match (d:player) where d.name ends with '{0}' return d.name,d.birthplace".format(e)
                   for e in entities]
        # 查询球员的合同数据
        if intent == "contract" and label == 'Player':
            sql = ["match (d:player) where d.name ends with '{0}' return d.name,d.contract".format(e)
                   for e in entities]
        # 查询球员的球场位置
        if intent == "player_pos" and label == 'Player':
            sql = ["match (d:player) where d.name ends with '{0}' return d.name,d.player_pos".format(e)
                   for e in entities]
        # 查询球员球衣号码
        if intent == "player_num" and label == 'Player':
            sql = ["match (d:player) where d.name ends with '{0}' return d.name,d.player_num".format(e)
                   for e in entities]
        # 查询球员体重
        if intent == "weight" and label == 'Player':
            sql = ["match (d:player) where d.name ends with '{0}' return d.name,d.weight".format(e)
                   for e in entities]
        # 查询球员身高
        if intent == "height" and label == 'Player':
            sql = ["match (d:player) where d.name ends with '{0}' return d.name,d.height".format(e)
                   for e in entities]
        # 查询球员选秀情况
        if intent == "select_des" and label == 'Player':
            sql = ["match (d:player) where d.name ends with '{0}' return d.name,d.select_des".format(e)
                   for e in entities]

        # 查询教练出生日期
        if intent == "birthday" and label == 'Coach':
            sql = ["match (d:coach) where d.name ends with '{0}' return d.name,d.birthday".format(e)
                   for e in entities]
        # 查询教练出生地址
        if intent == "birthplace" and label == 'Coach':
            sql = ["match (d:coach) where d.name ends with '{0}' return d.name,d.birthplace".format(e)
                   for e in entities]
        # 查询教练总决赛情况
        if intent == "final" and label == 'Coach':
            sql = ["match (d:coach) where d.name ends with '{0}' return d.name,d.final".format(e)
                   for e in entities]
        # 查询教练常规赛情况
        if intent == "normalGame" and label == 'Coach':
            sql = ["match (d:coach) where d.name ends with '{0}' return d.name,d.normalGame".format(e)
                   for e in entities]
        # 查询教练季后赛情况
        if intent == "playoff" and label == 'Coach':
            sql = ["match (d:coach) where d.name ends with '{0}' return d.name,d.playoff".format(e)
                   for e in entities]
        # 查询教练生涯情况
        if intent == "career" and label == 'Coach':
            sql = ["match (d:coach) where d.name ends with '{0}' return d.name,d.career".format(e)
                   for e in entities]
        # 查询教练总冠军情况
        if intent == "champion" and label == 'Coach':
            sql = ["match (d:coach) where d.name ends with '{0}' return d.name,d.champion".format(e)
                   for e in entities]
        # 查询球队位置
        if intent == "team_position" and label == 'Team':
            sql = ["match (d:team) where d.name ends with '{0}' return d.name,d.team_position".format(e)
                   for e in entities]
        # 查询球队介绍
        if intent == "team_introduce" and label == 'Team':
            sql = ["match (d:team) where d.name ends with '{0}' return d.name,d.team_introduce".format(e)
                   for e in entities]
        if intent == 'add_time' and label == 'Team':
            sql = ["MATCH p=(a:team{0})-[r:`加入`]->(b:league{1}) RETURN r.name,r.add_time".format(
                '{' + "name:'{0}'".format(entities[0]) + '}', '{' + "name:'{0}'".format('NBA') + '}')]
        return sql

    def transform_to_sql_mul_hon(self, label, node1, node2, intent):   #针对关系进行查询
        sql = []
        if node1 == '' or node2 == '':
            return []
        if intent == 'getTime' and 'Honour' in label and 'Player' in label:   #查询获得时间，即关系属性
            sql = ["MATCH p=(a:player{0})-[r:`获得`]->(b:honour{1}) RETURN r.name,r.getTime".format('{' + "name:'{0}'".format(node1[0]) + '}','{' + "name:'{0}'".format(node2[0]) + '}')]
        elif intent == "getTime" and "Honour" in label and "Coach" in label:
            sql = ["MATCH p=(a:coach{0})-[r:`获得`]->(b:honour{1}) RETURN r.name,r.getTime".format(
                '{' + "name:'{0}'".format(node1[0]) + '}', '{' + "name:'{0}'".format(node2[0]) + '}')]
        return sql

    def searching(self, sqls):
        final_answers = []
        for sql_ in sqls:
            intent = sql_['intention']
            queries = sql_['sql']
            answers = []
            for query in queries:
                ress = self.graph.run(query).data()
                answers += ress
            if intent == 'getTime':
                final_answer = self.answer_template_mul_hon(intent,answers,sql_['node1'],sql_['node2'])
            elif intent == 'add_time':
                final_answer = self.answer_template_mul_hon(intent,answers,sql_['node1'],'NBA')
            else:
                final_answer = self.answer_template_single(intent, answers)
            if final_answer:
                final_answers.append(final_answer)
        return final_answers

    def answer_template_single(self, intent, answers):
        dic = {'birthday':'生日','birthplace':'出生地','contract':'年薪','player_pos':'球场位置','player_num':'球衣号码',
               'weight':'体重','height':'身高','select_des':'选秀情况','final':'总决赛经历','normalGame':'常规赛战绩'
               ,'playoff':'季后赛战绩','career':'生涯执教情况','champion':'冠军数量','team_position':'位于'
               ,'team_introduce':'的简介'
               }
        final_answer = ''
        if not answers:
            return ""
        #查询球员效力球队
        if intent == "play_team":
            disease_dic = {}
            for data in answers:
                d = data['d.name']
                s = data['s.name']
                if d not in disease_dic:
                    disease_dic[d] = [s]
                else:
                    disease_dic[d].append(s)
            i = 0
            for k, v in disease_dic.items():
                if i >= 10:
                    break
                final_answer += "球员 {0} 的效力过的球队有：{1}\n".format(k, ','.join(list(set(v))))
                i += 1
        #查询教练执教球队
        if intent == "teach_team":
            disease_dic = {}
            for data in answers:
                d = data['d.name']
                s = data['s.name']
                if d not in disease_dic:
                    disease_dic[d] = [s]
                else:
                    disease_dic[d].append(s)
            i = 0
            for k, v in disease_dic.items():
                if i >= 10:
                    break
                final_answer += "教练 {0} 的执教过的球队有：{1}\n".format(k, ','.join(list(set(v))))
                i += 1
        if intent in ['birthday','birthplace','contract','player_pos','player_num','weight','height','select_des',
                        'final','normalGame','playoff','career','champion','team_position','team_introduce'
                      ]:
            disease_dic = {}
            for data in answers:
                d = data['d.name']
                s = data['d.' + intent]
                if d not in disease_dic:
                    disease_dic[d] = [s]
                else:
                    disease_dic[d].append(s)
            i = 0
            for k, v in disease_dic.items():
                if i >= 10:
                    break
                print(v)
                final_answer += " {0} 的".format(k) + dic[intent] + "是：{1}\n".format(k, ','.join(list(set(v))))
                i += 1
        return final_answer

    def answer_template_mul_hon(self, intent, answers,node1,node2):
        final_answer = ''
        if not answers:
            return ""
        if intent == "getTime":
            print(answers)
            time = answers[0]['r.getTime']
            final_answer = "{0}在{1}赛季拿到了{2}\n".format(node1[0],time,node2[0])
        elif intent == 'add_time':
            print(answers)
            time = answers[0]['r.add_time']
            final_answer = "{0}在{1}加入了{2}\n".format(node1[0],time,node2[0])
        return final_answer