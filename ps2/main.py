#!/usr/bin/python

# main.py
# main logic that puts together everything and handles the IO
# written by James Whang

import sys
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
                firstLine = False
                continue
            line = line.replace('\n', '')
            newData = line.split(',')
            i = 0
            newDict = {}
            attr_keys = attributes.keys()

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
                allDataSet.append(newDict)
    # print allDataSet[0]
    print attributes
    # print valueList
    allDataSet = preprocessData(allDataSet)
    tree = train.GenerateDTree(allDataSet, attributes, valueList)
    print tree


# preProcess
def preprocessData(allDataSet):
    newDataSet = []
    for entry in allDataSet:
        for key in entry.keys():
            if entry[key] == '?':
                entry[key] = findAverage(allDataSet, key)
        newDataSet.append(entry)
    fa = open('ppdata.csv', 'w')
    fa.write(newDataSet)
    fa.close()
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
