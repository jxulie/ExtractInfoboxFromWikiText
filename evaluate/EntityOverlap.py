#-*- coding:UTF-8 -*-
'''
Created on 2013年12月10日

@author: Bo Xu <mailto:bolang1988@gmail.com>

@version: 1.0

@summary: compare the experiment results

compare 1: entity overlap

compare 2: entity_attribute overlap

compare 3: entity_attribute_value overlap

'''

MENU_PATH = "G://xubo//baidu4//"
TARGET_INFOBOX_PATH = MENU_PATH + "targetinfobox.txt"
FUNSION_PATH = MENU_PATH + "value//Fusion歌手"

entity_set1 = set()
entity_set2 = set()
entity_attribute_set1 = set()
entity_attribute_set2 = set()
entity_attribute_value_set1 = set()
entity_attribute_value_set2 = set()

target_file = open(TARGET_INFOBOX_PATH, 'r')
target_lines = target_file.readlines()
for line in target_lines:
    line = line.rstrip()
    words = line.split("\t")
    entity = words[0]
    attribute = words[1]
    value = words[2]
    entity_set1.add(entity)
    entity_attribute_set1.add((entity, attribute))
    entity_attribute_value_set1.add((entity, attribute, value))

funsion_file = open(FUNSION_PATH.decode("utf-8"), 'r')
funsion_lines = funsion_file.readlines()
for line in funsion_lines:
    line = line.rstrip()
    words = line.split("\t")
    entity = words[0]
    attribute = words[1]
    value = words[2]
    entity_set2.add(entity)
    entity_attribute_set2.add((entity, attribute))
    entity_attribute_value_set2.add((entity, attribute, value))

print len(entity_set1), len(entity_set2), len(entity_set1.intersection(entity_set2))
print len(entity_attribute_set1), len(entity_attribute_set2), len(entity_attribute_set1.intersection(entity_attribute_set2))
print len(entity_attribute_value_set1), len(entity_attribute_value_set2), len(entity_attribute_value_set1.intersection(entity_attribute_value_set2))