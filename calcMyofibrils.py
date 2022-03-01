import numpy as np
import math

def calcSpacing(myofib, numData, headerKeys, edgeX, edgeY, xres, imgsize):
    spacing = []
    persistenceLength = []
    sortedList = []
    lengths = []
    lineCount = len(myofib)
    sortList = np.zeros((lineCount, 2))
    #calculate the initial basic slope and y-intercept of the myofibril
    X1 = numData[int(myofib[0]-1), headerKeys['x']]
    Y1 = numData[int(myofib[0]-1), headerKeys['y']]
    X2 = numData[int(myofib[lineCount-1]-1), headerKeys['x']]
    Y2 = numData[int(myofib[lineCount-1]-1), headerKeys['y']]
    mM = (Y2-Y1)/(X2-X1)
    mA = 180-np.rad2deg(np.arctan(mM))
    if mA >= 180:
            mA -= 180
    mB = Y1 - (mM*X1)
    #sort the z-lines from "left" to "right" in order
    for l in range(lineCount):
        length = numData[int(myofib[l]-1), headerKeys['length']]
        lengths.append(length)
        sortList[l,1] = int(myofib[l])
        LX1 = numData[int(myofib[l]-1), headerKeys['x']]
        LY1 = numData[int(myofib[l]-1), headerKeys['y']]
        distance = math.sqrt(LX1**2 + (LY1 - mB)**2)
        sortList[l,0] = distance
    sortedList = sortList[sortList[:,0].argsort()]
    #find the center point of the myofibril to calculate distance from the edge
    centerIndex = int(lineCount / 2)
    CX = numData[int(sortedList[centerIndex,1]-1), headerKeys['x']]
    CY = numData[int(sortedList[centerIndex,1]-1), headerKeys['y']]
    mCP = -1/(mM)
    bCP = CY - mCP*CX
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
    #print(sortedList)
    stackColumn = np.zeros((lineCount, 1))
    sortedList = np.hstack((sortedList, stackColumn))
    #print(sortedList)
    ln = 0
    stackID = 0
    while ln < lineCount-1:
        LX1 = numData[int(sortedList[ln,1]-1), headerKeys['x']]
        LY1 = numData[int(sortedList[ln,1]-1), headerKeys['y']]
        LX2 = numData[int(sortedList[ln+1,1]-1), headerKeys['x']]
        LY2 = numData[int(sortedList[ln+1,1]-1), headerKeys['y']]
        LA1 = numData[int(sortedList[ln,1]-1), headerKeys['angle']]
        if LX1 == LX2:
            LX2 +=0.001
        MC = (LY2-LY1) / (LX2-LX1)
        MA = 180-np.rad2deg(np.arctan(MC))
        if MA >= 180:
            MA -= 180
        if abs(MA-LA1) > 20:
            ln += 1
        else:
            if sortedList[ln,2] == 0:
                stackID +=1
                sortedList[ln,2] = stackID
            sortedList[ln+1, 2] = stackID
            ln += 1
    #print(sortedList)

    s = 0
    if sortedList[0, 2] != 0:
        currentStack = sortedList[s, 2]
        s += sum(sortedList[:,2] == currentStack) -1
        #print("line 1 is stacked", numData[int(sortedList[0,1]-1, 0)])
    while s < (lineCount - 1):
        if sortedList[s,2]==0:
            #print("line 1 is not stacked", numData[int(sortedList[s,1]-1),0])
            LX1 = numData[int(sortedList[s,1]-1), headerKeys['x']]
            LY1 = numData[int(sortedList[s,1]-1), headerKeys['y']]
            LA1 = numData[int(sortedList[s,1]-1), headerKeys['angle']]        
            if sortedList[s+1,2] == 0:
                #print("line 2 is not stacked", numData[int(sortedList[s+1,1]-1),0])
                LX2 = numData[int(sortedList[s+1,1]-1), headerKeys['x']]
                LY2 = numData[int(sortedList[s+1,1]-1), headerKeys['y']]
                LA2 = numData[int(sortedList[s+1,1]-1), headerKeys['angle']]
                step = 1
            else:
                currentStack = sortedList[s+1, 2]
                #find the next unstacked line and update step
                step = sum(sortedList[:,2] == currentStack)
                LX2 = numData[int(sortedList[s+step,1]-1), headerKeys['x']]
                LY2 = numData[int(sortedList[s+step,1]-1), headerKeys['y']]
                LA2 = numData[int(sortedList[s+step,1]-1), headerKeys['angle']]
                #print("line 2 is stacked", numData[int(sortedList[s+step,1]-1),0])
        else:
            #use the previously-made composite line
            #print("line 1 is stacked", numData[int(sortedList[s,1]-1),0])
            LX1 = numData[int(sortedList[s,1]-1), headerKeys['x']]
            LY1 = numData[int(sortedList[s,1]-1), headerKeys['y']]
            LA1 = numData[int(sortedList[s,1]-1), headerKeys['angle']]
            #find the next line
            if sortedList[s+1,2] == 0:
                #print("line 2 is not stacked", numData[int(sortedList[s+1,1]-1),0])
                LX2 = numData[int(sortedList[s+1,1]-1), headerKeys['x']]
                LY2 = numData[int(sortedList[s+1,1]-1), headerKeys['y']]
                LA2 = numData[int(sortedList[s+1,1]-1), headerKeys['angle']] 
                step = 1
            else:
                currentStack = sortedList[s+1, 2]
                #make new composite line
                #find the next unstacked line and update step
                step = sum(sortedList[:,2] == currentStack)
                LX2 = numData[int(sortedList[s+step,1]-1), headerKeys['x']]
                LY2 = numData[int(sortedList[s+step,1]-1), headerKeys['y']]
                LA2 = numData[int(sortedList[s+step,1]-1), headerKeys['angle']]
                #print("line 2 is stacked", numData[int(sortedList[s+step,1]-1),0])
        #print(numData[int(sortedList[s,1]-1),0], numData[int(sortedList[s+1,1]-1),0])
        #convert angles to radians, then tan to get slope
        RM1 =  np.deg2rad(180-LA1)
        M1 = 1/np.tan(RM1)
        RM2 = np.deg2rad(180-LA2)
        M2 = 1/np.tan(RM2)
        #print(RM1, M1, RM2, M2)
        #get y intercepts of the line and perpendicular slopes
        B1 = LY1 - (M1*LX1)
        B2 = LY2 - (M2*LX2)
        MP1 = -1/M1
        MP2 = -1/M2
        BP1 = LY2 - (MP1*LX2)
        BP2 = LY1 - (MP2*LX1)
        XP1 = (BP1 - B1) / (M1 - MP1)
        XP2 = (BP2 - B2) / (M2 - MP2)
        YP1 = (M1 * XP1) + B1
        YP2 = (M2 * XP2) + B2
        distance1 = math.sqrt((LX2-XP1)**2 + (LY2-YP1)**2)
        distance2 = math.sqrt((LX1-XP2)**2 + (LY1-YP2)**2)
        space = (distance1+distance2) / 2
        if LX1 == LX2:
            LX1 += 0.001
        MC = (LY2-LY1) / (LX2-LX1)
        MA = 180-np.rad2deg(np.arctan(MC))
        if MA >= 180:
            MA -= 180
        if abs(MA-LA1) > 20:
            #print(s, abs(MA-LA1), space)
            spacing.append(space)
        #print("spacing", space, abs(MA-LA1))
        s += step
    persistenceLength = sum(spacing)
    #print("pLen, mDist", persistenceLength, mDist)
    return spacing, persistenceLength, lengths, mA, mDist

