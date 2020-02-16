import os
import sys
import json
import matplotlib.pyplot as plt
from datetime import datetime


def lineEquation(x, slope, coffe):
    y = list()
    for value in x:
        y.append(100 + (slope*10*value) + coffe)
    
    return y


def main():    
    yAxis = [69, 63, 63, 68, 61, 64, 69, 65, 60, 60]
    xAxis = list(range(1,len(yAxis)+1))
    print(xAxis, yAxis)

    line = lineEquation(xAxis, -0.5212, -0.52121212)

    print(line)

    #plt.scatter(xAxis, yAxis)
    plt.plot(xAxis,yAxis,'o', xAxis, line)
    plt.show()


if __name__ == "__main__":
    # Initialize the Start Variable
    startTime = datetime.now()

    # Call Master Function
    main()

    # Total Time Taken for Script
    print("-- --")
    print("Total time taken for the Script (HH:MM:SS:MS): ", datetime.now() - startTime)