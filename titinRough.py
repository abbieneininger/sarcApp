import numpy as np
import math
from PIL import Image
from edgeDetection import edgeDetection
import os
from prepareData import prepareData
import PySimpleGUI as sg
from conv2png import conv2png
import csv

def findDoublets(lines, numData, headerKeys):
    index = np.linspace(0,len(lines)-1,len(lines))
    index2 = np.zeros(shape=(len(lines),))
    index = np.expand_dims(index,0)
    index2 = np.expand_dims(index2,0)
    index3 = np.concatenate((index, index2), axis = 0)
    #index3 has two columns: line index (NOT ID) and doublet ID
    #the actual identification of the line is in numData column 1
    doubletCount = 0
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
                        mC = (yj-yi) / (xj-xi)
                        mA = 180-np.rad2deg(np.arctan(mC))
                        #if the lines are close enough with the correct angles
                        #they are in the same doublet
                        if ((distance < 1) and (angleDifference < 10) and (abs(ai-mA)>15)):
                            if (index3[1, i] == 0 and index3[1, j] == 0):
                                doubletCount += 1
                                index3[1, i] = doubletCount
                                index3[1, j] = doubletCount
                            elif (index3[1, i] > 0 and index3[1, j] == 0):
                                index3[1, j] = index3[1, i]
                            elif (index3[1, i] == 0 and index3[1, j] > 0):
                                index3[1, i] = index3[1, j]
                            else:
                                doubToDelete = index3[1, j]
                                index3[1, j] = index3[1, i]
                                for s in range(len(lines)):
                                    if index3[1, s] == doubToDelete:
                                        index3[1, s] == index3[1, i]
    doubletIndices = np.unique(index3[1,:])
    doubletCount = 0
    doubletIdentities = []
    index3 = index3.astype(int)
    for k in range(len(doubletIndices)):
        kID = doubletIndices[k]
        if np.sum(index3[1,:]==kID) >= 2:
            doubletCount +=1
            lineIndices = np.where(index3[1,:] == kID)
            lineIndices = lineIndices[0]
            indexLocations = index3[0,lineIndices]
            lineLocations = lines[indexLocations]
            lineIdentities = numData[lineLocations, 0]
            doubletIdentities.append(lineIdentities)
    return(doubletIdentities[1:])

def splitDoubles(doubles, doubletIdentities, numData, headerKeys):
    #when two doublets are attached, split them into two "lines" and
    #pair them as a doublet so they can be drawn and quantified
    doubletIdentities = []
    for d in range(len(doubles)):
        #determine the size of numData
        #as the new line will be added to the end of numData
        shape = np.shape(numData)
        oldID = numData[doubles[d],0]
        newID = shape[0]
        numCols = shape[1]
        newRow = numData[doubles[d],:]
        #gather data about the paired double
        width = numData[doubles[d], headerKeys['width']]
        angle = numData[doubles[d], headerKeys['angle']]
        AR = numData[doubles[d], headerKeys['AR']]
        X = numData[doubles[d], headerKeys['x']]
        Y = numData[doubles[d], headerKeys['y']]
        radangle = np.deg2rad(angle)
        slope1 = np.tan(180-angle)
        if slope1 == 0:
            slope1 += 0.0001
        slope2 = -1/slope1
        #calculate how to separate the two new lines
        l = .25
        x1 = X+(l*math.sqrt(1/(1+slope2**2)))
        y1 = Y-(1*math.sqrt(l/(1+slope2**2)))
        x2 = X-(l*math.sqrt(1/(1+slope2**2)))
        y2 = Y+(1*math.sqrt(l/(1+slope2**2)))
        numData = np.append(numData, [newRow], axis=0)
        numData[newID, 0] = newID + 1
        numData[newID, headerKeys['x']] = x2
        numData[newID, headerKeys['y']] = y2
        numData[newID, headerKeys['AR']] = AR*2
        numData[doubles[d], headerKeys['x']] = x1
        numData[doubles[d], headerKeys['y']] = y1
        numData[doubles[d], headerKeys['AR']] = AR*2
        currentIDs = [oldID, newID+1]
        doubletIdentities.append(currentIDs)
    return(doubletIdentities, numData)

