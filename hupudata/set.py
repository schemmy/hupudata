#-*- coding=utf-8 -*-
##################

# @Author:             Chenxin Ma
# @Email:              machx9@gmail.com
# @Date:               2018-02-01 11:35:00
# @Last Modified by:   Chenxin Ma
# @Last Modified time: 2018-02-01 12:51:45

##################
import pandas as pd
import codecs


df = pd.read_csv('../hupu.csv', sep=',')

print (set(df['user'].values))