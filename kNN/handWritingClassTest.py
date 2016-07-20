# -*- coding: UTF-8 -*-
from kNN import *
import matplotlib
import matplotlib.pyplot as plt
from os import listdir

def handWritingClassTest():
    hwLabels = []
    trainingFileList = listdir('trainingDigits')
    m = len(trainingFileList)
    trainMat = zeros((m,1024))
    for i in range(m):
        filename = trainingFileList[i]
        num = filename.split('_')[0]
        hwLabels.append(int(num))
        vector = img2vector('trainingDigits/'+filename)
        trainMat[i,:] = vector

    testFileList = listdir('testDigits')
    errnum = 0
    n = len(testFileList)
    for i in range(n):
        filename = testFileList[i]
        num = filename.split('_')[0]
        label = int(num)
        vector = img2vector('testDigits/'+filename)
        classResult = classify0(vector,trainMat,hwLabels,3)
        print 'the item of class is %d and classed to %d' % (label, classResult)
        if(label!=classResult):
            errnum += 1
    print "err is %.2f%%" % (((errnum / float(n)) * 100))

handWritingClassTest()