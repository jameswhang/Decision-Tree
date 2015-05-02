# model-train.py
# generates a decision tree based on training set of data
# uses the ID3 Algorithm (1997 Mitchell)
# written by James Whang

from __future__ import division
import sys
from math import log
from collections import namedtuple
import pprint
import threading

DTreeNode = namedtuple("BTreeNode", "sign")


# CLASS DTREENODE
class dTreeNode():
    def __init__(self, label='none'):
        self.info = {}
        self.info['label'] = label
        self.info['branch'] = {}

    def setLabel(self, label):
        self.info['label'] = label

    def addBranch(self, cond, subtree=''):
        #subtree.printTree
        self.info['branch'][cond] = subtree.info

    def setDecision(self, bestA):
        self.info['decision'] = bestA

    #def setSubset(self, subset):
    #    self.info['subset'] = subset

    def saveTree(self, oStream):
        fout = open(oStream, 'w')
        pp = pprint.PrettyPrinter(indent=4, stream=fout)
        #pprint(self.info, fout)
        pp.pprint(self.info)

    def validate(self, vData, attrDict):
        valueList = []
        for entry in vData:
            val = self.traverse(entry, self.info, attrDict)
            #if val == None:
            #    val = 0
            valueList.append(val)
        return valueList

    def traverse(self, entry, root, attrDict):
        if len(root['branch'].keys()) == 0:
            target = root['label']
            print root
            print "################## "
            print "#### FINISHED #### "
            print "# LABEL : " + str(root['label']) + " #"
            print "################## "
            return target
        else:
            print root['decision']
            val = entry[root['decision']]
            #print root['decision']
            if attrDict[root['decision']] == 'c':
                conds = root['branch'].keys()
                conds.sort()
                for i in range(len(conds)):
                    if i == len(conds) - 1:
                        print 'taking this cond'
                        print root['branch']
                        return self.traverse(entry, root['branch'][conds[i]], attrDict)
                    elif i == 0 and val < conds[0]:
                        return self.traverse(entry, root['branch'][conds[0]], attrDict)
                    elif val > conds[i] and conds[i+1] > val:
                        return self.traverse(entry, root['branch'][conds[i]], attrDict)
            else:
                for cond in root['branch'].keys():
                    if val == cond:
                        return self.traverse(entry, root['branch'][cond], attrDict)

threadLock = threading.Lock()
g_gain = {}

class myThread(threading.Thread):
    def __init__(self, threadID, dataSet, attr, attrDict, valueList):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.data = dataSet
        self.attr = attr
        self.attrDict = attrDict
        self.valueList = valueList

    def run(self):
        findGainThreads(self.data, self.attr, self.attrDict, self.valueList)



def findGainThreads(data, attr, attrDict, valueList):
    global g_gain
    threadLock.acquire()
    g_gain[attr] = Gain(data, attr, attrDict, valueList)
    threadLock.release()


# GenerateDTree
# Generates a Decision Tree
# @param:
#   dataset -> a list of dictionary containing training data
#   attributes -> a dictionary containing the attributes and the type
def GenerateDTree(dataset, attrList, attrDict, valueList):
    root = dTreeNode()
    if allPositive(valueList):
        root.setLabel(1)
        return root
    elif allNegative(valueList):
        root.setLabel(0)
        return root

    if len(attrList) == 0:  # or len(dataset)minimum allowed per branch
        MCV = mostCommonValue(valueList)
        return dTreeNode(MCV)

    bestAttr = bestAttribute(dataset, attrList, attrDict, valueList)

    if bestAttr == '':
        bestAttr = attrList[0]  # Choosing arbitrary value when there isn't any.

    root.setDecision(bestAttr)
    if attrDict[bestAttr] == 'c':
        subsets, knownVals = makeSubsetsContinuous(dataset, bestAttr, 3)
    else:
        subsets, knownVals = makeSubsetsDiscrete(dataset, bestAttr)

    for possibleVal in subsets.keys():
        newAttrList = []
        for val in attrList:
            newAttrList.append(val)

        if len(subsets[possibleVal]) != 0:
            newSet = []
            newValList = []
            for i in subsets[possibleVal]:
                newSet.append(dataset[i])
                newValList.append(valueList[i])
            if bestAttr in newAttrList:
                newAttrList.remove(bestAttr)
            newNode = GenerateDTree(newSet, newAttrList, attrDict, newValList)
            root.addBranch(possibleVal, newNode)
        else:
            MCV = mostCommonValue(valueList)
            newNode = dTreeNode(MCV)
            root.addBranch(possibleVal, newNode)


    return root


# bestAttribute
# Calculates the best attribute
# @param:
#   dataset-> a list of dictionary containing the training data
#   attrDict -> a dictionary containing the attirubtes and their type
#   valueList -> a list of values of the classification
# @ret:
#   bAttr -> the best attribute (string)
def bestAttribute(dataset, attrList, attrDict, valueList):
    global g_gain
    attrDict = attrDict.copy()
    maxGain = 0
    bAttr = ""
    threads = []
    for i in range(len(attrList)):
        threads.append(myThread(i, dataset, attrList[i], attrDict, valueList))

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    for attr in g_gain.keys():
        if g_gain[attr] > maxGain:
            bAttr = attr
            maxGain = g_gain[attr]

    g_gain = {}
    return bAttr


