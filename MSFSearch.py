import numpy as np
import math

def MSFSearch(numData, Zbodies, headerKeys, edgeX, edgeY, actin=False):
    maxDistance = 3
    maxAngleDifference = 15
    index = np.linspace(0,len(Zbodies)-1,len(Zbodies))
    index2 = np.zeros(shape=(len(Zbodies),))
    index = np.expand_dims(index,0)
    index2 = np.expand_dims(index2,0)
    index3 = np.concatenate((index, index2), axis = 0)
    MSFCount = 0
    for i in range(len(Zbodies)):
        
        #if there are more than 0 candidate Zbodies in the cell
        if (numData[Zbodies[i], headerKeys['x']] > 0):
            #find their X and Y coordinates
            X = numData[Zbodies[i], headerKeys['x']]
            Y = numData[Zbodies[i], headerKeys['y']]
            distToEdge = []

            #for each point in the edge, find X and Y coordinates and
            #calculate distance from the candidate Z body
            for p in range(len(edgeX)):
                tmpX = edgeX[p]
                tmpY = edgeY[p]
                distToEdge.append(math.sqrt((tmpX-X)**2+(tmpY-Y)**2))
            #find closest edge point to the candidate Z body
            edgeIdx = np.argmin(distToEdge)

            #for the remaining Z bodies in the list
            for j in range(i+1,len(Zbodies)):
                #find the X and Y coordinates (J)
                XJ = numData[Zbodies[j], headerKeys['x']]

                if XJ == X:
                    XJ += 0.001
                YJ = numData[Zbodies[j], headerKeys['y']]
                #calculate the distance between the prev Z body and this one
                distance = math.sqrt((Y-YJ)**2+(X-XJ)**2)

                #if these Z-bodies are sufficiently close
                if distance < maxDistance:
                    distToEdge2 = []

                    #calculate the closest edge segment to Z body 2
                    for p in range(len(edgeX)):
                        tmpX = edgeX[p]
                        tmpY = edgeY[p]
                        #AC: check equation
                        distToEdge2.append(math.sqrt((tmpX-XJ)**2+(tmpY-YJ)**2))
                    edgeIdx2 = np.argmin(distToEdge2)
                    
                    #if both Z bodies are next to the same edge segment, use the
                    #next one to calculate the relative slope of the edge
                    if ((edgeIdx == edgeIdx2) and (edgeIdx < len(edgeX))):
                        edgeIdx2 += 1
                    elif edgeIdx == len(edgeX):
                        edgeIdx2 = edgeIdx - 1
                    e1X = edgeX[int(edgeIdx)]
                    e1Y = edgeY[int(edgeIdx)]
                    e2X = edgeX[int(edgeIdx2)]
                    e2Y = edgeY[int(edgeIdx2)] 
                    
                    if e1X == e2X:
                        e2X += 0.001
                    #calculate the slope of the nearby edge segment
                    edgeSlope = 180-np.rad2deg(np.arctan(e2Y-e1Y)/(e2X-e1X))   
                    #calculate the slope of the line between the two Z-bodies           
                    mC = (Y-YJ)/(X-XJ)
                    mA = 180-np.rad2deg(np.arctan(mC))
                    angleDifference = abs(mA-edgeSlope)
                    
                    #if Z-bodies align with the edge (basically)
                    if angleDifference < maxAngleDifference:
                        if (index3[1, i] == 0 and index3[1, j] == 0):
                            MSFCount += 1
                            index3[1, i] = MSFCount
                            index3[1, j] = MSFCount
                        elif (index3[1, i] > 0 and index3[1, j] == 0):
                            index3[1, j] = index3[1, i]
                        elif (index3[1, i] == 0 and index3[1, j] > 0):
                            index3[1, i] = index3[1, j]
                        else:
                            MSFToDelete = index3[1, j]
                            index3[1, j] = index3[1, i]
                            for s in range(len(Zbodies)):
                                if index3[1, s] == MSFToDelete:
                                    index3[1, s] == index3[1, i]
    
    MSFIndices = np.unique(index3[1,:])-1
    minBodies = 4
    MSFCount = 0
    ZBodyCount = 0
    MSFIdentities = []
    
    for k in range(len(MSFIndices+1)):
        if np.sum(index3[1,:] == k+1) > minBodies:
            MSFCount += 1
            bodyIndices = np.where(index3[1, :] == k+1)
            bodyIndices = bodyIndices[0]
            ZBodyCount += len(bodyIndices)
            ZBodyIdentities = numData[Zbodies[bodyIndices],0]
            MSFIdentities.append(ZBodyIdentities)
    
    return(MSFIdentities)