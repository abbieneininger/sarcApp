import numpy as np
import math

def myofibrilSearch(numData, lines, headerKeys, marker):
    if marker == 'actinin':
        minLines = 4
    elif marker == 'myomesin':
        minLines = 3
    index = np.linspace(0,len(lines)-1,len(lines))
    index2 = np.zeros(shape=(len(lines),))
    index = np.expand_dims(index,0)
    index2 = np.expand_dims(index2,0)
    index3 = np.concatenate((index, index2), axis = 0)
    #for each potential line
    myofibCount = 0
    for i in range(len(lines)):
        if (numData[lines[i], headerKeys['x']] > 0):
            for j in range(i+1,len(lines)):
                if (index3[1, i] + index3[1, j] == 0 or index3[1, i] != index3[1, j]):
                    if (numData[lines[j], headerKeys['x']] > 0):
                        xi = numData[lines[i], headerKeys['x']]
                        xj = numData[lines[j], headerKeys['x']]
                        yi = numData[lines[i], headerKeys['y']]
                        yj = numData[lines[j], headerKeys['y']]
                        #calculate the distance between the two lines
                        distance = math.sqrt(((xi-xj)**2)+((yi-yj)**2))
                        ai = numData[lines[i], headerKeys['angle']]        
                        aj = numData[lines[j], headerKeys['angle']]    
                        angleDifference = abs(ai-aj)
                        #calculate the angle of the line between the two centers
                        if xj == xi:
                            xj += 0.001
                        mC = (yj-yi) / (xj-xi)
                        mA = 180-np.rad2deg(np.arctan(mC))
                        #if the lines are close enough with the correct angles
                        #they are in the same myofibril
                        if ((distance < 3) and (angleDifference < 30) and (abs(ai-mA)>15)):
                            if (index3[1, i] == 0 and index3[1, j] == 0):
                                myofibCount += 1
                                index3[1, i] = myofibCount
                                index3[1, j] = myofibCount
                            elif (index3[1, i] > 0 and index3[1, j] == 0):
                                index3[1, j] = index3[1, i]
                            elif (index3[1, i] == 0 and index3[1, j] > 0):
                                index3[1, i] = index3[1, j]
                            else:
                                myoToDelete = index3[1, j]
                                index3[1, j] = index3[1, i]
                                for s in range(len(lines)):
                                    if index3[1, s] == myoToDelete:
                                        index3[1, s] == index3[1, i]
    #figure out unique myofibrils
    myofibrilIndices = np.unique(index3[1,:])-1
    myofibCount = 0
    lineCount = 0
    myofibrilIdentities = []
    #remove myofibrils with fewer than 3 m lines or 4 z lines
    for k in range(len(myofibrilIndices+1)):
        if np.sum(index3[1,:]==k+1) >= minLines:
            myofibCount +=1
            lineIndices = np.where(index3[1, :]==k+1)
            lineIndices = lineIndices[0]
            lineCount += len(lineIndices)
            lineIdentities = numData[lines[lineIndices],0]
            myofibrilIdentities.append(lineIdentities)
    #print(myofibrilIdentities)
    return myofibrilIdentities
