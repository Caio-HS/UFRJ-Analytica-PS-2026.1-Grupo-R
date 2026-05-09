import csv

import sys

inputFile = sys.argv[1]
inputExtension = ".csv"
inputFilename = inputFile + inputExtension

with open(inputFilename, mode='r', encoding='utf-8') as file:
    csv_reader = csv.reader(file)
    next(csv_reader)

    init = next(csv_reader)
    xMax = xMin = float(init[2])
    yMax = yMin = float(init[3])

    for line in csv_reader:
        if not line:
            continue
        
        x = float(line[2])
        y = float(line[3])

        if(x < xMin):
            xMin = x

        if(x > xMax):
            xMax = x

        if(y < yMin):
            yMin = y

        if(y > yMax):
            yMax = y

    print(f"x Maxima: {xMax}")
    print(f"x Minima: {xMin}")
    print(f"y Maxima: {yMax}")
    print(f"y Minima: {yMin}")
