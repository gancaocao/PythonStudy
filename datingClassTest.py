# -*- coding: UTF-8 -*-
from kNN import *
import matplotlib
import matplotlib.pyplot as plt


def plotData(ratio):
    m, l = file2matrix('datingTestSet2.txt')
    fig = plt.figure()
    ax = fig.add_subplot(111)
    m, ranges, minVals = autoNorm(m)
    testNum = int(m.shape[0]*ratio)
    ax.scatter(m[testNum:, 0], m[testNum:, 1], 20, 15 * array(l[testNum:]))  # numpy数组不支持python数组操作，所以需要进行转换
    plt.show()


def datingClassTest(ratio):
    testRatio = ratio
    matrix, labels = file2matrix('datingTestSet2.txt')
    normMat, ranges, minVals = autoNorm(matrix)
    totalNum = normMat.shape[0]
    testNum = int(totalNum * testRatio)
    errcount = 0
    for i in range(testNum):
        classResult = classify0(normMat[i, :], normMat[testNum:, :], labels[testNum:], 4)
        print 'the item of class is %d and classed to %d' % (labels[i], classResult)
        if (classResult != labels[i]):
            errcount += 1
    print "err is %.2f%%" % (((errcount / float(totalNum)) * 100))

#plotData(0.1)
datingClassTest(0.1)
