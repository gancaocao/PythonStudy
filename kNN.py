# -*- coding: UTF-8 -*-
from numpy import *
import operator


def createDataSet():
    group = array([[1.0, 1.1], [1.0, 1.0], [0, 0], [0, 0.1]])
    labels = ['A', 'A', 'B', 'B']
    return group, labels


def classify0(inx, dataSet, labels, k):
    datasetsize = dataSet.shape[0]
    diffMat = tile(inx, (datasetsize, 1)) - dataSet
    sqDiffMat = diffMat ** 2
    sqDistances = sqDiffMat.sum(axis=1)  # axis=1表示行相加，axis=0列相加
    distance = sqDistances ** 0.5
    sortedDistIndicies = distance.argsort()
    classCount = {}

    for i in range(k):
        voteIlabel = labels[sortedDistIndicies[i]]  # 从距离最短的那个开始，直到第k个
        classCount[voteIlabel] = classCount.get(voteIlabel, 0) + 1
    sortedClassCount = sorted(classCount.items(), key=operator.itemgetter(1), reverse=True)
    m = classCount.items()
    return sortedClassCount[0][0]





def cll(x, dataSet, labels, k):
    nx = tile(x, (dataSet.shape[0], 1))
    diffxd = nx - dataSet
    diffxd = diffxd ** 2
    diffxd = diffxd.sum(axis=1)
    diffxd = diffxd ** 0.5
    diffsort = diffxd.argsort()

    data = {}  # tuple

    for i in range(k):
        v = labels[diffsort[i]]
        data[v] = data.get(v, 0) + 1
    rdata = sorted(data.iteritems(), key=operator.itemgetter(1), reverse=True)
    return rdata[0][0]

group, labels = createDataSet()
print classify0([0, 0], group, labels, 3)
