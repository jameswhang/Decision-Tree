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
    if len(sys.argv) < 3:
        WrongUsage()
        sys.exit()
    elif sys.argv[1] != '-t':
        WrongUsage()
    else:
        inputFile = sys.argv[2]
        inputFileContent = open(inputFile)
        firstLine = True
        attributes = {}
        trainData = []
        valueList = []
        attr_keys = []
        for line in inputFileContent:
            if firstLine:
                attrs = line.split(',')
                for attr in attrs:
                    if attr == attrs[len(attrs) - 1]:
                        break
                    attr = attr.replace('\n', '').replace(' ', '')
                    attrType = raw_input('Found an attr, ' + attr +
                                         '. Type? [c: continuous (numeral), ' +
                                         'd: discrete(nominal)] : ')
                    attr = attr.replace(' ', '')
                    attributes[attr] = attrType.replace('\n', '')
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
                        valueList.append(int(newData[i]))
                    break
                if newData[i] == '?':
                    newDict[attr_keys[i]] = newData[i]
                else:
                    newDict[attr_keys[i]] = float(newData[i])
                i += 1
            if doAppend:
                # print newDict
                trainData.append(newDict)
    trainData = preprocessData(trainData, attributes)
    attributeList = attributes.keys()

    tree = train.GenerateDTree(trainData, attributeList, attributes, valueList)
    
    saveTree = raw_input('Tree is generated! Would you like to save it? [y/n]').replace('\n', '')
    if saveTree == 'y':
        how = raw_input('How should I save the tree? [p: pickle (Python object form) t: text file').replace('\n', '')
        if how == 'p':
            with open('tree.pkl', 'wb') as output:
                pickle.dump(tree, output, pickle.HIGHEST_PROTOCOL)
        elif how == 't':
            oStream = raw_input('Enter the name of the result file: ')
            tree.saveTree(oStream)
    
    validate = raw_input('Do you want to validate it? [y/n]').replace('\n', '')
    if validate == 'y':
        how = raw_input('How would you like to validate it? [1: n-fold cross validation  2: with a validation set').replace('\n', '')
        if how == '1':
            N = int(raw_input('What is N?  '))
            validate.nFold(trainData, valueList, attributes, N)
        else:
            vFilepath = raw_input('Where is it?').replace('\n', '')
            vContent = open(vFilepath, 'rb')
            vData = []
            vValuelist = []
            firstLine = True
            for line in vContent:
                if firstLine:
                    pass
                else:
                    line = line.replace('\n', '')
                    newData = line.split(',')
                    i = 0
                    newDict = {}

                    doAppend = True
                    for data in vData:
                        if i == (len(vData) - 1):
                            if vData[i] == '?':
                                doAppend = False
                            else:
                                vValuelist.append(int(vData[i]))
                            break
                        if vData[i] == '?':
                            newDict[attr_keys[i]] = vData[i]
                        else:
                            newDict[attr_keys[i]] = float(vData[i])
                        i += 1
                    if doAppend:
                        # print newDict
                        vData.append(newDict)
            validate.validate(tree, vData, vValuelist)
    print 'BYE!'


# preProcess
def preprocessData(allDataSet, attrDict):
    newDataSet = []
    averages = {}
    mcvs = {}
    for entry in allDataSet:
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
    print "Usage: ./ps2 -t [training_file_path] -v [validate_file_path] "


if __name__ == '__main__':
    main()