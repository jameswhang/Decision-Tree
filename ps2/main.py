#!/usr/bin/python

# main.py
# main logic that puts together everything and handles the IO
# written by James Whang

import sys


# main function
def main():
    allDataSet = []
    if len(sys.argv) < 3:
        WrongUsage()
        sys.exit()
    elif sys.argv[1] != '-f':
        WrongUsage()
    else:
        inputFile = sys.argv[2]
        inputFileContent = open(inputFile)
        firstLine = True
        for line in inputFileContent:
            if firstLine:
                firstLine = False
                continue
            line = line.replace('\n', '')
            newData = line.split(',')
            newDict = {
                'winPercentageA': newData[0],
                'winPercentageB': newData[1],
                'weather': newData[2],
                'temperature': newData[3],
                'numInjuriesA': newData[4],
                'numInjuriesB': newData[5],
                'startPitcherA': newData[6],
                'startPitcherB': newData[7],
                'daysSinceLastGameA': newData[8],
                'daysSinceLastGameB': newData[9],
                'homeForA': newData[10],
                'runDifferentialA': newData[11],
                'runDifferentialB': newData[12],
                'winner': newData[13]
            }
            allDataSet.append(newDict)
    print allDataSet[0]


# wrong usage
def WrongUsage():
    print "Usage: ./ps2 -f [input_file_path] -o [output_file_path] "


if __name__ == '__main__':
    main()
