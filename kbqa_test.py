from entity_extractor import EntityExtractor
from search_answer import AnswerSearching
class KBQA:
    def __init__(self,question):
        self.question = question   #输入问题
        self.extractor = EntityExtractor(self.question)  #意图获取，实体识别
        self.searcher = AnswerSearching()  #答案查找

    def qa_main(self):
        input_str = self.question
        answer = "对不起，您的问题我不知道，我今后会努力改进的。"
        entities = self.extractor.start(input_str)      #实体抽取结果以及提问目标，字典形式

        if not entities:   #问题未匹配到
            return answer
        sqls = self.searcher.question_parser(entities)  #转为sql查询语言
        print(sqls)
        final_answer = self.searcher.searching(sqls)  #查询结果格式化结果
        if not final_answer:
            return answer
        else:
            return '\n'.join(final_answer)

    def main(self):
        answer = self.qa_main()
        return answer