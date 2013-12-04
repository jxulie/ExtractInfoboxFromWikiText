#-*- coding:UTF-8 -*-
'''
Created on 2013年12月4日

@author: Bo Xu <mailto:bolang1988@gmail.com>

@version: 1.0

@summary: Construct (category, attribute, value, sentence) training data


input:

    schema entity value: (category, attribute, entity, value) split with "\t"
                        different schema(category, attribute) in different files

    article text:   text in Baidu Baike. split to sentences. each each a file

output:

    schema value sentence: (category, attribute, value, sentence)
                            split with "\t"
                        different schema(category, attribute) in different files
e.g.:

    schema entity value file

              歌手_经纪公司.txt
                 陈紫函    华谊兄弟传媒集团
                娄译心    索卡尼娱乐
                妮琪·米娜    YoungMoney/CashMoney/环球
                川澄绫子    大泽事务所
                范玮琪    百娱传媒股份有限公司
                胡蓓蔚    “永星”唱片公司
                超新星_(韩国组合)    CoreContentsMedia
                易灵汐    巧思传媒文化公司
                黄铠晴    东亚娱乐
                朴灿烈    SMEntertainment
                梁咏琪    美亚娱乐资讯集团有限公司
                雷·查尔斯    AtlanticRecords
                艾莉莎    喜乐音乐文化传媒（北京）公司
                练正华    成都歌舞剧院
                郑华娟    滚石唱片有限公司
                言承旭    戏梦堂娱乐经纪有限公司
    --end--

    article text
            陈紫函.txt

            籍贯陈紫函(6张)：重庆[1-3]
            中学：重庆南开中学
            大学：北京电影学院表演系
            家庭成员：父母、本人
            粉丝昵称：紫菜
            语言：中文、粤语、英语
            方言：重庆话
            特长：舞蹈、绘画、设计、单眼转
            爱好：阅读、旅行、保龄球
            宗教信仰陈紫函签名照(5张)：基督教
            宠物：卡卡、宝宝（雪纳瑞犬）、卢比（泰迪）
            最喜欢的水果：山竹
            最喜欢的糖果：巧克力
            最喜欢的食物：辣椒
            电视剧剧照(35张)最喜欢的颜色：蓝色、紫色
            最喜欢的衣着：休闲
            最喜欢的电影：《魂断蓝桥》
            最喜欢的男演员：反町隆史
            最喜欢的女演员：张曼玉
    --end--

    schema value sentence

            歌手_经纪公司.txt(different menu)
            华谊兄弟传媒集团    经纪公司是华谊兄弟传媒集团
    --end--

'''

import os

class SchemaValueSentence(object):
    '''Construct (category, attribute, value, sentence) training data
    Step1: read the schema entity value file.
    Step2: For each schema, find value sentences
    through entity-value and entity-sentence files
    '''

    def __init__(self, schema_entity_value_menu, \
                 article_menu, schema_value_sentence_menu):
        '''Notice that: schema_entity_value_menu is a menu, not a path'''
        self.read_schema_entity_value_file(schema_entity_value_menu, \
                                           article_menu, \
                                           schema_value_sentence_menu)

    def read_schema_entity_value_file(self, \
                                      schema_entity_value_menu, \
                                      article_menu, \
                                      schema_value_sentence_menu):
        '''Step1: read the schema entity value file.'''
        schema_list = os.listdir(schema_entity_value_menu)
        for schema in schema_list:
            schema = schema#.decode("gb18030")
            self.read_each_schema_file(schema_entity_value_menu, \
                                       schema, \
                                       article_menu, \
                                       schema_value_sentence_menu)

    def read_each_schema_file(self, \
                              schema_entity_value_menu, \
                              schema, \
                              article_menu, \
                              schema_value_sentence_menu):
        '''read each schema file'''
        try:
            schema_file = open(schema_entity_value_menu + schema, 'r')
            schema_lines = schema_file.readlines()
            for line in schema_lines:
                line = line.rstrip()
                words = line.split("\t")
#                 print words[0] + "++++++++++++++" + words[1]
                try:
                    article_lines = self.read_each_article_file(article_menu, \
                                                                words[0])
                    self.write_match_sentence(schema, \
                                             words[1], \
                                             article_lines, \
                                             schema_value_sentence_menu)
                except IOError:
                    print article_menu + words[0] + ".txt" + "not exist"
            schema_file.close()
        except IOError:
            print schema + schema + " not exist"

    def read_each_article_file(self, article_menu, entity):
        '''read each article, and return the lines'''
        article_file = open(article_menu + entity.decode("utf-8") + ".txt", 'r')
        article_lines = article_file.readlines()
        return article_lines

    def write_match_sentence(self, \
                            schema, \
                            value, \
                            lines, \
                            schema_value_sentence_menu):
        '''find value in sentence of file
        if value in sentence, write value,sentence pair'''
        if not os.path.exists(schema_value_sentence_menu):
            os.makedirs(schema_value_sentence_menu)
        match_file = open(schema_value_sentence_menu + schema, 'a')
        for line in lines:
            line = line.strip()
            if value in line:
                match_file.write("%s\t%s\n" %(value,line))
        match_file.close()

if __name__ == "__main__":
    MENU_PATH = "G://xubo//baidu4//"
    SCHEMA_ENTITY_VALUE_MENU = MENU_PATH + "trainset1//"
    ARTICLE_MENU = MENU_PATH + "geshou//"
    SCHEMA_VALUE_SENTENCE_MENU = MENU_PATH + "trainset2//"
    TEST = SchemaValueSentence(SCHEMA_ENTITY_VALUE_MENU, \
                         ARTICLE_MENU, SCHEMA_VALUE_SENTENCE_MENU)
