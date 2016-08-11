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

def bagOfWords2Vec(vocabList, inputSet):
    returnVec = [0] * len(vocabList)
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)] += 1
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
    if p1>p0:
        return 1
    else:
        return 0

def textParse(bigString):
    import re
    listOfTokens = re.split(r'\W*',bigString)
    return [tok.lower() for tok in listOfTokens if len(tok) > 2]

def calcMostFreq(vocabList,fullText):
    import operator
    freqDict = {}
    for item in vocabList:
        freqDict[item] = fullText.count(item)
    sortedFreq = sorted(freqDict.iteritems(),key=operator.itemgetter(1),reverse=True)
    return sortedFreq[:200]

def localWords(feed1,feed0):
    import feedparser
    docList=[]; classList=[]; fullText=[];
    minLen = min(len(feed0['entries']),len(feed1['entries']))
    for i in range(minLen):
        wordList = textParse(feed0['entries'][i]['summary'])
        docList.append(wordList)
        classList.append(0)
        fullText.extend(wordList)
        wordList = textParse(feed1['entries'][i]['summary'])
        docList.append(wordList)
        classList.append(1)
        fullText.extend(wordList)
    vocabList = createVocabList(docList)
    top30words = calcMostFreq(vocabList,fullText)
    for pairw in top30words:
        if pairw[0] in vocabList: vocabList.remove(pairw[0])
    trainingSet=range(2*minLen);testSet=[]
    for i in range(20):
        randIndex = int(random.uniform(0,len(trainingSet)))
        testSet.append(trainingSet[randIndex])
        del(trainingSet[randIndex])
    trainMat=[];trainClasses=[]
    for docIndex in trainingSet:
        trainMat.append(bagOfWords2Vec(vocabList,docList[docIndex]))
        trainClasses.append(classList[docIndex])
    p0v,p1v,pa = trainNB0(trainMat,trainClasses)
    errcnt = 0
    for docIndex in testSet:
        wordsVec = bagOfWords2Vec(vocabList,docList[docIndex])
        if classList[docIndex] != classifyNB(wordsVec,p0v,p1v,pa):
            errcnt+=1
    print 'the error rate is :',float(errcnt)/len(testSet)
    return vocabList, p0v, p1v

def getTopWords(ny,sf):
    import operator
    vocabList,p0v,p1v = localWords(ny,sf)
    topNY=[]; topSF=[];
    for i in range(len(p0v)):
        if p0v[i]>-4.5 : topSF.append((vocabList[i],p0v[i]))
        if p1v[i]>-4.5 : topNY.append((vocabList[i],p1v[i]))
    sortedSF = sorted(topSF,key=operator.itemgetter(1),reverse=True)
    sortedNY = sorted(topNY, key=operator.itemgetter(1), reverse=True)
    print 'sfsfsfsfsfsfsfs'
    for item in sortedSF:
        print item[0]
    print 'nynynynynynynnynynynyn'
    for item in sortedNY:
        print item[0]


def spamTest():
    docList = []; classList = []; fullText = []
    for i in range(1,26):
        wordList = textParse(open('email/spam/%d.txt' %i).read())
        docList.append(wordList)
        fullText.extend(wordList)
        classList.append(1)
        wordList = textParse(open('email/ham/%d.txt' %i).read())
        docList.append(wordList)
        fullText.extend(wordList)
        classList.append(0)
    vocabList = createVocabList(docList)
    trainingSet = range(50); testSet=[]
    for i in range(10):
        randIndex = int(random.uniform(0,len(trainingSet)))
        testSet.append(trainingSet[randIndex])
        del(trainingSet[randIndex])
    trainMat=[];trainClasses=[]
    for docIndex in trainingSet:
        trainMat.append(setOfWords2Vec(vocabList,docList[docIndex]))
        trainClasses.append(classList[docIndex])
    p0v,p1v,pa=trainNB0(trainMat,array(trainClasses)) #need exchange to array
    errorcnt = 0
    for docIndex in testSet:
        wordVec = setOfWords2Vec(vocabList,docList[docIndex])
        if classifyNB(wordVec,p0v,p1v,pa) != classList[docIndex]:
            errorcnt+=1
            print docList[docIndex]
    print 'the error rate is : ',float(errorcnt)/len(testSet)

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
    testEntry = ['stupid','stupid']
    thisDoc = array(setOfWords2Vec(vocabList, testEntry))
    print testEntry, 'class as ', classifyNB(thisDoc, p0v, p1v, pa)


def testRss():
    import feedparser
    ny=feedparser.parse('http://newyork.craigslist.org/stp/index.rss')
    sf = feedparser.parse('http://sfbay.craigslist.org/stp/index.rss')
    # vocabList,pny,psf = localWords(ny,sf)
    # vocabList,pny,psf = localWords(ny,sf)
    getTopWords(ny,sf)
#spamTest()
testRss()