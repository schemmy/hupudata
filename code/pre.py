#-*- coding=utf-8 -*-
##################

# @Author:             Chenxin Ma
# @Email:              machx9@gmail.com
# @Date:               2018-02-01 11:35:00
# @Last Modified by:   Chenxin Ma
# @Last Modified time: 2018-02-01 20:46:00

##################
import pandas as pd
import codecs


# o = pd.read_csv('../hupu.csv', sep=',')


# print ('Consistency check: %s' %
# 	(len(set(o.iloc[:,0].values))+1 == len(o.iloc[:,0].values) ))


# o1 = o.dropna(axis=0, how='any')

# team_data = o1.iloc[:,1].values
# dic = {}
# with open('teams.txt', 'w') as f:
# 	for i in team_data:
# 		t = i.split('+')
# 		for o in t:
# 			dic[o] = dic.get(o, 0) + 1
# 		line = ','.join(t)
# 		f.write(line+'\n')

# dic = sorted(dic.items(), key=lambda x: x[1])

# print (dic)


# print (o1.iloc[:,1].values)


o = pd.read_csv('../data/arsenal.csv', sep=',',
				names=['poster', 'ids', 'name', 'url'])

print (len(o))
print (len(set(o['name'])))