def distanceFromEdgeR(ring, numData, headerKeys, edgeX, edgeY):
    x = numData[ring, headerKeys['x']]
    y = numData[ring, headerKeys['y']]
    return 0

def distanceFromEdgeD(doublet, numData, headerKeys, edgeX, edgeY):
    X1 = numData[doublet[0], headerKeys['x']]
    Y1 = numData[doublet[0], headerKeys['y']]
    X2 = numData[doublet[1], headerKeys['x']]
    Y2 = numData[doublet[1], headerKeys['y']]
    CX = (X1+X2)/2
    CY = (Y1+Y2)/2
    mM = (Y2-Y1)/(X2-X1)
    mCP = -1/(mM)
    bCP = CY - mCP*CX
    mDistIdx = 0
    if edgeX:
        #ABbie check this code, why isn't inty used?
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
    return mDist

def titinRings(rings, numData, headerKeys, edgeX, edgeY):
    confirmedRings = []
    ringLengths = []
    ringARs = []
    ringDistances = []
    i=0
    for r in range(len(rings)):
        if numData[rings[r], headerKeys['AR']]<2:
            confirmedRings.append(rings[r])
            ringLengths.append(numData[rings[r], headerKeys['length']])
            ringARs.append(numData[rings[r], headerKeys['AR']])
            if edgeX is not None:
                distance = distanceFromEdgeR(rings[r], numData, headerKeys, edgeX, edgeY)
                ringDistances.append(distance)
    return(confirmedRings, ringLengths, ringARs, ringDistances)

def doubletSpacing(doublet, numData, headerKeys):
    #abbie: to do, account for 'doublets' with >2 lines
        LX1 = numData[int(doublet[0]-1), headerKeys['x']]
        LY1 = numData[int(doublet[0]-1), headerKeys['y']]
        LA1 = numData[int(doublet[0]-1), headerKeys['angle']]
        LX2 = numData[int(doublet[1]-1), headerKeys['x']]
        LY2 = numData[int(doublet[1]-1), headerKeys['y']]
        LA2 = numData[int(doublet[1]-1), headerKeys['angle']]
        #convert angles to radians, then tan to get slope
        RM1 =  np.deg2rad(180-LA1)
        M1 = 1/np.tan(RM1)
        RM2 = np.deg2rad(180-LA2)
        M2 = 1/np.tan(RM2)
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
        length = (numData[int(doublet[0]-1), headerKeys['length']] + numData[int(doublet[1]-1), headerKeys['length']]) / 2
        return length, space

def sarcAssign():
    pass

