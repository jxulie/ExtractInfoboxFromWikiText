#-*- coding:UTF-8 -*-
'''
Created on 2013-12-2

@author: Bo Xu <mailto:bolang1988@gmail.com>

@version: 1.0

@summary: 找到描述一个category的所有attribute

input:

    infobox:    (entity,attribute, value) split with "\t"

    category:   (entity, category) split with "\t"

    threshold:  real value between [0-1] which means that
                at least threshold*100% percent of the entities in the category
                that contains the attribute

output:

    refined schema: (category, attribute, ratio) split with "\t"

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

    threshold 0.6

    schema file

                公司        公司口号
                公司        公司名称
                公司        公司性质
    --end--
'''
from __future__ import division


class SchemaRefiner(object):
    '''Refine schema'''
    entity_attribute_dict = None    #key:entity
                                    #value:attribute
                                    #from infobox file
    category_entity_dict = None     #key:category
                                    #value:entity
                                    #from category file
    entity_categroy_dict = None #key:entity
                                #value:category
                                #from category file
    all_category_attribute_dict = None  #All
                                        #key:(category, attribute)
                                        #value:count
                                        #pairs
    category_attribute_dict = None  #Filtered
                                    #key:(category, attribute)
                                    #value:count
                                    #pairs
                                    #Count > Thresholds


    def __init__(self, infobox_path, category_path, threshold, schema_path):
        self.read_entity_attribute_dict_file(infobox_path)
        self.read_entity_category_file(category_path)
        self.count_category_attribute_pair()
        self.fliter_category_attribute_pair(threshold)
        self.write_category_attribute_pair(schema_path)

    def read_entity_attribute_dict_file(self, infobox_path):
        '''Get entity_attribute_dict from infobox file'''
        self.entity_attribute_dict = dict()
        eafile = open(infobox_path,'r')
        ealines = eafile.readlines()
        for ealine in ealines:
        #     print "each line", line1
            try:
                ealine = ealine.rstrip()
                words = ealine.split("\t")
                if words[0] not in self.entity_attribute_dict:
                    self.entity_attribute_dict[words[0]] = set()
                self.entity_attribute_dict[words[0]].add(words[1])
            except IOError:
                print ealine
        eafile.close()

    def read_entity_category_file(self, category_path):
        '''Get category_entity_dict and entity_categroy_dict
        from category file'''
        self.category_entity_dict = dict()
        self.entity_categroy_dict = dict()
        ecfile = open(category_path,'r')
        eclines = ecfile.readlines()
        for ecline in eclines:
        #     print "each line", line1
            try:
                ecline = ecline.rstrip()
                words = ecline.split("\t")
                if words[0] in self.entity_attribute_dict:
                    if words[1] not in self.category_entity_dict:
                        self.category_entity_dict[words[1]] = set()
                    self.category_entity_dict[words[1]].add(words[0])
                    if words[0] not in self.entity_categroy_dict:
                        self.entity_categroy_dict[words[0]] = set()
                    self.entity_categroy_dict[words[0]].add(words[1])
            except IOError:
                print ecline
        ecfile.close()

    def count_category_attribute_pair(self):
        '''Count all the(category,attribute) pairs'''
        self.all_category_attribute_dict = dict()
        print "entity_categroy_dict number is :", \
                        str(len(self.entity_categroy_dict))
        round_count = 0
        for k, vvvv in self.entity_categroy_dict.iteritems():
            round_count += 1
            print str(round_count)
            for caset in vvvv:
                for atset in self.entity_attribute_dict[k]:
                    if (caset, atset) not in self.all_category_attribute_dict:
                        self.all_category_attribute_dict[(caset, atset)] = 0
                    self.all_category_attribute_dict[(caset, atset)] += 1

    def fliter_category_attribute_pair(self, threshold):
        '''filter the(category,attribute) pairs
        with the count ratio > threshold'''
        self.category_attribute_dict = dict()
        for k, vvvv in self.all_category_attribute_dict.iteritems():
#             print k
#             print v
#             print self.category_entity_dict[k[0]]
#             print len(self.category_entity_dict[k[0]])

            attribute_ratio = vvvv/len(self.category_entity_dict[k[0]])
            if attribute_ratio > threshold:
#                 print k,str(attribute_ratio)
                self.category_attribute_dict[k] = attribute_ratio
    def write_category_attribute_pair(self, schema_path):
        '''write the filtered (category,attribute) pairs
        to schema file'''
        cafile = open(schema_path,'w')
        for k, vvvv in sorted(self.category_attribute_dict.iteritems(),
                          key = lambda d: d[0][0]):
            cafile.write("%s\t%s\t%s\n" %(k[0], k[1], str(vvvv)))

if __name__ == "__main__":
    INFOBOX_PATH = "D://xubo//baidu3//baiduinfobox_filter.txt"
    CATEGORY_PATH = "D://xubo//baidu3//baiducategory_filter10.txt"
    SCHEMA_PATH = "D://xubo//baidu3//baidu_schema_refinered.txt"
    THRESHOLD = 0.15
    TEST = SchemaRefiner(INFOBOX_PATH, \
                         CATEGORY_PATH, THRESHOLD, SCHEMA_PATH)
