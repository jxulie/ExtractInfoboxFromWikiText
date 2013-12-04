#-*- coding:UTF-8 -*-
'''
Created on 2013年12月4日

@author: Bo Xu <mailto:bolang1988@gmail.com>

@version: 1.0

@summary: test dir

对于中文文件需要加上decode("gb18030")

'''

import os

# filenames = os.listdir("G:\\xubo\\baidu4\\trainset1")
# for name in filenames:
# #     name = name.decode("gb18030")
#     file1 = open("G:\\xubo\\baidu4\\trainset1\\" + name,'r')
#     lines1 = file1.readlines()
#     print lines1[0]
# #     print filename.decode("utf-8")

file1 = open(r"G://xubo//baidu4//geshou//歌手_中文名",'r')
lines1 = file1.readlines()
print lines1[0]