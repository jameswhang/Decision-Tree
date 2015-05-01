# model-train.py
# generates a decision tree based on training set of data
# uses the ID3 Algorithm (1997 Mitchell)
# written by James Whang

from __future__ import division
import sys
from math import log
from collections import namedtuple

DTreeNode = namedtuple("BTreeNode", "sign")


# CLASS DTREENODE
class dTreeNode():
    def __init__(self, label='none'):
        self.info = {}
        self.info['label'] = label
        self.info['children'] = []

    def addBranch(self, node):
        self.info['children'].append(node)

    def setDecision(self, bestA):
        self.info['decision'] = bestA


# GenerateDTree
# Generates a Decision Tree
# @param:
#   dataset -> a list of dictionary containing training data
#   attributes -> a dictionary containing the attributes and the type
def GenerateDTree(dataset, attrDict, valueList):
    print dataset
    print valueList
    if allPositive(valueList):
        return dTreeNode(1)
    elif allNegative(valueList):
        return dTreeNode(0)

    if len(attrDict) == 0:  # or len(dataset)minimum allowed per branch
        MCV = mostCommonValue(valueList)
        return dTreeNode(MCV)

    bestAttr = bestAttribute(dataset, attrDict, valueList)
    print bestAttr
    returnNode = dTreeNode()
    returnNode.setDecision(bestAttr)

    if attrDict[bestAttr] == 'c':
        subsets, knownVals = makeSubsetsContinuous(dataset, bestAttr, 10)
    else:
        subsets, knownVals = makeSubsetsDiscrete(dataset, bestAttr)

    for possibleVal in subsets.keys():
        if knownVals[possibleVal] != 0:
            newSet = []
            newValList = []
            for i in subsets[possibleVal]:
                newSet.append(dataset[i])
                newValList.append(valueList[i])
            newNode = GenerateDTree(newSet, attrDict, newValList)
            returnNode.addBranch(newNode)
    return returnNode


# bestAttribute
# Calculates the best attribute
# @param:
#   dataset-> a list of dictionary containing the training data
#   attrDict -> a dictionary containing the attirubtes and their type
#   valueList -> a list of values of the classification
# @ret:
#   bAttr -> the best attribute (string)
def bestAttribute(dataset, attrDict, valueList):
    print dataset
    print attrDict
    print "LOLOLOL"
    maxGain = 0
    bAttr = ""
    for attr in attrDict.keys():
        tGain = Gain(dataset, attr, attrDict, valueList)
        if abs(tGain) > abs(maxGain):
            bAttr = attr
            maxGain = tGain
    print bAttr
    return bAttr


# Entropy
# Calculates the entropy of a set
def Entropy(listAttr, listValue):
    pPos = positiveProp(listAttr, listValue)
    pNeg = negativeProp(listAttr, listValue)
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
        # N = int(raw_input('Found a continuous value for attribute' + attr +
                        #  '. How many subsets? '))
        subsets, knownVals = makeSubsetsContinuous(S, attr, 10)  # TODO FIX THIS
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
        if valueList[i] in values.keys():
            values[valueList[i]] = values[valueList[i]] + 1
        else:
            values[valueList[i]] = 0

    candidates = values.keys()
    MCV = values[candidates[0]]
    for i in range(len(candidates)):
        if MCV < values[candidates[i]]:
            MCV = values[candidates[i]]
    return MCV
