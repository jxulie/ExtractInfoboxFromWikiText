#-*- coding:UTF-8 -*-
'''
Created on 2013年12月4日

@author: Bo Xu <mailto:bolang1988@gmail.com>

@version: 1.0

@summary: convert sentence to pattern and filter the unusual patterns

input:

    schema value sentence: (category, attribute, value, sentence)
                            split with "\t"
                        different schema(category, attribute) in different files
                        file type: category_attribute.txt    value \t sentence

    threshold: filter unusually patterns

output:

    filter schema pattern count: (category, attribute, pattern, \
                                            count, total_count)
                            split with "\t"
                        different schema(category, attribute) in different files

e.g.:

input:

    schema value sentence

            歌手_经纪公司.txt(different menu)
            华谊兄弟传媒集团    经纪公司是华谊兄弟传媒集团
    --end--

    threshold

    20

output:

    filter schema pattern count

            歌手_经纪公司.txt(different menu)
            经纪公司是([\\S]+)    4000    40000
    --end--

'''

import os
import operator

class ParseCount(object):
    '''convert value in sentence to ([\\S]+)'''

    threshold = None
    schema_value_sentence_menu = None
    schema_pattern_menu = None

    def __init__(self, schema_value_sentence_menu, \
                 threshold, schema_pattern_menu):
        if not os.path.exists(schema_pattern_menu):
            os.makedirs(schema_pattern_menu)
        self.threshold = threshold
        self.schema_value_sentence_menu = schema_value_sentence_menu
        self.schema_pattern_menu = schema_pattern_menu
        self.parse_schema_file()


    def parse_schema_file(self):
        '''parse schemas'''
        schema_list = os.listdir(self.schema_value_sentence_menu)
        for schema in schema_list:
            self.parse_schema_value_sentence(schema)

    def parse_schema_value_sentence(self, schema):
        '''parse each schema file'''
        try:
            schema = schema.decode("gb18030")
            schema_file = open(self.schema_value_sentence_menu + schema, 'r')
            schema_pattern_dict = dict()
            schema_lines = schema_file.readlines()
            pattern_count = 0
            for line in schema_lines:
                try:
                    if line != "\n":
                        line = line.rstrip()
                        line = line.replace(" ", "")
                        words = line.split("\t")
                        if words[0] != words[1]:
                            pattern = self.convert_sentence_to_pattern\
                                                        (words[0], words[1])
                            if pattern not in schema_pattern_dict:
                                schema_pattern_dict[pattern] = 0
                            schema_pattern_dict[pattern] += 1
                            pattern_count += 1
                except:
    #                     pass
                    print "error in : " + line
            self.write_schema_pattern(schema, \
                                      schema_pattern_dict, pattern_count)

            schema_file.close()
            del schema_pattern_dict
        except IOError:
            print self.schema_value_sentence_menu + schema + " not exist"

    @staticmethod
    def convert_sentence_to_pattern(value, sentence):
        '''convert sentence to pattern'''
        regular_pattern = sentence.replace(value,"([\\S]+)")
        return regular_pattern

    def write_schema_pattern(self, schema, schema_pattern_dict, pattern_count):
        '''Write schema pattern to file, filter
        input:
            schema: category_attribute
            schema_pattern_dict: pattern dict
            pattern_count: the total number of pattern

        output:
            schema_pattern_file: category_attribute.txt pattern


        '''
        schema_pattern_file = open(self.schema_pattern_menu + schema, 'w')
        count_num = 0
        for pattern, value in sorted(schema_pattern_dict.iteritems(), \
                                     key=operator.itemgetter(1), \
                                     reverse = True):
            if value > self.threshold:
                count_num += 1
                schema_pattern_file.write("%s\t%s\t%s\n" %\
                                          (pattern, value, pattern_count))
                if count_num >= 10:
                    break
        schema_pattern_file.close()

if __name__ == "__main__":
    MENU_PATH = "G://xubo//baidu4//"
    SCHEMA_VALUE_SENTENCE_MENU = MENU_PATH + "trainset2//"
    THRESHOLD = 20
    SCHEMA_PATTERN_MENU = MENU_PATH + "pattern//"
    TEST = ParseCount(SCHEMA_VALUE_SENTENCE_MENU, \
                         THRESHOLD, SCHEMA_PATTERN_MENU)
