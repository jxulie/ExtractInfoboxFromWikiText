#-*- coding:UTF-8 -*-
'''
Created on 2013年12月9日

@author: Bo Xu <mailto:bolang1988@gmail.com>

@version: 1.0

@summary: Funsion the same entity attribute pair

input:

    filter schema pattern: (category, attribute, pattern)
                            split with "\t"

    entity attribute pattern value

output:

    funsion entity attribute value

e.g.

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

    entity attribute pattern value
        陈紫函    经纪公司    所属公司：([\\S]+)    华谊兄弟传媒集团
        陈紫函    经纪公司    公司：([\S]+)    喜马拉雅音乐

output:

    funsion entity attribute value
        陈紫函    经纪公司    华谊兄弟传媒集团

'''
import time

class ValueFusion(object):
    '''Funsion the same entity attribute pair from
     lots of entity attribute value '''
    category_model_path = None
    entity_value_path = None
    funsion_path = None
    pattern_precise_dict = None
    def __init__(self, category_model_path, entity_value_path, funsion_path):
        self.category_model_path = category_model_path.decode("utf-8")
        self.entity_value_path = entity_value_path.decode("utf-8")
        self.funsion_path = funsion_path.decode("utf-8")
        self.read_pattern_precise()
        self.funsion_data()

    def read_pattern_precise(self):
        '''fill pattern_attribute_precise_dict with category_model_menu'''
        self.pattern_precise_dict = dict()
        pattern_attribute_file = open(self.category_model_path, 'r')
        pattern_attribute_lines = pattern_attribute_file.readlines()
        for line in pattern_attribute_lines:
            line = line.rstrip()
            words = line.split("\t")
            attribute = words[0]
            pattern = words[1]
            precise = float(words[2])
            self.pattern_precise_dict[(pattern,attribute)] = precise
        pattern_attribute_file.close()

    def funsion_data(self):
        '''funsion the same entity attribute pair'''
        entity_attribute_dict = dict()
        entity_value_file = open(self.entity_value_path, 'r')
        entity_value_lines = entity_value_file.readlines()
        for line in entity_value_lines:
            line = line.rstrip()
            words = line.split("\t")
            entity = words[0]
            attribute = words[1]
            pattern = words[2]
            value = words[3]
            if (entity, attribute) not in entity_attribute_dict:
                entity_attribute_dict[(entity, attribute)] = dict()
            if value not in entity_attribute_dict[(entity, attribute)]:
                entity_attribute_dict[(entity, attribute)][value] = 0
            entity_attribute_dict[(entity, attribute)][value] +=\
                                self.pattern_precise_dict[(pattern, attribute)]
        entity_value_file.close()
#         one (entity, attribute) return one value
        funsion_file = open(self.funsion_path, 'w')
        for dict_key, dict_value in sorted(entity_attribute_dict.iteritems()):
            max_value = max(dict_value.iterkeys(),key=lambda k:dict_value[k])
            funsion_file.write("%s\t%s\t%s\n" %\
                               (dict_key[0], dict_key[1], max_value))
        funsion_file.close()

if __name__ == "__main__":
    START_TIME = time.clock()
    MENU_PATH = "G://xubo//baidu4//"
    CATEGORY_MODEL_PATH = MENU_PATH + "model//歌手"
    ENTITY_VALUE_MENU = MENU_PATH + "value//"
    ENTITY_VALUE_PATH = ENTITY_VALUE_MENU + "歌手"
    FUNSION_PATH = ENTITY_VALUE_MENU + "Fusion歌手"
    TEST = ValueFusion(CATEGORY_MODEL_PATH, \
                         ENTITY_VALUE_PATH, \
                         FUNSION_PATH)
    END_TIME = time.clock()
    print "Spend time : ", (END_TIME - START_TIME)
