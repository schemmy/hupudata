import sys
from pyspark import SparkConf, SparkContext

import numpy as np
import scipy.sparse as sps
from pyspark.mllib.linalg import Vectors
from pyspark.mllib.linalg import SparseVector
from pyspark.mllib.regression import LabeledPoint
import csv
def parsePoint(line):
    line = line.split(',')
    label = int(line[0])
    linksTo = line[1:-1]
    
    NNZ = len(linksTo)
    index=[]
    values=[]
    dic={}
    for e in linksTo:
#         dic[int(e)] = 1/(NNZ+0.0)
        index+=[int(e)]
        values+=[1/(NNZ+0.0)]
    return LabeledPoint(int(label), SparseVector(NNZ,sorted(index),values))

def doMultiplication(labeledPoint):
    out=[] 
  
    label = labeledPoint.label
    sparseVector = labeledPoint.features
    
    if sparseVector.size > 0:
        ri = r[int(label)]
        value = ri*sparseVector.values[0]
        for rowId in sparseVector.indices:
            if rowId < totalPages:
                out+= [ [rowId,  value] ]

    return out   


if __name__ == "__main__":
    conf = SparkConf()
    conf.setAppName("SimRank")
    sc = SparkContext(conf=conf)
    batchsize = int(sys.argv[1])
    index = int(sys.argv[2])

    linkData = sc.textFile('catgoNetwork.txt').map(parsePoint)

    totalPages = linkData.map(lambda a: a.label).reduce(max)
    totalPages = int(totalPages+1)
    print "Total catogories ", totalPages

    for st in range(49):
        r=np.zeros(totalPages)
        r[st] = 1.0

        beta=0.8
        secondPart = r*(1-beta)
        linkdata.cache()  # to have faster computation  

        for it in xrange(10):  
            #print "Iteration ",it
            newdata = linkdata.flatMap(doMultiplication)           
            reducedData = newdata.reduceByKey(lambda a,b: a+b).collect()    
            r=np.zeros( totalPages )
            for k,v in reducedData:
                    r[k]=v*beta
            r = r + secondPart  

        rOrig = r.copy()
        B = np.zeros(49, int)
        for i in xrange(49):
            idx = np.argmax(r)
            B[i]=idx; 
            r[idx]=0

        edge = open('edge.txt', 'a')
        for i in xrange(49):
            if i==0:
                bm = rOrig[B[i]]
            if i>0 and B[i]<49:
                if rOrig[B[i]]> bm/300:
                    edge.write('%d,%d,%f\n' %(st, B[i], rOrig[B[i]]))
        edge.close()

