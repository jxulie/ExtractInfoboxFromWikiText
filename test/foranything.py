#-*- coding:UTF-8 -*-
'''
Created on 2013-12-3

@author: Bo Xu <mailto:bolang1988@gmail.com>

@version: 1.0

@summary: test file

'''

# import os.path
# 
# SCHEMA = "D:\\ASDF\\"
# if not os.path.exists(SCHEMA):
#     os.makedirs(SCHEMA)
# 
# TESTFILE = open(SCHEMA+"sdfd.txt",'w')
# TESTFILE.write("hello word")

# import re
# 
# pattern = "生日：([\\S]+)年"
# line = "生日：20394年 生日：20334年"
# extract_value = re.findall(pattern, line)
# if len(extract_value):
#     for value in extract_value:
#         print value

def lcs(value1, value2):
    lengths = [[0 for temp_j in range(len(value2)+1)] for temp_i in range(len(value1)+1)]
    # row 0 and column 0 are initialized to 0 already
    for temp_i, temp_x in enumerate(value1):
        for temp_j, temp_y in enumerate(value2):
            if temp_x == temp_y:
                lengths[temp_i+1][temp_j+1] = lengths[temp_i][temp_j] + 1
            else:
                lengths[temp_i+1][temp_j+1] = \
                    max(lengths[temp_i+1][temp_j], lengths[temp_i][temp_j+1])
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

print lcs("中国人物","中国是人")