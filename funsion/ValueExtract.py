#-*- coding:UTF-8 -*-
'''
Created on 2013年12月6日

@author: Bo Xu <mailto:bolang1988@gmail.com>

@version: 1.0

@summary: Extract value from the article text using the patterns

input:

    filter schema pattern: (category, attribute, pattern)
                            split with "\t"
    article text: text in Baidu Baike. split to sentences. each each a file

output:

    entity attribute pattern value


e.g.:

input:

    filter schema pattern
        歌手.txt
         经纪公司       所属公司：([\\S]+)    0.901
         经纪公司       经纪公司：([\\S]+)    0.932
        经纪公司       签约公司：([\\S]+)    0.802
        经纪公司       公司：([\\S]+)    0.793
       职业      职业：([\\S]+)    0.872
       职业      职业：([\\S]+)    0.768
       职业      最佳本地([\\S]+)    0.876

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

output:

    陈紫函    经纪公司    所属公司：([\\S]+)    华谊兄弟传媒集团

'''

import os
import re
import time

class ValueExtractFromCategory(object):
    '''Extract value from the article text of a category using the patterns'''
    category_model_path = None
    article_menu = None
    entity_value_path = None
    pattern_attribute_dict = None
    pattern_list = None
    def __init__(self, category_model_path, article_menu, entity_value_path):
        self.category_model_path = category_model_path.decode("utf-8")
        self.article_menu = article_menu
        self.entity_value_path = entity_value_path.decode("utf-8")
        self.read_pattern_attribute()
        self.extract_value()

    def read_pattern_attribute(self):
        '''fill pattern_attribute_dict with category_model_menu'''
        self.pattern_attribute_dict = dict()
        self.pattern_list = list()
        pattern_attribute_file = open(self.category_model_path, 'r')
        pattern_attribute_lines = pattern_attribute_file.readlines()
        for line in pattern_attribute_lines:
            line = line.rstrip()
            words = line.split("\t")
            attribute = words[0]
            pattern = words[1]
            self.pattern_attribute_dict[pattern] = attribute
            self.pattern_list.append(pattern)
        pattern_attribute_file.close()

    def extract_value(self):
        '''extract value'''
        entity_value_file = open(self.entity_value_path, 'w')
        article_list = os.listdir(self.article_menu)
        for article in article_list:
            article = article.decode("gb18030")
#             article = article.replace(".txt", "")
            try:
                article_lines = self.read_each_article_file(self.article_menu, \
                                                            article)
                if article_lines:
                    extract_pattern_values =\
                                 self.extract_pattern_value(article_lines)
                    if extract_pattern_values:
                        pattern_value_dict = dict()
                        for pattern_value in extract_pattern_values:
                            one_pattern = pattern_value[0]
                            two_value = pattern_value[1]
                            if one_pattern not in pattern_value_dict:
                                pattern_value_dict[one_pattern] = set()
                            pattern_value_dict[one_pattern].add(two_value)
                        for dict_pattern, dict_value in\
                                     pattern_value_dict.iteritems():
                            list_value = list(dict_value)
                            if len(list_value) == 1:
                                new_value = list_value[0]
                                entity_value_file.write("%s\t%s\t%s\t%s\n" %\
                                    (article.replace(".txt", ""), \
                                    self.pattern_attribute_dict[dict_pattern], \
                                    dict_pattern, \
                                    new_value))
            except IOError:
                print article + " not open"
        entity_value_file.close()\

    @staticmethod
    def read_each_article_file(article_menu, entity):
        '''read each article, and return the lines'''
        article_file = open(article_menu + entity, 'r')
        article_lines = article_file.readlines()
        article_file.close()
        return article_lines

    def extract_pattern_value(self, article_lines):
        '''extract value from article lines using the patterns
        input: patterns, article_lines
        output: pattern_value_list'''
        pattern_value_list = list()
        for line in article_lines:
            for pattern in self.pattern_list:
                try:
                    extract_value = re.findall(pattern, line)
                    if len(extract_value):
                        for value in extract_value:
        #                     print value
                            pattern_value_list.append((pattern, value))
                except:
                    pass
        return pattern_value_list

if __name__ == "__main__":
    START_TIME = time.clock()
    MENU_PATH = "G://xubo//baidu4//"
    CATEGORY_MODEL_PATH = MENU_PATH + "model//歌手"
    ARTICLE_MENU = MENU_PATH + "geshou//"
    ENTITY_VALUE_MENU = MENU_PATH + "value//"
    ENTITY_VALUE_PATH = ENTITY_VALUE_MENU + "歌手"
    TEST = ValueExtractFromCategory(CATEGORY_MODEL_PATH, \
                         ARTICLE_MENU, \
                         ENTITY_VALUE_PATH)
    END_TIME = time.clock()
    print "Spend time : ", (END_TIME - START_TIME)
