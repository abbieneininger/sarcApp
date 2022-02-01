import numpy as np
import math
from PIL import Image
from edgeDetection import edgeDetection
import os
from prepareData import prepareData
import PySimpleGUI as sg
from conv2png import conv2png

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

def splitDoublets(doubles, numData, headerKeys):
    pass

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
        if numData[rings[r], headerKeys['AR']]<1.2:
            confirmedRings.append(rings[r])
            ringLengths.append(numData[rings[r], headerKeys['length']])
            ringARs.append(numData[rings[r], headerKeys['AR']])
            distance = distanceFromEdgeR(rings[r], numData, headerKeys, edgeX, edgeY)
            ringDistances.append(distance)
    return(confirmedRings, ringLengths, ringARs, ringDistances)

def doubletSpacing(doublet, numData, headerKeys):
    pass

def titinFixed2D(i, numData, headerKeys, uploadBools, channels = False, display = None, xres = 1):
    edgeX = 0
    edgeY = 0
    lines = np.where((numData[:, headerKeys['length']]>=0.6) & (numData[:,headerKeys['width']]<0.53) &(numData[:,headerKeys['AR']]>2))
    lines = lines[0]
    doubles = np.where((numData[:, headerKeys['length']]>=1) & (numData[:,headerKeys['width']]>0.55) & (numData[:,headerKeys['AR']]<3) & (numData[:,headerKeys['circ']]<0.5))
    doubles = doubles[0]
    doubletIdentities = findDoublets(lines, numData, headerKeys)
    print(doubletIdentities)
    splitDoublets(doubles, numData, headerKeys)
    notRings = np.union1d(lines, doubles) + 1
    notRingsIdx = (np.in1d(numData[:,0], notRings))
    rings = np.where(notRingsIdx==False)
    rings = rings[0]
    confirmedRings, ringLengths, ringARs, ringDistances = titinRings(rings, numData, headerKeys, edgeX, edgeY)

    doubletHeaders = ['doublet', 'length', 'spacing', 'distance from edge']
    ringHeaders = ['ring', 'diameter', 'aspect ratio', 'distance from edge']
    cellHeaders = ['number of doublets', 'avg doublet length', 'avg doublet spacing', 'avg doublet distance from edge', 
                    'number of rings', 'avg ring diameter', 'avg aspect ratio', 'avg ring distance from edge']


    imgsize = display.size
    G_SIZE = (800,800)
    if channels:
        edgeX, edgeY, edge_shape = edgeDetection(numData, headerKeys)  
    if display is not None:
        image = display
        rawSize = image.size
        img_I = image.convert("I")
        img_array = np.array(img_I)
        if uploadBools[0]:
            img_adj = img_array/25
        else:
            img_adj = img_array*255
        img_pil = Image.fromarray(img_adj)
        img_to_display = img_pil.convert("RGB")
        img_to_display.thumbnail(G_SIZE)
        newSize = img_to_display.size
        scale = rawSize[0]/newSize[0]

        layout = [[sg.Graph(canvas_size=G_SIZE, graph_bottom_left=(0, 800), graph_top_right=(800,0), enable_events=True, key='graph')],
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
        for d in range(len(doubletIdentities)):    
            doublet = doubletIdentities[d]
            for j in range(0, len(doubletIdentities[d])):
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
        for r in range(len(confirmedRings)):
            centerX = (numData[rings[r], headerKeys['x']]*xres)/scale
            centerY = (numData[rings[r], headerKeys['y']]*xres)/scale
            diameter = (numData[rings[r], headerKeys['length']]*xres)/scale
            circle = graph.draw_circle((centerX, centerY), radius = diameter/2, line_color = 'red')

        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED:
                break
            elif event == '-SAVE-':
                pass
                #filename = "actininImage{}.jpg".format(i)
                #save_element_as_file(graph, filename)
            elif event == 'Next':
                break
        window.close()

def main():
    i=0
    img_dir = "C:/Users/abbie/Documents/sarcApp/python/toy data/titin_img"
    img_samples =sorted(os.listdir(img_dir))
    img_path = os.path.join(img_dir, img_samples[0])
    img = Image.open(img_path)
    xres = 9.0909
    dat_dir = "C:/Users/abbie/Documents/sarcApp/python/toy data/titin_dat"
    dat_samples = sorted(os.listdir(dat_dir))
    dat_path = os.path.join(dat_dir, dat_samples[0])
    numData, headerKeys = prepareData(dat_path)
    uploadBools = [True, False, True]
    titinFixed2D(i, numData, headerKeys, uploadBools, channels=False, display = img, xres=xres)

if __name__ == '__main__':
    main()