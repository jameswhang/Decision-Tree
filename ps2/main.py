#!/usr/bin/python

# main.py
# main logic that puts together everything and handles the IO
# written by James Whang

import sys
import csv
import train
import validate

# main function
def main():
    if len(sys.argv) < 3:
        WrongUsage()
        sys.exit()
    elif sys.argv[1] != '-f':
        WrongUsage()
    else:
        inputFile = sys.argv[2]
        inputFileContent = open(inputFile)
        firstLine = True
        attributes = {}
        allDataSet = []
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
                                         '. Type? [n: numeral, ' +
                                         'm: nominal, v: value] : ')
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
                allDataSet.append(newDict)
    allDataSet = preprocessData(allDataSet, attributes)
    attributeList = attributes.keys()
    #tree = train.GenerateDTree(allDataSet[0:2000], attributeList, attributes, valueList[0:2000])
    #tree.saveTree()
    #print allDataSet[0:2]
    #c = validate.validate(tree, allDataSet[0:1000], valueList[0:1000], attributes)
    #print c
    validate.nFold(allDataSet[0:10000], valueList[0:10000], attributes, 10)

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
    print "Usage: ./ps2 -f [input_file_path] -o [output_file_path] "


if __name__ == '__main__':
    main()