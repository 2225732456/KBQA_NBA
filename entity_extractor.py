import ahocorasick
from sklearn.externals import joblib
import numpy as np
import scrapy
from getQuestion import MyClassifier
class EntityExtractor:
    def __init__(self,question):
        self.question = question
        self.player_path = 'data/player.txt'
        self.team_path = 'data/team.txt'
        self.honour_path = 'data/honour.txt'
        self.coach_path = 'data/coach.txt'
        self.player_entities = [w.strip() for w in open(self.player_path, encoding='utf-8') if w.strip()]
        self.team_entities = [w.strip() for w in open(self.team_path, encoding='utf-8') if w.strip()]
        self.honour_entities = [w.strip() for w in open(self.honour_path, encoding='utf-8') if w.strip()]
        self.coach_entities = [w.strip() for w in open(self.coach_path, encoding='utf-8') if w.strip()]

        # if '-' not in self.question:
        #     li = self.player_entities
        #     for cur in li:
        #         temp = cur.split('-')
        #         if len(temp) >= 2:
        #             if temp[1] not in self.player_entities:
        #                 self.player_entities.append(temp[1])
        #     li = self.coach_entities
        #     for cur in li:
        #         temp = cur.split('-')
        #         if len(temp) >= 2:
        #             if temp[1] not in self.coach_entities:
        #                 self.coach_entities.append(temp[1])

        self.player_tree = self.build_actree(list(set(self.player_entities)))
        self.team_tree = self.build_actree(list(set(self.team_entities)))
        self.honour_tree = self.build_actree(list(set(self.honour_entities)))
        self.coach_tree = self.build_actree(list(set(self.coach_entities)))

    def entity_reg(self, question):
        """
        模式匹配, 得到匹配的词和类型
        :param question:str
        :return:
        """
        self.result = {}
        for i in self.player_tree.iter(question):
            word = i[1][1]

            if "Player" not in self.result:
                self.result["Player"] = [word]
            else:
                self.result["Player"].append(word)
        for i in self.team_tree.iter(question):
            word = i[1][1]
            if "Team" not in self.result:
                self.result["Team"] = [word]
            else:
                self.result["Team"].append(word)
        for i in self.honour_tree.iter(question):
            wd = i[1][1]
            if "Honour" not in self.result:
                self.result["Honour"] = [wd]
            else:
                self.result["Honour"].append(wd)
        for i in self.coach_tree.iter(question):
            wd = i[1][1]
            if "Coach" not in self.result:
                self.result["Coach"] = [wd]
            else:
                self.result["Coach"] .append(wd)
        return self.result

    def build_actree(self, wordlist):
        """
        构造actree，加速过滤
        :param wordlist:
        :return:
        """
        actree = ahocorasick.Automaton()
        # 向树中添加单词
        for index, word in enumerate(wordlist):
            actree.add_word(word, (index, word))
        actree.make_automaton()
        return actree

    def extractor(self, question):
        self.entity_reg(question)
        types = []  # 实体类型
        for v in self.result.keys():
            types.append(v)
        return self.result

    def edit_distance(self, word1, word2):
        len1 = len(word1)
        len2 = len(word2)
        dp = np.zeros((len1 + 1, len2 + 1))
        for i in range(len1 + 1):
            dp[i][0] = i
        for j in range(len2 + 1):
            dp[0][j] = j

        for i in range(1, len1 + 1):
            for j in range(1, len2 + 1):
                delta = 0 if word1[i - 1] == word2[j - 1] else 1
                dp[i][j] = min(dp[i - 1][j - 1] + delta, min(dp[i - 1][j] + 1, dp[i][j - 1] + 1))
        return dp[len1][len2]

    def start(self,target):
        extractor = EntityExtractor(target)
        classifier = MyClassifier()
        goal = classifier.classifier(target)   #问题分类器
        result = extractor.extractor(target)   #实体抽取
        result['intentions'] = [goal[0]]       #以相似度最高的问题模板作为目标问题
        print(result)
        return result

# if __name__ == '__main__':
#     target = "科比-布莱恩特的生日是多久"
#     extractor = EntityExtractor(target)  #实体抽取
#     classifier = MyClassifier()   #问题分类器
#     goal = classifier.classifier(target)
#     result = extractor.extractor(target)
#     result['intention'] = [goal[0]]
#     print("问题",target)
#     print(result)
