from numpy import *
def loadDataSet():
    postingList = [['my', 'dog', 'has', 'flea', 'problems', 'help', 'please'],
                   ['maybe', 'not', 'take', 'him', 'to', 'dog', 'park', 'stupid'],
                   ['my', 'dalmation', 'is', 'so', 'cute', 'i', 'love', 'him'],
                   ['stop', 'posting', 'stupid', 'worthless', 'garbage'],
                   ['mr', 'licks', 'ate', ',my', 'steak', 'how', 'to', 'stop', 'him'],
                   ['quit', 'buying', 'worthless', 'dog', 'food', 'stupid']]
    classVec = [0, 1, 0, 1, 0, 1]
    return postingList, classVec


def createVocabList(dataSet):
    vocabList = set([])
    for document in dataSet:
        vocabList = vocabList | set(document)
    return list(vocabList)


def setOfWords2Vec(vocabList, inputSet):
    returnVec = [0] * len(vocabList)
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)] = 1
    return returnVec

def trainNB0(trainMatrix,trainCategory):
    numDocs = len(trainMatrix)
    numWords = len(trainMatrix[0])
    pa = sum(trainCategory)/float(numDocs)
    p0num = ones(numWords)
    p1num = ones(numWords)
    p0total = 2.0
    p1total = 2.0
    for i in range(numDocs):
        if trainCategory[i]==1:
            p1num += trainMatrix[i]
            p1total += sum(trainMatrix[i])
        else:
            p0num += trainMatrix[i]
            p0total += sum(trainMatrix[i])
    p0 = log(p0num/p0total)
    p1 = log(p1num/p1total)
    return p0,p1,pa

def classifyNB(vec2classify,p0vec,p1vec,pclass1):
    p1 = sum(vec2classify*p1vec) + log(pclass1)
    p0 = sum(vec2classify*p0vec) + log(1.0-pclass1)
    return p1,p0
'''   if p1>p0:
        return p
    else:
        return 0
'''
def testNB():
    posts,classes = loadDataSet()
    vocabList = createVocabList(posts)
    trainMat = []
    for doc in posts:
        trainMat.append(setOfWords2Vec(vocabList,doc))
    p0v,p1v,pa = trainNB0(trainMat,classes)
    testEntry =['love','my','dalmation']
    thisDoc = array(setOfWords2Vec(vocabList,testEntry))
    print testEntry,'class as ',classifyNB(thisDoc,p0v,p1v,pa)
    testEntry = ['stupid']
    thisDoc = array(setOfWords2Vec(vocabList, testEntry))
    print testEntry, 'class as ', classifyNB(thisDoc, p0v, p1v, pa)

testNB()