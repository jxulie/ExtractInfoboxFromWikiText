#-*- coding:UTF-8 -*-
'''
Created on 2013-12-3

@author: Bo Xu <mailto:bolang1988@gmail.com>

@version: 1.0

@summary: test file

'''

import os.path

SCHEMA = "D:\\ASDF\\"
if not os.path.exists(SCHEMA):
    os.makedirs(SCHEMA)

TESTFILE = open(SCHEMA+"sdfd.txt",'w')
TESTFILE.write("hello word")
