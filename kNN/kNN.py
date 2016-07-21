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


def file2matrix(filename):
    fr = open(filename)
    arrayOLines = fr.readlines()
    numOfLines = len(arrayOLines)
    returnMat = zeros((numOfLines, 3))
    classLabelVector = []
    index = 0

    for line in arrayOLines:
        line = line.strip()
        listLine = line.split('\t')
        returnMat[index, :] = listLine[0:3]
        classLabelVector.append(int(listLine[-1]))
        index += 1
    return returnMat, classLabelVector  # classLabelVector是一个numpy数组


def autoNorm(dataSet):
    minVals = dataSet.min(0)
    maxVals = dataSet.max(0)
    ranges = maxVals - minVals
    normDataSet = zeros(shape(dataSet))
    m = dataSet.shape[0]
    normDataSet = dataSet - tile(minVals, (m, 1))
    normDataSet = normDataSet / tile(ranges, (m, 1))
    return normDataSet, ranges, minVals


def img2vector(filename):
    retvec = zeros((1, 1024))
    fr = open(filename)
    for i in range(32):
        line = fr.readline()
        for j in range(32):
            retvec[0, i * 32 + j] = int(line[j])
    return retvec
# group, labels = createDataSet()
# print classify0([0, 0], group, labels, 3)
