#-*- coding:UTF-8 -*-
'''
Created on 2013年12月5日

@author: Bo Xu <mailto:bolang1988@gmail.com>

@version: 1.0

@summary: Verify the pattern on the training data

input:

    filter schema pattern count: (category, attribute, pattern, \
                                            count, total_count)
                            split with "\t"
                        different schema(category, attribute) in different files

    schema entity value: (category, attribute, entity, value) split with "\t"
                        different schema(category, attribute) in different files

    article text:   text in Baidu Baike. split to sentences. each each a file

output:

    filter schema pattern precise: (category, attribute, pattern, \
                                            precise)
                            split with "\t"
                        different schema(category, attribute) in different files

e.g.:

input:

    filter schema pattern count

            歌手_经纪公司.txt(different menu)
            经纪公司是([\\S]+)    4000    40000
    --end--

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

output:

    filter schema pattern precise: (category, attribute, pattern, \
                                            precise)
            歌手_经纪公司.txt(different menu)
            经纪公司是([\\S]+)    0.98

'''
from __future__ import division
import os
import re
import sys


class Verifying(object):
    '''verify the pattern
    step1: find each schema from schemas
    step2: find all patterns from patterns of one schema
    step3: verify each pattern by schema entity value file and article text'''
    schema_pattern_menu = None
    schema_entity_value_menu = None
    article_menu = None
    schema_pattern_precise_menu = None

    def __init__(self, schema_pattern_menu, \
                 schema_entity_value_menu, \
                 article_menu, \
                 schema_pattern_precise_menu):
        if not os.path.exists(schema_pattern_precise_menu):
            os.makedirs(schema_pattern_precise_menu)
        self.schema_pattern_menu = schema_pattern_menu
        self.schema_entity_value_menu = schema_entity_value_menu
        self.article_menu = article_menu
        self.schema_pattern_precise_menu = schema_pattern_precise_menu
        self.parse_schema_file()

    def parse_schema_file(self):
        '''parse schemas
        input: schema_pattern_menu'''
        schema_pattern_list = os.listdir(self.schema_pattern_menu)
        for schema in schema_pattern_list:
            self.parse_schema_pattern(schema)

    def parse_schema_pattern(self, schema):
        '''parse each schema file
        input: each schema'''
        schema = schema.decode("gb18030")
        print schema
        schema_pattern_precise_file = open(\
                                self.schema_pattern_precise_menu + schema, 'w')
        schema_file = open(self.schema_pattern_menu + schema, 'r')
        schema_lines = schema_file.readlines()
        patterns = list()
        for line in schema_lines:
            line = line.rstrip()
            words = line.split("\t")
            patterns.append(words[0])
        for pattern_precise_tuple in self.verify_pattern(schema, patterns):
            schema_pattern_precise_file.write("%s\t%s\t%s\n" %\
                                    (pattern_precise_tuple[0], \
                                   pattern_precise_tuple[1], \
                                   pattern_precise_tuple[2]))
        schema_pattern_precise_file.close()

    def verify_pattern(self, schema, patterns):
        '''verify each pattern by schema entity value file and article text
        input: pattern, schema_entity_value, article text
        output: pattern_count_dict = (right_count, total_count)'''
        pattern_count_list = list()
        pattern_count_dict = dict()
        schema_entity_value_file =\
         open(self.schema_entity_value_menu + schema, 'r')
        schema_entity_value_lines = schema_entity_value_file.readlines()
        for line in schema_entity_value_lines:
            line = line.rstrip()
            words = line.split("\t")
            entity = words[0]
            value = words[1]
            article_lines = self.read_each_article_file(entity)
            if article_lines:
                extract_pattern_values = self.extract_pattern_value(patterns, \
                                                            article_lines)
                if extract_pattern_values:
                    local_pattern_count_dict = self.compare_two_value(\
                                            value, extract_pattern_values)
                    for local_pattern, count_tuple in\
                                     local_pattern_count_dict.iteritems():
                        if local_pattern not in pattern_count_dict:
                            pattern_count_dict[local_pattern] = [0,0]
                        pattern_count_dict[local_pattern][0] += count_tuple[0]
                        pattern_count_dict[local_pattern][1] += count_tuple[1]
        for pattern, count_tuple in pattern_count_dict.iteritems():
            pattern_count_list.append((pattern, count_tuple[0], count_tuple[1]))
        return pattern_count_list

    def read_each_article_file(self, entity):
        '''read each article, and return the lines'''
        article_lines = None
        try:
            article_file = open(self.article_menu +\
                                entity.decode("utf-8") + ".txt", 'r')
            article_lines = article_file.readlines()
        except IOError:
            pass
        except:
            print "Unexpected error:", sys.exc_info()[0]
        finally:
            return article_lines


    @staticmethod
    def extract_pattern_value(patterns, article_lines):
        '''extract value from article lines using the patterns
        input: patterns, article_lines
        output: pattern_value_list'''
        pattern_value_list = list()
        for line in article_lines:
            for pattern in patterns:
                try:
                    extract_value = re.findall(pattern, line)
                    if len(extract_value):
                        for value in extract_value:
        #                     print value
                            pattern_value_list.append((pattern, value))
                except:
                    pass
        return pattern_value_list

    def compare_two_value(self, value, extract_pattern_values):
        '''compare exact value and the extract pattern value sets'''
        local_pattern_count_dict = dict()
        for pattern, extract_value in extract_pattern_values:
            if pattern not in local_pattern_count_dict:
                local_pattern_count_dict[pattern] = [0,0]
            lcs = self.longest_common_subsequence(value, extract_value)
            if lcs == value or lcs == extract_value:
                local_pattern_count_dict[pattern][0] += 1
            local_pattern_count_dict[pattern][1] += 1
        return local_pattern_count_dict

    @staticmethod
    def longest_common_subsequence(value1, value2):
        '''find the longest common subsequence between value1 and value2'''
        lengths = [[0 for temp_j in range(len(value2)+1)]\
                    for temp_i in range(len(value1)+1)]
        # row 0 and column 0 are initialized to 0 already
        for temp_i, temp_x in enumerate(value1):
            for temp_j, temp_y in enumerate(value2):
                if temp_x == temp_y:
                    lengths[temp_i+1][temp_j+1] = lengths[temp_i][temp_j] + 1
                else:
                    lengths[temp_i+1][temp_j+1] = \
                        max(lengths[temp_i+1][temp_j], \
                            lengths[temp_i][temp_j+1])
        # read the substring out from the matrix
        result = ""
        temp_x, temp_y = len(value1), len(value2)
        while temp_x != 0 and temp_y != 0:
            if lengths[temp_x][temp_y] == lengths[temp_x-1][temp_y]:
                temp_x -= 1
            elif lengths[temp_x][temp_y] == lengths[temp_x][temp_y-1]:
                temp_y -= 1
            else:
                assert value1[temp_x-1] == value2[temp_y-1]
                result = value1[temp_x-1] + result
                temp_x -= 1
                temp_y -= 1
        return result

if __name__ == "__main__":
    MENU_PATH = "G://xubo//baidu4//"
    SCHEMA_PATTERN_MENU = MENU_PATH + "pattern//"
    SCHEMA_ENTITY_VALUE_MENU = MENU_PATH + "trainset1//"
    ARTICLE_MENU = MENU_PATH + "geshou//"
    SCHEMA_PATTERN_PRECISE_MENU = MENU_PATH + "precise//"

    TEST = Verifying(SCHEMA_PATTERN_MENU, \
                         SCHEMA_ENTITY_VALUE_MENU, \
                         ARTICLE_MENU, \
                         SCHEMA_PATTERN_PRECISE_MENU)
