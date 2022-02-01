import numpy as np
import math
import os
from prepareData import prepareData
import csv 

def quickCalc(doublet, numData, headerKeys):
    #print(doublet)
    X1 = numData[int(doublet[0]-1),headerKeys['x']]
    Y1 = numData[int(doublet[0]-1),headerKeys['y']]
    X2 = numData[int(doublet[1]-1),headerKeys['x']]
    Y2 = numData[int(doublet[1]-1),headerKeys['y']]
    A1 = numData[int(doublet[0]-1),headerKeys['angle']]
    A2 = numData[int(doublet[1]-1),headerKeys['angle']]
    #print(X1,X2)
    spacing = math.sqrt((Y2-Y1)**2 + (X2-X1)**2)
    angleDiff = abs(A2-A1)
    return spacing, angleDiff

def main():
    dat_dir = "C:/Users/abbie/Documents/sarcApp/python/toy data/titin_dat"
    dat_samples = sorted(os.listdir(dat_dir))
    dat_path = os.path.join(dat_dir, dat_samples[0])
    numData, headerKeys = prepareData(dat_path)
    index = "C:/Users/abbie/Documents/sarcApp/python/toy data/test2.csv"
    with open(index, 'r', errors="ignore") as f:
        data = list(csv.reader(f))
    headers = np.array(data[0])
    index3 = np.array(data[1:]).astype(int)
    doubletIndices = np.unique(index3[:,1])
    doubletCount = 0
    doubletIdentities = []
    #print(doubletIndices)
    for k in range(len(doubletIndices)):
        kID = doubletIndices[k]
        #print(kID)
        if np.sum(index3[:,1]==kID) >= 2:
            doubletCount +=1
            lineIndices = np.where(index3[:,1] == kID)
            print(kID, lineIndices)
            lineIndices = lineIndices[0]
            lineIdentities = numData[index3[lineIndices,0],0]
            doubletIdentities.append(lineIdentities)
    for d in range(len(doubletIdentities)):
        doublet = doubletIdentities[d]
        spacing, angleDiff = quickCalc(doublet, numData, headerKeys)
        print(doublet, spacing, angleDiff)
    #print(doubletIdentities)

if __name__ == '__main__':
    main()