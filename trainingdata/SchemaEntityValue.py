#-*- coding:UTF-8 -*-
'''
Created on 2013-12-3

@author: Bo Xu <mailto:bolang1988@gmail.com>

@version: 1.0

@summary: Construct (category, attribute, entity, value) training data

input:

    infobox:    (entity,attribute, value) split with "\t"

    category:   (entity, category) split with "\t"

    schema:   (category, attribute, ratio) split with "\t",
              ratio is the coverage of an attribute in the category
              It is optional


output:

    schema entity value: (category, attribute, entity, value) split with "\t"
                        different schema(category, attribute) in different files
e.g.:

    infobox file

    ati    公司口号    客户永远是第一位的
    ati    公司名称    冶天
    ati    公司性质    外商独资
    ati    员工数    2500人(2007年)
    ati    外文名称    ATI
    ati    年营业额    20亿美元(2005年)
    ati    总部地点    加拿大安大略省万锦
    ati    成立时间    1985年
    ati    经营范围    显卡、芯片组、电子游戏机
    ibm    公司口号    停止空谈，开始行动！
    ibm    公司名称    国际商业机器公司
    ibm    公司性质    外商独资
    --end--

    category file

    ati    公司
    ibm    公司
    --end--

    schema file

                公司        公司口号    1
                公司        公司名称    1
                公司        公司性质    1
    --end--

    schema entity value file

                公司_公司口号.txt
                公司    公司口号    ati    客户永远是第一位的
                公司    公司口号    ibm    停止空谈，开始行动！

                公司_公司名称.txt
                  公司    公司名称    ati    冶天
                 公司    公司名称    ibm    国际商业机器公司

                公司_公司性质.txt
                  公司    公司性质    ati    外商独资
                 公司    公司性质    ibm    外商独资

'''

import os.path

class SchemaEntityValue(object):
    '''Construct (category, attribute, entity, value) training data'''
    attribute_entity_dict = None    #key:attribute
                                    #value:entity
                                    #from infobox file
    entity_attribute_value_dict = None      #key:(entity,attribute)
                                            #value:value
                                            #from infobox file
    category_entity_dict = None     #key:category
                                    #value:entity
                                    #from category file

    def __init__(self, infobox_path, category_path,\
                 schema_path, schema_entity_value_menu):
        '''Notice that: schema_entity_value_menu is a menu, not a path'''
        self.read_infobox_file(infobox_path)
        self.read_category_file(category_path)
        self.write_schema_entity_value(schema_path, schema_entity_value_menu)

    def read_infobox_file(self,infobox_path):
        '''Get attribute_entity_dict and
        entity_attribute_value_dictfrom infobox file'''
        self.attribute_entity_dict = dict()
        self.entity_attribute_value_dict = dict()
        infobox_file = open(infobox_path,'r')
        infobox_lines = infobox_file.readlines()
        for line in infobox_lines:

            try:
                line = line.rstrip()
                words = line.split("\t")
                if words[1] not in self.attribute_entity_dict:
                    self.attribute_entity_dict[words[1]] = set()
                self.attribute_entity_dict[words[1]].add(words[0])
                self.entity_attribute_value_dict[(words[0], words[1])]\
                 = words[2]
            except IOError:
                print line
        infobox_file.close()

    def read_category_file(self, category_path):
        '''Get category_entity_dict from category file'''
        self.category_entity_dict = dict()
        category_file = open(category_path,'r')
        category_lines = category_file.readlines()
        for line in category_lines:
        #     print "each line", line1
            try:
                line = line.rstrip()
                words = line.split("\t")
                if words[1] not in self.category_entity_dict:
                    self.category_entity_dict[words[1]] = set()
                self.category_entity_dict[words[1]].add(words[0])
            except IOError:
                print line
        category_file.close()

    def write_schema_entity_value(self,schema_path, schema_entity_value_menu):
        '''Get schema. for each schema, find the training data'''
        if not os.path.exists(schema_entity_value_menu):
            os.makedirs(schema_entity_value_menu)
        schema_file = open(schema_path,'r')
        schema_lines = schema_file.readlines()
        for line in schema_lines:
        #     print "each line", line1
            try:
                line = line.rstrip()
                words = line.split("\t")
                category = words[0]
                attribute = words[1]
                file_name = category + "_" + attribute
                entity_set = self.category_entity_dict[category].\
                            intersection(self.attribute_entity_dict[attribute])
                #                 create schema entity value file
                schema_entity_value_file = open(schema_entity_value_menu\
                                                + file_name, 'w')
                for entity in entity_set:
                    schema_entity_value_file.write(entity,\
                        self.entity_attribute_value_dict[(entity, attribute)])

                schema_entity_value_file.close()
            except IOError:
                print line
        schema_file.close()

if __name__ == "__main__":
    MENU_PATH = "H://xubo//baidu4//"
    INFOBOX_PATH = MENU_PATH + "baiduinfobox_filter.txt"
    CATEGORY_PATH = MENU_PATH + "baiducategory_filter10.txt"
    SCHEMA_PATH = MENU_PATH + "sample_baidu_schema_refinered.txt"
    SCHEMA_ENTITY_VALUE_MENU = MENU_PATH + "trainset1"
    TEST = SchemaEntityValue(INFOBOX_PATH, \
                         CATEGORY_PATH, SCHEMA_PATH, SCHEMA_ENTITY_VALUE_MENU)
    