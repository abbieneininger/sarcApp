import numpy as np
import math

def calcSpacingMSF(numData, MSF, headerKeys, edgeX, edgeY):
    #set up arrays to hold data
    spacing = []
    persistenceLength = []
    sortedList = []
    lengths = []
    ZBodyCount = len(MSF)
    sortList = np.zeros((ZBodyCount, 2))
    #calculate initial slope
    X1 = numData[int(MSF[0]-1), headerKeys['x']]
    Y1 = numData[int(MSF[0]-1), headerKeys['y']]
    X2 = numData[int(MSF[ZBodyCount-1]-1), headerKeys['x']]
    Y2 = numData[int(MSF[ZBodyCount-1]-1), headerKeys['y']]
    if X2 == X1:
        X2+=0.001
    mM = (Y2-Y1)/(X2-X1)
    mB = Y1 - (mM*X1)
    #sort the Z bodies from left to right
    for b in range(ZBodyCount):
        length = numData[int(MSF[b]-1), headerKeys['length']]
        lengths.append(length)
        sortList[b,1] = int(MSF[b])
        BX1 = numData[int(MSF[b]-1), headerKeys['x']]
        BY1 = numData[int(MSF[b]-1), headerKeys['y']]
        distance = math.sqrt(BX1**2 + (BY1 - mB)**2)
        sortList[b,0] = distance
    sortedList = sortList[sortList[:,0].argsort()]
    #find center point of MSF
    centerIndex = int(ZBodyCount / 2)
    CX = numData[int(sortedList[centerIndex,1]-1), headerKeys['x']]
    CY = numData[int(sortedList[centerIndex,1]-1), headerKeys['y']]
    mCP = -1/(mM)
    bCP = CY - mCP*CX
    #calculate distance from the edge of the MSF
    mDistIdx = 0
    if edgeX is not False:
        for p in range(len(edgeX)-1):
            if edgeX[p+1] == edgeX[p]:
                edgeX[p+1] += 0.001
            mEdge = (edgeY[p+1]-edgeY[p])/(edgeX[p+1]-edgeX[p])
            bEdge = edgeY[p] - (mEdge*edgeX[p])
            intX = (bEdge-bCP) / (mCP-mEdge)
            intY = mEdge*intX + bEdge
            if (intX <= edgeX[p+1] and intX >= edgeX[p]):
                mDistIdx = p
        if mDistIdx > 0:
            mDist = math.sqrt((edgeX[mDistIdx]-CX)**2 + (edgeY[mDistIdx]-CY)**2)
        else:
            mDistIdxBeg = 0
            mDistIdxEnd = len(edgeX)-1
            mDistBeg = math.sqrt((edgeX[mDistIdxBeg]-CX)**2 + (edgeX[mDistIdxBeg]-CY)**2)
            mDistEnd = math.sqrt((edgeX[mDistIdxEnd]-CX)**2 + (edgeY[mDistIdxEnd]-CY)**2)
            mDist = min(mDistBeg, mDistEnd)
    else:
        mDist = 0
    #calculate spacing
    for s in range(ZBodyCount-1):
        BX1 = numData[int(sortedList[s,1]-1), headerKeys['x']]
        BY1 = numData[int(sortedList[s,1]-1), headerKeys['y']]
        BX2 = numData[int(sortedList[s+1,1]-1), headerKeys['x']]
        BY2 = numData[int(sortedList[s+1,1]-1), headerKeys['y']]
        spacing.append(math.sqrt((BY2-BY1)**2+(BX2-BX1)**2))
    persistenceLength = sum(spacing)
    return spacing, persistenceLength, lengths, mDist

def calcMSFs(numData, MSFs, headerKeys, edgeX, edgeY):
    MSFStats = np.zeros((len(MSFs), 6))
    cellStats = np.zeros((1,5))
    totalSpacing = np.array([])
    totalLengths = np.array([])
    if len(MSFs) > 1:
        for m in range(len(MSFs)):
            MSF = MSFs[m]
            spaceM, pLM, lengthM, mDist = calcSpacingMSF(numData, MSF, headerKeys, edgeX, edgeY)
            totalSpacing = np.append(totalSpacing, spaceM)
            totalLengths = np.append(totalLengths, lengthM)
            MSFStats[m,0] = m+1
            MSFStats[m,1] = len(MSF)
            if len(spaceM) > 0:
                MSFStats[m,2] = np.nanmean(spaceM)
            else:
                MSFStats[m,2] = float("NaN")
            if pLM > 0:
                MSFStats[m,3] = pLM
            else:
                MSFStats[m,3] = float("NaN")
            MSFStats[m,4] = np.mean(lengthM)
            MSFStats[m,5] = mDist
        cellStats[0,0] = len(MSFs)
        cellStats[0,1] = sum(MSFStats[:,1])
        cellStats[0,2] = np.nanmean(MSFStats[:,3])
        cellStats[0,3] = np.nanmean(totalLengths)
        cellStats[0,4] = np.nanmean(totalSpacing)
    else:
        cellStats[0,0] = 0
        cellStats[0,1] = 0
        cellStats[0,2] = float("NaN")
        cellStats[0,3] = float("NaN")
        cellStats[0,4] = float("NaN")
    #print(cellStats[0])
    return MSFStats, cellStats
