#-*- coding:UTF-8 -*-
'''
Created on 2013-12-3

@author: Bo Xu <mailto:bolang1988@gmail.com>

@version: 1.0

@summary: Training Data Construction

input:

    infobox:    (entity,attribute, value) split with "\t"

    category:   (entity, category) split with "\t"

    schema:   (category, attribute, ratio) split with "\t",
              ratio is the coverage of an attribute in the category
              It is optional

    article text:  pure text file in baidu baike(not include baike card)
                   divided into sentences

output:

    training data 1: (category, attribute, entity, value) split with "\t"

e.g.:

    infobox file
'''