def calcMyofibrils(numData, myofibrils, headerKeys, edgeX, edgeY, xres, imgsize, marker, image=False):
    #set up myofibril data storage list
    myofibrilStats = np.zeros((len(myofibrils),7))
    cellStats = np.zeros((1, 7))
    totalSpacing = np.array([])
    totalLengths = np.array([])
    #for each myofibril
    particles = np.where(numData[:, headerKeys['length']]>=0.2)
    numParticles = (np.shape(particles[0]))
    if len(myofibrils) > 1:
        for m in range(len(myofibrils)):
            myofib = myofibrils[m] #pull out the individual myofibril
            #abbie question: should M-lines and Z-lines be measured differently?
            #are z-lines always on both sides of the Mline??
            #calc spacing and persistence length (separate function)
            spaceM, pLM, lengthM, mA, mDist = calcSpacing(myofib, numData, headerKeys, edgeX, edgeY, xres, imgsize)
            #add number of lines and lengths to the data storage list
            totalSpacing = np.append(totalSpacing, spaceM)
            totalLengths = np.append(totalLengths, lengthM)
            myofibrilStats[m,0] = m+1
            myofibrilStats[m,1] = len(myofib)
            if len(spaceM) > 0:
                myofibrilStats[m,2] = np.nanmean(spaceM)
            else:
                myofibrilStats[m,2] = float("NaN")
            if pLM > 0:
                myofibrilStats[m,3] = pLM
            else:
                myofibrilStats[m,3] = float("NaN")
            myofibrilStats[m,4] = mA
            myofibrilStats[m,5] = np.mean(lengthM)
            if edgeX is not False:
                myofibrilStats[m,6] = mDist
        #calculate whole-cell stats below:
        cellStats[0,0] = len(myofibrils)
        cellStats[0,1] = sum(myofibrilStats[:,1])
        cellStats[0,2] = np.nanmean(myofibrilStats[:,3])
        cellStats[0,3] = np.nanmean(totalLengths)
        cellStats[0,4] = np.nanmean(totalSpacing)
        cellStats[0,5] = sum(numData[(numData[:,headerKeys['length']] >= 0.2), headerKeys['length']])/numParticles[0]
        cellStats[0,6] = numParticles[0]
    else:
        cellStats[0,0] = 0
        cellStats[0,1] = 0
        cellStats[0,2] = float("NaN")
        cellStats[0,3] = float("NaN")
        cellStats[0,4] = float("NaN")
        cellStats[0,5] = sum(numData[(numData[:,headerKeys['length']] >= 0.2), headerKeys['length']])/numParticles[0]
        cellStats[0,6] = numParticles[0]
    #print(myofibrilStats)
    #print(cellStats)
    return myofibrilStats, cellStats

# def main():
#     data_dir = "C:/Users/abbie/Documents/sarcApp/python/toy data/dat1"
#     data_samples = sorted(os.listdir(data_dir))
#     data_path = os.path.join(data_dir, data_samples[0])
#     numData, headerKeys = prepareData(data_path)
#     lines = np.where(numData[:, headerKeys['length']]>=1.4)
#     lines = lines[0]
#     myofibrils = myofibrilSearch(numData, lines, headerKeys, 'actinin')    
#     edgeX, edgeY, edge_shape = edgeDetection(numData, headerKeys)
#     #print(edgeX, edgeY)
#     img_dir = "C:/Users/abbie/Documents/sarcApp/python/toy data/images"
#     img_samples =sorted(os.listdir(img_dir))
#     img_path = os.path.join(img_dir, img_samples[0])
#     img = Image.open(img_path)
#     xres = getMetadata(img)
#     rawSize = img.size
#     calcMyofibrils(numData, myofibrils, headerKeys, edgeX, edgeY, xres, rawSize, 'actinin', image=False)

# if __name__ == '__main__':
#     main()