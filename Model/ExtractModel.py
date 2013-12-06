#-*- coding:UTF-8 -*-
'''
Created on 2013年12月6日

@author: Bo Xu <mailto:bolang1988@gmail.com>

@version: 1.0

@summary: Determine the extract model from learning module

input:

    schema pattern right count: (category, attribute, pattern, \
                                            right, count)
                            split with "\t"
                        different schema(category, attribute) in different files

    threshold:    the threshold of which pattern to choose

output:

    filter schema pattern: (category, attribute, pattern)
                            split with "\t"


e.g.:

input:

    schema pattern right count

            歌手_经纪公司.txt
            所属公司：([\S]+)    95    134
            经纪公司：([\S]+)    122    172
            签约公司：([\S]+)    19    22
            公司：([\S]+)    497    979
    --end--

            歌手_职业.txt
            职业：([\S]+)    306    566
            职业：([\S]+)　    6    11
            最佳本地([\S]+)    22    73
    --end--

output:

    filter schema pattern
         歌手    经纪公司       所属公司：([\S]+)
         歌手    经纪公司       经纪公司：([\S]+)
        歌手    经纪公司       签约公司：([\S]+)
        歌手    经纪公司       公司：([\S]+)
       歌手    职业      职业：([\S]+)
       歌手    职业      职业：([\S]+)
       歌手    职业      最佳本地([\S]+)
'''
from __future__ import division
import os

class ExtractModel(object):
    '''Merge all the schema of the same category, \
    and filter the low precise pattern'''
    schema_pattern_precise_menu = None
    threshold = None
    category_model_menu = None
    def __init__(self, schema_pattern_precise_menu, \
                 threshold, category_model_menu):
        self.schema_pattern_precise_menu = schema_pattern_precise_menu
        self.threshold = threshold
        self.category_model_menu = category_model_menu
        if not os.path.exists(category_model_menu):
            os.makedirs(category_model_menu)
        self.merge_schema()

    def merge_schema(self):
        '''merge schemas
        input: schema_pattern_precise_menu'''
        schema_pattern_list = os.listdir(self.schema_pattern_precise_menu)
        for schema in schema_pattern_list:
            schema = schema.decode("gb18030")
            schema_split = schema.split("_")
            category = schema_split[0]
            attribute = schema_split[1]
#             print category, attribute
            patterns = self.filter_schema_pattern(schema)
            category_model_file = open(self.category_model_menu + category, 'a')
            for pattern in patterns:
                category_model_file.write("%s\t%s\t%s\n" %(\
                                            category, attribute, pattern))
            category_model_file.close()

    def filter_schema_pattern(self, schema):
        '''filter schema pattern with threshold'''
        schema_file = open(self.schema_pattern_precise_menu + schema, 'r')
        schema_lines = schema_file.readlines()
        patterns = list()
        for line in schema_lines:
#             print line
            line = line.rstrip()
            words = line.split("\t")
#             print line
#             print words[0], words[1], words[2], int(words[1])/int(words[2])
            if int(words[1])/int(words[2]) > self.threshold:
#                 print "ok " + words[0], words[1], words[2]
                patterns.append(words[0])
        return patterns

if __name__ == "__main__":
    MENU_PATH = "G://xubo//baidu4//"
    SCHEMA_PATTERN_PRECISE_MENU = MENU_PATH + "precise//"
    THRESHOLD = 0.5
    CATEGORY_MODEL_MENU = MENU_PATH + "model//"
    TEST = ExtractModel(SCHEMA_PATTERN_PRECISE_MENU, \
                         THRESHOLD, \
                         CATEGORY_MODEL_MENU)

