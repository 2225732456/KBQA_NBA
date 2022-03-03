import jieba
import math
import pickle
class MyTfIdf:
    def __init__(self,passages,content):
        self.passages = passages  #文档列表
        self.content = content    #正文集合
        self.word_list = self.jieba_cut()   #词项表
        self.count_list = self.getCount()   #词个数表
        self.tf_list = self.getTf()   #tf表
        self.idf_list = self.getIdf()   #idf表
        self.tfidf_list = self.get_tf_idf()   #tfidf表

    def jieba_cut(self):
        tests = self.passages  #获取文件内容,分文章
        word_list = []
        for test in tests:
            word_list.append([m for m in jieba.cut(str(test))])   #结巴分词
        return word_list

    def getCount(self):
        word_list = self.word_list
        count_list = []
        for words in word_list:
            docv = {}
            for word in words:
                docv[word] = docv.get(word, 0) + 1
            count_list.append(docv)
        return count_list

    def returnSum_125(self,myDict):
        sum = 0
        for i in myDict:
            sum = sum + myDict[i]
        return sum

    def getTf(self):
        count_list = self.count_list
        tf_list = []
        for i, words in enumerate(count_list):
            tfs = {}
            lenth = self.returnSum_125(words)
            for word in words:
                tfs[word] = 1.0 * count_list[i][word] / lenth
            tf_list.append(tfs)
        return tf_list

    def getIdf(self):
        count_list = self.count_list
        docs = {}
        for counts in count_list:  # 计算出现的文档数
            for word in counts:
                docs[word] = docs.get(word, 0) + 1
        idf_list = {}
        for doc in docs:
            idf_list[doc] = math.log(len(count_list) / (docs[doc] + 1))
        return idf_list

    def get_tf_idf(self):
        tf_list = self.tf_list
        idf_list = self.idf_list
        word_tfidf = {}
        for word_vec in tf_list:
            for word in word_vec:
                word_tfidf[word] = 1.0 * word_vec[word] * idf_list[word]
        return word_tfidf

class MyClassifier(object):
    def __init__(self):
        self.path = r"data/question.txt"  # 问题模板   # 问题模板所在路径
        self.target_pas = []  #问题模板
        self.target_words = []  #模板和问题的分词结果
        self.content = ''  # 所用的资源文件整体
        self.passages = self.getDate()  # 各篇文章集合列表
        # with open('tfidf.pkl', 'rb') as file:
        #     self.myTfidf = pickle.load(file)  # 计算检索出的文章与检索句子的TFIDF
        self.myTfidf = MyTfIdf(self.passages,self.content).tfidf_list
        self.result = ''  #检索结果
        self.intention = {}

    # 获取源数据
    def getDate(self):
        path = self.path
        content = open(path, encoding='utf-8').read()
        self.content = content  #初始化
        content = content.split('\n')   #每一行即为一篇文章
        return content

    def order_dict(dicts, n):
        result = []
        result1 = []
        p = sorted([(k, v) for k, v in dicts.items()], reverse=True)
        s = set()
        for i in p:
            s.add(i[1])
        for i in sorted(s, reverse=True)[:n]:
            for j in p:
                if j[1] == i:
                    result.append(j)
        for r in result:
            result1.append(r[0])
        return result1[0:n]

    def Similarity(self, a, b):
        sum_1, sum_2, sum_3 = 0, 0, 0
        for i in range(0, len(a)):
            sum_1 += a[i] * b[i]
            sum_2 += a[i] * a[i]
            sum_3 += b[i] * b[i]
        sum_4 = math.sqrt(sum_2) * math.sqrt(sum_3)
        if sum_4 != 0:
            result = sum_1 / sum_4
        else:
            result = sum_1 / (sum_4 + 1)
        return result

    def getSimilarity(self,target_pas):
        # 向量化，tfidf作为分量
        vecs = []
        for passage in target_pas:  #依次取出一篇文章
            temp = []
            for word in self.myTfidf:  #依次取出一个词
                if word in passage:
                    temp.append(self.myTfidf[word])
                else:
                    temp.append(0)
            vecs.append(temp)  #tfidf向量化

        result = {}
        for i in range(len(vecs) - 1):
            sum_1 = self.Similarity(vecs[len(vecs) - 1], vecs[i])
            result[self.intention[target_pas[i]]] = sum_1
        result = sorted(result.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)
        self.result = result
        return result

    def Start(self,sentence):  #数据预处理
        target = sentence   #待处理问题
        target_pas = open(self.path,encoding='utf-8').read().split('\n')  # 问题模板集合
        pas = []
        for cur in target_pas:
            temp = cur.split(' ')
            self.intention[temp[1]] = temp[0]
            pas.append(temp[1])
        target_pas = pas

        target_pas.append(target)  # 把待处理问题和问题模板放在一起计算tfIDF
        self.content = ''.join(target_pas)  #字符串形式的文章
        self.target_pas = target_pas
        return

    def display(self):
        for cur in self.result:
            print(cur)

    def classifier(self,sentence):
        self.Start(sentence)  # 程序入口
        self.getSimilarity(self.target_pas)  # 计算搜索句子与检索出的文章的相似度
        return self.result[0]

def main(sentence):
    myclassifier = MyClassifier()
    myclassifier.Start(sentence)   #程序入口
    myclassifier.getSimilarity(myclassifier.target_pas)  #计算搜索句子与检索出的文章的相似度
    print("问题",sentence)
    myclassifier.display()
# main("勒布朗-詹姆斯哪个赛季拿到了MVP")