def titinFixed2D(i, numData, headerKeys, uploadBools, outputFolder = 0, channels = False, display = None, xres = 1):
    edgeX = None
    edgeY = None
    if channels:
        doubletHeaders = ['Doublet ID', 'Length', 'Spacing', 'Distance from Edge']
        ringHeaders = ['Ring ID', 'Diameter', 'Aspect Ratio', 'Distance from Edge']
        cellHeaders = ['Number of Doublets', 'Mean Doublet Length', 'Mean Doublet Spacing',
                    'Number of Rings', 'Mean Ring Diameter', 'Mean Ring Aspect Ratio',
                    'Mean Doublet Distance from Edge', 'Closest Doublet Distance to Edge',
                    'Mean Ring Distance from Edge']
        cellStats = np.zeros((1, 9))
    else:
        doubletHeaders = ['Doublet ID', 'Length', 'Spacing']
        ringHeaders = ['Ring ID', 'Diameter', 'Aspect Ratio']
        cellHeaders = ['Number of Doublets', 'Mean Doublet Length', 'Mean Doublet Spacing',
                    'Number of Rings', 'Mean Ring Diameter', 'Mean Ring Aspect Ratio']
        cellStats = np.zeros((1, 6))
        #to do: set up edge
    path1 = os.path.join(outputFolder, 'titin_doubletResults{}.csv'.format(i))
    path2 = os.path.join(outputFolder, 'titin_ringResults{}.csv'.format(i))
    path3 = os.path.join(outputFolder, 'titin_cellResults{}.csv'.format(i))
    
    lines = np.where((numData[:, headerKeys['length']]>=0.5) & (numData[:,headerKeys['width']]<0.5) &(numData[:,headerKeys['AR']]>2))
    lines = lines[0]
    doubles = np.where((numData[:, headerKeys['length']]>=1) & (numData[:,headerKeys['width']]>0.6) & (numData[:,headerKeys['circ']]<0.5))
    doubles = doubles[0]
    doubletIdentities = findDoublets(lines, numData, headerKeys)
    #print(doubletIdentities)
    #print(lines)
    #print(doubles)
    
    doubletIdentities, numData = splitDoubles(doubles, doubletIdentities, numData, headerKeys)
    #print(doubletIdentities)
    #to do: combine split doubles with found doublets from above
    #then, presumably, both sets of identities together will undergo spacing calcs as below
    
    if len(doubletIdentities) > 0:
        doubletLengths = []
        doubletSpaces = []
        doubletDistances = []
        if channels:
            doubletStats = np.zeros((len(doubletIdentities), 4))
        else:
            doubletStats = np.zeros((len(doubletIdentities), 3))
        for d in range(len(doubletIdentities)):
            doublet = doubletIdentities[d]
            length, space = doubletSpacing(doublet, numData, headerKeys)
            doubletLengths = np.append(doubletLengths, length)
            doubletSpaces = np.append(doubletSpaces, space)
            doubletStats[d,1], doubletStats[d,2] = length, space
            doubletStats[d,0] = d+1
            if channels:
                distance = distanceFromEdgeD(doublet, numData, headerKeys, edgeX, edgeY)
                doubletDistances = np.append(doubletDistances, distance)
        cellStats[0,0] = len(doubletIdentities)
        cellStats[0,1] = np.nanmean(doubletLengths)
        cellStats[0,2] = np.nanmean(doubletSpaces)
        if channels:
            cellStats[0,6] = np.nanmean(doubletDistances)
            cellStats[0,7] = np.min(doubletDistances)
        

    notRings = np.union1d(lines, doubles) + 1
    notRingsIdx = (np.in1d(numData[:,0], notRings))
    rings = np.where(notRingsIdx==False)
    rings = rings[0]
    if len(rings) > 0:
        confirmedRings, ringLengths, ringARs, ringDistances = titinRings(rings, numData, headerKeys, edgeX, edgeY)
        ringCount = np.linspace(0,len(confirmedRings)-1,len(confirmedRings))
        #print(confirmedRings)
        cellStats[0,3] = len(confirmedRings)
        cellStats[0,4] = np.nanmean(ringLengths)
        cellStats[0,5] = np.nanmean(ringARs)
        if channels:
            ringStats = np.transpose(np.stack((ringCount, ringLengths, ringARs, ringDistances)))
            cellStats[0,12] = np.nanmean(ringDistances)
            #cellStats[0,13] = 
        else:
            ringStats = np.transpose(np.stack((ringCount, ringLengths, ringARs)))
    else:
        cellStats[0,3] = 0
        cellStats[0,4] = float("NaN")
        cellStats[0,5] = float("NaN")
        if channels:
            cellStats[0,8] = float("NaN")


    
    if len(doubletIdentities) > 1:
        with open(path1,'w', newline='') as f:
            write = csv.writer(f)
            write.writerow(doubletHeaders)
            write.writerows(doubletStats)
    if len(confirmedRings) > 1:
        with open(path2, 'w', newline='') as f:
            write = csv.writer(f)
            write.writerow(ringHeaders)
            write.writerows(ringStats)
    with open(path3, 'w', newline='') as f:
        write = csv.writer(f)
        write.writerow(cellHeaders)
        write.writerows(cellStats)

    imgsize = display.size
    G_SIZE = (600,600)
    if channels:
        edgeX, edgeY, edge_shape = edgeDetection(numData, headerKeys)  
    if display is not None:
        image = display
        rawSize = image.size
        img_I = image.convert("I")
        img_array = np.array(img_I)
        if uploadBools[0]:
            img_adj = img_array
        else:
            img_adj = img_array*255
            #abbie note: check above line, does it need *255
        img_pil = Image.fromarray(img_adj)
        img_to_display = img_pil.convert("RGB")
        img_to_display.thumbnail(G_SIZE)
        newSize = img_to_display.size
        scale = rawSize[0]/newSize[0]

        layout = [[sg.Graph(canvas_size=G_SIZE, graph_bottom_left=(0, G_SIZE[1]), graph_top_right=(G_SIZE[0],0), enable_events=True, key='graph')],
                [sg.Button('Next'), sg.Button('Save', key='-SAVE-')]]

        window = sg.Window('titin', layout, finalize=True)
        graph = window['graph']
        image = graph.draw_image(data=conv2png(img_to_display), location = (0,0))
        if channels:
            edgeX = edgeX*xres/scale
            edgeY = edgeY*xres/scale
            points = np.stack((edgeX, edgeY), axis=1)
            x, y = points[0]
            for x1,y1 in points:
                graph.draw_line((x,y), (x1,y1), color = 'grey', width = 1)
                x, y = x1, y1
        palette = ['#b81dda', '#2ed2d9', '#29c08c', '#f4f933', '#e08f1a']
        p=0
        # for j in range(len(doubles)):
        #     centerX = (numData[int(doubles[j]), headerKeys['x']]*xres)/scale
        #     centerY = (numData[int(doubles[j]), headerKeys['y']]*xres)/scale
        #     length = (numData[int(doubles[j]), headerKeys['length']]*xres)/scale
        #     angle = numData[int(doubles[j]), headerKeys['angle']]
        #     radAngle = np.deg2rad(180-angle)
        #     slope = 1/np.tan(radAngle)
        #     height = (length/2)*np.sin(np.arctan(slope))
        #     width = (length/2)*np.cos(np.arctan(slope))
        #     X1 = centerX - height
        #     Y1 = centerY - width
        #     X2 = centerX + height
        #     Y2 = centerY + width
        #     line = graph.draw_line((X1,Y1),(X2,Y2), color = palette[p], width = 1)
        #     p = (p+1) % 5
        for d in range(len(doubletIdentities)):    
            doublet = doubletIdentities[d]
            print(doublet)
            for j in range(0, len(doubletIdentities[d])):
                #print(numData[int(doublet[j]-1),:])
                centerX = (numData[int(doublet[j]-1), headerKeys['x']]*xres)/scale
                centerY = (numData[int(doublet[j]-1), headerKeys['y']]*xres)/scale
                length = (numData[int(doublet[j]-1), headerKeys['length']]*xres)/scale
                angle = numData[int(doublet[j]-1), headerKeys['angle']]
                radAngle = np.deg2rad(180-angle)
                slope = 1/np.tan(radAngle)
                height = (length/2)*np.sin(np.arctan(slope))
                width = (length/2)*np.cos(np.arctan(slope))
                X1 = centerX - height
                Y1 = centerY - width
                X2 = centerX + height
                Y2 = centerY + width
                line = graph.draw_line((X1,Y1),(X2,Y2), color = palette[p], width = 1)
            p = (p+1) % 5
        # for r in range(len(confirmedRings)):
        #     if numData[int(confirmedRings[r]), headerKeys['area']] > 0.2:
        #         centerX = (numData[int(confirmedRings[r]), headerKeys['x']]*xres)/scale
        #         centerY = (numData[int(confirmedRings[r]), headerKeys['y']]*xres)/scale
        #         diameter = (numData[int(confirmedRings[r]), headerKeys['length']]*xres)/scale
        #         circle = graph.draw_circle((centerX, centerY), radius = diameter/2, line_color = 'red')

        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED:
                break
            elif event == '-SAVE-':
                pass
                #filename = "titinImage{}.jpg".format(i)
                #save_element_as_file(graph, filename)
            elif event == 'Next':
                break
        window.close()

def main():
    i=0
    img_dir = "C:/Users/abbie/Documents/sarcApp/python/toy data/titin_bin"
    img_samples =sorted(os.listdir(img_dir))
    img_path = os.path.join(img_dir, img_samples[3])
    img = Image.open(img_path)
    xres = 9.0909
    dat_dir = "C:/Users/abbie/Documents/sarcApp/python/toy data/titin_dat"
    dat_samples = sorted(os.listdir(dat_dir))
    dat_path = os.path.join(dat_dir, dat_samples[3])
    numData, headerKeys = prepareData(dat_path)
    uploadBools = [True, False, True]
    titinFixed2D(i, numData, headerKeys, uploadBools, outputFolder = "C:/Users/abbie/Documents/sarcApp/python/toy data/titin_out", channels=False, display = img, xres=xres)

if __name__ == '__main__':
    main()