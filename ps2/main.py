#!/usr/bin/python

# main.py
# main logic that puts together everything and handles the IO
# written by James Whang

import sys
import csv
import train

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
    # print allDataSet[0]
    # print attributes
    # print valueList
    allDataSet = preprocessData(allDataSet)
    attributeList = attributes.keys()
    # print attributeList
    tree = train.GenerateDTree(allDataSet, attributeList, attributes, valueList)
    tree.printTree()


# preProcess
def preprocessData(allDataSet):
    newDataSet = []
    averages = {}
    for entry in allDataSet:
        entry = entry.copy()
        for key in entry.keys():
            if entry[key] == '?':
                if key in averages.keys():
                    entry[key] = averages[key]
                else:
                    avg = findAverage(allDataSet, key)
                    averages[key] = avg
                    entry[key] = avg
                
        #print entry
        newDataSet.append(entry)
    writer = csv.writer(open('ppdata.csv', 'wb'))
    for entry in newDataSet:
        for key, value in entry.items():
            writer.writerow([key, value])
    return newDataSet


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
    return sumValue/len(allDataSet)


# wrong usage
def WrongUsage():
    print "Usage: ./ps2 -f [input_file_path] -o [output_file_path] "


if __name__ == '__main__':
    main()
