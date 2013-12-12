#-*- coding:UTF-8 -*-
'''
Created on 2013年12月10日

@author: Bo Xu <mailto:bolang1988@gmail.com>

@version: 1.0

@summary: Get the target infobox from infobox and category

input:

    infobox file

    category file

    target category

output:

    target infobox file

'''
target_category = "歌手".decode("utf-8")
MENU_PATH = "G://xubo//baidu4//"
INFOBOX_PATH = MENU_PATH + "baiduinfobox_filter.txt"
CATEGORY_PATH = MENU_PATH + "baiducategory_filter10.txt"
TARGET_INFOBOX_PATH = MENU_PATH + "targetinfobox.txt"
category_entity_set = set()
category_file = open(CATEGORY_PATH, 'r')
category_lines = category_file.readlines()
for line in category_lines:
    line = line.rstrip()
    words = line.split("\t")
    entity = words[0]
    category = words[1]
    if category == target_category:
        category_entity_set.add(entity)
category_file.close()

target_file = open(TARGET_INFOBOX_PATH, 'w')
infobox_file = open(INFOBOX_PATH, 'r')
infobox_lines = infobox_file.readlines()
for line in infobox_lines:
    line = line.rstrip()
    words = line.split("\t")
    if words[0] in category_entity_set:
        target_file.write("%s\t%s\t%s\n" %(words[0], words[1], words[2]))
