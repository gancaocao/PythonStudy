# -*- coding: utf-8 -*-

from math import log
import operator
import treePlotter

# 计算香浓熵
def calcShannonEnt(dataSet):
    num = len(dataSet)
    labelCount = {}
    for item in dataSet:
        curr = item[-1]
        if curr not in labelCount.keys():
            labelCount[curr] = 0
        labelCount[curr] += 1
    shannonEnt = 0.0
    for key in labelCount.keys():
        prop = float(labelCount[key]) / num
        shannonEnt -= prop * log(prop, 2)
    return shannonEnt


# 划分数据集
def splitDataSet(dataSet, axis, value):
    retDataSet = []
    for item in dataSet:
        if (item[axis] == value):
            retDataItem = item[:axis]
            retDataItem.extend(item[axis + 1:])
            retDataSet.append(retDataItem)
    return retDataSet


# 选择最优的划分特征
def chooseBestFeatureToSplit(dataSet):
    numFeatures = len(dataSet[0]) - 1
    baseEntropy = calcShannonEnt(dataSet)
    bestInfoGain = 0.0
    bestFeature = -1
    for i in range(numFeatures):
        featList = [example[i] for example in dataSet]  # 获取每个数据的第i个特征值
        newEntropy = 0.0
        featSet = set(featList)
        for value in featSet:
            splitedDataSet = splitDataSet(dataSet, i, value)
            prop = len(splitedDataSet) / float(len(dataSet))
            newEntropy += prop * calcShannonEnt(splitedDataSet)
        diff = baseEntropy - newEntropy
        print '%d diff %f' % (i, diff)
        if bestInfoGain <= diff:
            bestInfoGain = diff
            bestFeature = i
    return bestFeature


# 选择主要分类
def majorityCnt(classList):
    classCount = {}
    for item in classList:
        if item not in classCount.keys():
            classCount[item] = 0
        classCount[item] += 1
    sortedClassCount = sorted(classCount.iteritems(), key=operator.itemgetter(1), reverse=True)
    return sortedClassCount[0][0]


# 创建决策树
def createTree(dataSet, labels):
    classList = [example[-1] for example in dataSet]
    if classList.count(classList[0]) == len(classList):
        return classList[0]  # 所有的数据都是一个分类的
    if len(dataSet[0]) == 1:
        return majorityCnt(classList)  # 已经没有特征值进行分类的，使用多数服从少数的方式判断
    bestFeature = chooseBestFeatureToSplit(dataSet)
    bestFeatureLabel = labels[bestFeature]
    myTree = {bestFeatureLabel:{}}
    del (labels[bestFeature])
    bestFeatureList = [example[bestFeature] for example in dataSet]
    bestFeatureSet = set(bestFeatureList)
    for item in bestFeatureSet:
        subLabels = labels[:]#这里主要是为了不影响迭代时的labels
        myTree[bestFeatureLabel][item] = createTree(splitDataSet(dataSet, bestFeature, item), subLabels)
    return myTree


#对数据进行分类
def classfy(inputTree, featLabels, testVec):
    firstStr = inputTree.keys()[0]
    dict = inputTree[firstStr]
    featIndex = featLabels.index(firstStr)
    for key in dict.keys():
        if testVec[featIndex]==key:
            if type(dict[key]).__name__=='dict':
                classLabel = classfy(dict[key],featLabels,testVec)
            else:
                classLabel = dict[key]
            return classLabel


def test():
    dataSet = [[1, 1, 'yes'],
               [1, 1, 'yes'],
               [1, 0, 'no'],
               [0, 1, 'no'],
               [0, 1, 'no']]
    labels = ['no surfacing','flippers']
    featLabels = ['no surfacing','flippers']
    tree = createTree(dataSet,labels)
    print classfy(tree,featLabels,[1,1])

def test2():
    fr = open('lenses.txt')
    leses = [inst.strip().split('\t') for inst in fr.readlines()]
    lesesLabels=['age','prescript','astigmatic','tearRate']
    lesesTree = createTree(leses,lesesLabels)
    treePlotter.createPlot(lesesTree)
test2()
