#-*- coding:UTF-8 -*-
'''
Created on 2013-12-3

@author: Bo Xu <mailto:bolang1988@gmail.com>

@version: 1.0

@summary: 从大的集合schema ensemble中找到几个样本category的schema

input:

    schema ensemble: (category, attribute, ratio) split with "\t"

    sample category string:  category list
                    (String Type, split with ",". e.g.:"电视剧，歌手")

output:

    sample schema:  (category, attribute, ratio) split with "\t"

e.g.:

    schema ensemble file:

             歌唱组合    国籍    0.666666666667
            歌唱组合    宣传公司    0.333333333333
            歌唱组合    代表作品    0.666666666667
            歌唱组合    民族    0.333333333333
            歌姬    姓名    0.375
            歌姬    出生地    0.625
            歌姬    别名    0.375
            歌姬    代表作品    0.5
            歌姬    主要成就    0.375
            电视剧    编剧    0.488944409744
            电视剧    主演    0.794378513429
            电视剧    上映时间    0.590630855715
            电视剧    出品时间    0.411617738913
            电视剧    类型    0.706933166771
            歌手    体重    0.204231311707
            歌手    出生地    0.788434414669
            歌手    身高    0.312552891396
            歌手    出生日期    0.844569816643
            歌手    经纪公司    0.407616361072
    --end--

    sample category string:

            电视剧,歌手
    --end--

    sample schema:

            电视剧    编剧    0.488944409744
            电视剧    主演    0.794378513429
            电视剧    上映时间    0.590630855715
            电视剧    出品时间    0.411617738913
            电视剧    类型    0.706933166771
            歌手    体重    0.204231311707
            歌手    出生地    0.788434414669
            歌手    身高    0.312552891396
            歌手    出生日期    0.844569816643
            歌手    经纪公司    0.407616361072
    --end--

'''

class SampleSchema(object):
    '''Find sample schema from schema ensemble using sample category'''

    category_list = None  #sample category list, convert from category string

    def __init__(self,schema_ensemble_path, \
                 sample_category_string,sample_schema_path):

        self.category_list = sample_category_string.split(",")
        print self.category_list
        self.print_infomation()
        self.write_sample_schema(schema_ensemble_path,sample_schema_path)

    def write_sample_schema(self,schema_ensemble_path,sample_schema_path):
        '''Write sample schema to file'''
        schema_ensemble_file = open(schema_ensemble_path,'r')
        sample_schema_file = open(sample_schema_path,'w')
        schema_ensemble_lines = schema_ensemble_file.readlines()
        for line in schema_ensemble_lines:
            try:
#                 print line
                words = line.split("\t")
                if words[0] in self.category_list:
                    sample_schema_file.write(line)
            except IOError:
                print line
        schema_ensemble_file.close()
        sample_schema_file.close()

    def print_infomation(self):
        '''print sample task'''
        print "find %s sample schema from schema ensemble" \
        % ",".join(self.category_list)

if __name__ == "__main__":
    MENU_PATH = "H://xubo//baidu4//"
    SCHEMA_ENSEMBLE_PATH = MENU_PATH + "baidu_schema_refinered.txt"
    SAMPLE_CATEGORY_STRING = "电视剧,歌手"
    SAMPLE_SCHEMA_PATH = MENU_PATH + "sample_baidu_schema_refinered.txt"
    TEST = SampleSchema(SCHEMA_ENSEMBLE_PATH, \
                         SAMPLE_CATEGORY_STRING, SAMPLE_SCHEMA_PATH)