# Entropy
# Calculates the entropy of a set
def Entropy(listAttr, listValue):
    pPos = positiveProp(listAttr, listValue)
    pNeg = negativeProp(listAttr, listValue)
    if pPos == 0 and pNeg == 0:
        print listAttr
        print listValue
        print pPos
        print pNeg
    if pPos == 0:
        return pNeg * -1 * log(pNeg, 2)
    elif pNeg == 0:
        return pPos * -1 * log(pPos, 2)
    else:
        return pPos * -1 * log(pPos, 2) + pNeg * -1 * log(pNeg, 2)


# Gain
# Computes the gain of an attribute
# @param
#   S -> Set of data (given as a list of dictionary)
#   attr -> attribute (given as string)
def Gain(S, attr, attrDict, listValue):
    attrDict = attrDict.copy()
    e1 = Entropy(S, listValue)
    sumSubsetEntropy = 0
    if attrDict[attr] == 'd':
        subsets, knownVals = makeSubsetsDiscrete(S, attr)
        for i in knownVals.keys():
            p_i = knownVals[i] / len(S)
            s_i = []
            val_i = []
            for index in subsets[i]:
                s_i.append(S[index])
                val_i.append(listValue[index])
            ent_i = Entropy(s_i, val_i)
            sumSubsetEntropy += (ent_i * p_i)
        return e1 - sumSubsetEntropy
    else:
        subsets, knownVals = makeSubsetsContinuous(S, attr, 3)
        for i in knownVals.keys():
            p_i = knownVals[i] / len(S)
            s_i = []
            val_i = []
            for index in subsets[i]:
                s_i.append(S[index])
                val_i.append(listValue[index])
            if len(s_i) != 0:
                ent_i = Entropy(s_i, val_i)
                sumSubsetEntropy += (ent_i * p_i)
        return e1 - sumSubsetEntropy


# makeSubsetsDiscrete
# Helper function that generates subsets to be put into IGain
# Works on discrete attributes only
# @param
#   S -> Set of data (given as an attribute
#   attr -> attribute (given as a string)
# @return
#   subsets
#   Dictionary of type:
#   value of attr -> list of indices of S matching this value
#   value of attr -> number of sets
def makeSubsetsDiscrete(S, attr):
    knownVals = {}
    subsets = {}
    i = 0
    for entry in S:
        entry = entry.copy()
        val = entry[attr]
        if val in knownVals.keys():
            knownVals[val] += 1
            subsets[val].append(i)
        else:
            knownVals[val] = 1
            subsets[val] = [i]
        i += 1
    return subsets, knownVals


# makeSubsetsContinuous
# Helper function that generates subsets to be put into IGain
# Works on discrete attributes only
# @param
#   S -> Set of data (given as an attribute
#   attr -> attribute (given as a string)
#   N -> Number of subsets (given as int)
# @return
#   subsets
#   Dictionary of type:
#   value of attr -> list of indices of S matching this value
#   value of attr -> number of sets
def makeSubsetsContinuous(S, attr, N):
    knownVals = {}
    subsets = {}
    i = 0
    minVal = sys.maxint
    maxVal = -sys.maxint+1
    for entry in S:
        val = entry[attr]
        if val < minVal:
            minVal = val
        if val > maxVal:
            maxVal = val
    thres = (maxVal - minVal) / N

    lowerBound = minVal
    bounds = []
    for i in range(N):
        subsets[lowerBound] = []
        knownVals[lowerBound] = 0
        bounds.append(lowerBound)
        lowerBound += thres

    j = 0
    for entry in S:
        entry = entry.copy()  # without this, Python modifies the dictionary
        val = entry[attr]
        for i in range(len(bounds)):
            if i == (len(bounds) - 1):
                subsets[bounds[i]].append(j)
                knownVals[bounds[i]] += 1
            elif val > bounds[i] and val < bounds[i+1]:
                subsets[bounds[i]].append(j)
                knownVals[bounds[i]] += 1
        j += 1

    return subsets, knownVals


# positiveProp
# calculates the proportion of positive examples in a set
# @param:
#   listAttr -> list of dictionary of attributes
# @return:
#   count -> double
def positiveProp(listData, valueList):
    count = 0
    tSize = len(listData)
    for i in range(len(listData)):
        if valueList[i] == 1:
            count += 1
    return count/tSize


# negativeProp
# calculates the proportion of negative examples in a set
# @param:
#   setAttr -> list of dictionary of attributes
# @return:
#   count -> integer
def negativeProp(listData, valueList):
    count = 0
    tSize = len(listData)
    for i in range(len(listData)):
        if valueList[i] == 0:
            count += 1
    return count/tSize


# Given a list of values, return True if they're all 1
# otherwise, return False
def allPositive(valueList):
    for i in range(len(valueList)):
        if valueList[i] != 1:
            return False
    return True


def allNegative(valueList):
    for i in range(len(valueList)):
        if valueList[i] != 0:
            return False
    return True


def mostCommonValue(valueList):
    values = {}
    for i in range(len(valueList)):
        item = valueList[i]
        if item in values.keys():
            values[item] = values[item] + 1
        else:
            values[item] = 0

    candidates = values.keys()
    MCV = 0
    maxCount = 0
    for i in range(len(candidates)):
        if maxCount < values[candidates[i]]:
            maxCount = values[candidates[i]]
            MCV = candidates[i]
    return MCV
