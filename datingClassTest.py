# -*- coding: UTF-8 -*-
from kNN import *
m,l = file2matrix('datingTestSet2.txt')
import matplotlib
import matplotlib.pyplot as plt
fig = plt.figure()
ax = fig.add_subplot(111)
m,ranges,minVals = autoNorm(m)
ax.scatter(m[:,0],m[:,1],20,15*array(l))#numpy数组不支持python数组操作，所以需要进行转换
plt.show()
