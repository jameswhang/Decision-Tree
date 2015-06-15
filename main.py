#!/usr/bin/python

# main.py
# main logic that puts together everything and handles the IO
# written by James Whang

import sys
import csv
import train
import validate
import prune
import pickle

# main function
def main():
    if len(sys.argv) < 2:
        WrongUsage()
        sys.exit()
    else:
        trainFile = sys.argv[1]
        printIntro()
        readResult = readDataFromFile(trainFile, False)
        trainData = readResult[0]
        attrDict = readResult[1]
        targetLabelList = readResult[2]

        attributeList = attrDict.keys()

        tTree = train.GenerateDTree(trainData, attributeList, attrDict, targetLabelList)

        saveTree = raw_input('Finished generating the tree! Would you like to save it? [y/n]    ').replace('\n', '')
        if saveTree == 'y':
            how = raw_input('How should I save the tree?\n [p: Python object form    t: text file]      ').replace('\n', '')
            if how == 'p':
                with open('tree.pkl', 'wb') as output:
                    pickle.dump(tTree, output, pickle.HIGHEST_PROTOCOL)
            elif how == 't':
                    oStream = raw_input('Enter the name of the text file (WARNING: This may take a while):        ')
                    tTree.saveTree(oStream)

        doPruning = raw_input('Do you want to prune the tree? [y/n]     ').replace('\n', '')
        if doPruning == 'y':
            prune.pruneWrapper(tTree.info, trainData, targetLabelList, attrDict)
            print 'Pruning complete. All validation will be done with the pruned tree'
        doValidate = raw_input('Do you want to validate the generated tree? [y/n]        ').replace('\n', '')
        if doValidate == 'y':
            how = raw_input('How would you like to validate it?\n[1: n-fold cross-validation    ' +
                            '2: with a validation file        ')
            if how == '1':
                N = int(raw_input('What is N?    '))
                validate.nFold(trainData[0:1000], targetLabelList[0:1000], attrDict, N)
            else:
                vFilepath = raw_input('Where is it?        ').replace('\n', '')
                vFileRead = readDataFromFile(vFilepath, True)
                validData = vFileRead[0]
                vLabelList = vFileRead[2]
                validate.validate(tTree, trainData, vLabelList, attrDict)

        print "Bye!"

# readInput
def readDataFromFile(filepath, v):
    inputFile = sys.argv[1]
    inputFileContent = open(inputFile)
    firstLine = True
    attrDict = {}
    dataList = []
    targetLabelList = []
    attr_keys = []
    for line in inputFileContent:
        if firstLine:
            attrs = line.split(',')
            for attr in attrs:
                if attr == attrs[len(attrs) - 1]:
                    break
                attr = attr.replace('\n', '').replace(' ', '')
                while True:
                    attrType = raw_input('Found a new attribute <' + attr +
                                        '>. Type? [c: continuous (numeral), ' +
                                        'd: discrete(nominal)] : ')
                    attrType = attrType.replace('\n', '')
                    if attrType == 'c' or attrType == 'd':
                        break
                    else:
                        print "Wrong entry. Only type c or d"
                attrDict[attr] = attrType
                attr_keys.append(attr)
            firstLine = False
            continue
        line = line.replace('\n', '')
        newData = line.split(',')
        i = 0
        newDict = {}
        doAppend = True
        for data in newData:
            if i == (len(newData) - 1):
                if newData[i] == '?':
                    doAppend = False
                else:
                    targetLabelList.append(int(newData[i]))
                break
            if newData[i] == '?':
                newDict[attr_keys[i]] = newData[i]
            else:
                newDict[attr_keys[i]] = float(newData[i])
            i += 1
        if doAppend:
            dataList.append(newDict)
    dataList = preprocessData(dataList, attrDict)
    return [dataList, attrDict, targetLabelList]


# preProcess
def preprocessData(allDataSet, attrDict):
    newDataSet = []
    averages = {}
    mcvs = {}
    #print allDataSet
    for entry in allDataSet:
        #print entry
        entry = entry.copy()
        for key in entry.keys():
            if entry[key] == '?':
                if attrDict[key] == 'c':
                    if key in averages.keys():
                        entry[key] = averages[key]
                    else:
                        avg = findAverage(allDataSet, key)
                        averages[key] = avg
                        entry[key] = avg
                else:
                    if key in mcvs.keys():
                        entry[key] = mcvs[key]
                    else:
                        mcv = mostCommonValue(allDataSet, key)
                        mcvs[key] = mcv
                        entry[key] = mcv
        #print entry
        newDataSet.append(entry)
    writer = csv.writer(open('ppdata.csv', 'wb'))
    for entry in newDataSet:
        for key, value in entry.items():
            writer.writerow([key, value])
    return newDataSet


def mostCommonValue(allDataSet, key):
    countDict = {}
    for entry in allDataSet:
        for entryKey in entry.keys():
            if entryKey == key and entry[key] != '?':
                if entry[key] in countDict.keys():
                    countDict[entry[key]] += 1
                else:
                    countDict[entry[key]] = 1
    maxCount = 0
    mcv = ''
    for k in countDict.keys():
        if countDict[k] > maxCount:
            mcv = k
            maxCount = countDict[k]
   # print countDict
    #print maxCount
    return mcv


def findAverage(allDataSet, key):
    sumValue = 0
    unknowns = 0
    for entry in allDataSet:
        for entryKey in entry.keys():
            if entryKey == key:
                val = entry[key]
                if val == '?':
                    unknowns += 1
                else:
                    sumValue += val
    return sumValue/(len(allDataSet)-unknowns)


# wrong usage
def WrongUsage():
    print "Usage: ./ps2 [training_file_path]"

def printIntro():
    print "########################################"
    print "#      EECS 349 : Machine Learning     #"
    print "#       Written by : James Whang       #"
    print "#     Decision Tree Implementation     #"
    print "########################################"

if __name__ == '__main__':
    main()
