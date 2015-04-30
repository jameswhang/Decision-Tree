#!/usr/bin/python

# main.py
# main logic that puts together everything and handles the IO
# written by James Whang

import sys


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
                    attr = attr.replace('\n', '')
                    if attr == attrs[len(attrs) - 1]:
                        break
                    attrType = raw_input('Found an attr, ' + attr +
                                         '. Type? [n: numeral, ' +
                                         'm: nominal, v: value] : ')
                    attr = attr.replace(' ', '')
                    attributes[attr] = attrType
                firstLine = False
                continue
            line = line.replace('\n', '')
            newData = line.split(',')
            i = 0
            newDict = {}
            attr_keys = attributes.keys()
            for data in newData:
                if i == (len(newData) - 1):
                    valueList.append(newData[i])
                newDict[attr_keys[i]] = float(newData[i])
                i += 1
            # print newDict
            allDataSet.append(newDict)
    print allDataSet[0]
    print attributes
    print valueList


# wrong usage
def WrongUsage():
    print "Usage: ./ps2 -f [input_file_path] -o [output_file_path] "


if __name__ == '__main__':
    main()
