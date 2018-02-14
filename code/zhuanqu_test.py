<<<<<<< HEAD
##################

# @Author:             Chenxin Ma
# @Email:              machx9@gmail.com
# @Date:               2018-02-02 17:58:59
# @Last Modified by:   schemmy
# @Last Modified time: 2018-02-13 19:22:28

##################


from os import listdir
from os.path import isdir, join
import pandas as pd
import csv,codecs


def get_score(row):
    if row['poster'] == 'Y':
        return 5
    else:
        return 1

def combine_teams():
    path = '../data/'
    folders = [f for f in listdir(path) if isdir(join(path, f))]

    files = [path+i+'/'+f for i in folders for f in listdir(path+i) if not f.startswith('.')]


    count = 0
    for f in files:
        o = pd.read_csv(f, sep=',',
                    names=['poster', 'ids', 'name', 'url'])

        o['sc'] = o.apply(lambda row: get_score(row), axis=1)
        o1 = o.groupby(['ids']).sum()
        o2 = o1.sort_values(['sc'], ascending=[0])
        o2['team'] = f.split('/')[-1].split('.')[0]
        o3 = o2[o2['sc'] >= 3]
        count += 1
        if count == 1:
            o_entire = o3
        else:
            o_entire = pd.concat([o_entire, o3])
        # print (o3)
        # print (len(o), len(o3), f)

    o_entire.to_csv('../data/zhuanqu.csv', header=False)
    #61062 50564
    o = pd.read_csv('../data/zhuanqu.csv', sep=',', names=['ids', 'sc', 'team'])
    o = o.sort_values(['ids'])
    print (len(o), len(set(o['ids'])))
    o.to_csv('../data/zhuanqu.csv', header=False, index=False)


def build_network():

    path = '../data/'
    folders = [f for f in listdir(path) if isdir(join(path, f))]
    files = [f.split('.')[0] for i in folders for f in listdir(path+i) if not f.startswith('.')]

    dic = {}
    for i in range(len(files)):
        dic[files[i]] = i

    print (dic)
    count = len(dic)
    o = pd.read_csv('../data/zhuanqu.csv', sep=',', names=['ids', 'sc', 'team'])    
    for index, row in o.iterrows():
        if row['ids'] not in dic:
            dic[row['ids']] = count
            count += 1
     
    network = {}
    for index, row in o.iterrows():
        network[dic[row['team']]] = network.get(dic[row['team']], []) + [str(dic[row['ids']])]
        network[dic[row['ids']]] = network.get(dic[row['ids']], []) + [str(dic[row['team']])]

    txt = open('../data/network.txt', 'w')
    for i in range(len(network)):
        txt.write(str(i) + ',')
        txt.write(','.join(network[i]))
        txt.write('\n')
    txt.close()
 

def node_txt():
    path = '../data/'
    folders = [f for f in listdir(path) if isdir(join(path, f))]
    files = [f.split('.')[0] for i in folders for f in listdir(path+i) if not f.startswith('.')]

    f = codecs.open('../data/node.csv', 'w') 
    writer = csv.writer(f) 
    txt = open('../data/network.txt', 'r')
    writer.writerow(['Id','Label','Discipline','counts'])
    i = 0
    for line in txt:
        if i < 19:
            cat = 'football'
        else:
            cat = 'nba'
        line = [str(i), files[i], cat, str(len(line.split(','))-1)]
        writer.writerow(line)
        i += 1
        if i == len(files):
            break
    f.close()


def edge_txt():

    txt = open('../data/edge.txt', 'r')
    f = codecs.open('../data/edge.csv', 'w') 
    writer = csv.writer(f)     
    writer.writerow(['Source','Target','Weight','Type'])

    for line in txt:
        l = line.split(',') + ['Directed']
        writer.writerow(l)
    
    f.close()
    

# combine_teams()
# build_network()
node_txt()
# edge_txt()