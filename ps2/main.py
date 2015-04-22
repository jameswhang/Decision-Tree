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
        inputFileContent = open(inputFile).read()


# wrong usage
def WrongUsage():
    print "Usage: ./ps2 -f [input_file_path] -o [output_file_path] "


if __name__ == '__main__':
    main()
