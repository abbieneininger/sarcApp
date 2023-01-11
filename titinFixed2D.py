import numpy as np
import math
from PIL import Image
import os
import PySimpleGUI as sg
from conv2png import conv2png
import csv
from myofibrilSearch import myofibrilSearch
from calcMyofibrils import calcMyofibrils
import matplotlib.pyplot as plt

def pairSingles(singles, numData, headerKeys):
    index = np.linspace(0,len(singles)-1,len(singles))
    index2 = np.zeros(shape=(len(singles),))
    index = np.expand_dims(index,0)
    index2 = np.expand_dims(index2,0)
    index3 = np.concatenate((index, index2), axis = 0)
    #index3 has two columns: line index (NOT ID) and doublet ID
    #the actual identification of the line is in numData column 1
    doubletCount = 0
    for i in range(len(singles)):
        if (numData[singles[i], headerKeys['x']] > 0):
            for j in range(i+1,len(singles)):
                if (index3[1, i] + index3[1, j] == 0 or index3[1, i] != index3[1, j]):
                    if (numData[singles[j], headerKeys['x']] > 0):
                        xi = numData[singles[i], headerKeys['x']]
                        xj = numData[singles[j], headerKeys['x']]
                        yi = numData[singles[i], headerKeys['y']]
                        yj = numData[singles[j], headerKeys['y']]
                        #calculate the distance between the two singles
                        distance = math.sqrt(((xi-xj)**2)+((yi-yj)**2))
                        ai = numData[singles[i], headerKeys['angle']]        
                        aj = numData[singles[j], headerKeys['angle']]    
                        angleDifference = abs(ai-aj)
                        #calculate the angle of the line between the two centers
                        if xj == xi:
                            xj += 0.001
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
                                for s in range(len(singles)):
                                    if index3[1, s] == doubToDelete:
                                        index3[1, s] == index3[1, i]
    doubletCandidates = np.unique(index3[1,:])
    pairedIndices = []
    index3 = index3.astype(int)
    for k in doubletCandidates[1:]:
        if np.sum(index3[1,:]==k) >= 2:
            currentPairIndices = np.where(index3[1,:] == k)
            pairTuple = currentPairIndices[0]
            idx1, idx2, *rest = pairTuple
            pairedIndices.append([idx1,idx2])
    pairedSingles = []
    for p in pairedIndices:
        shape = np.shape(numData)
        newLocation = shape[0]
        numCols = shape[1]
        idx = p[0]
        newRow = numData[idx,:]
        X1 = numData[p[0], headerKeys['x']]
        Y1 = numData[p[0], headerKeys['y']]
        X2 = numData[p[1], headerKeys['x']]
        Y2 = numData[p[1], headerKeys['y']]
        newX = (X2+X1)/2
        newY = (Y2+Y1)/2
        newRow[headerKeys['x']] = newX
        newRow[headerKeys['y']] = newY
        length1 = numData[p[0], headerKeys['length']]
        length2 = numData[p[1], headerKeys['length']]
        newLength = (length2+length1)/2
        newRow[headerKeys['length']] = newLength
        numData = np.append(numData, [newRow], axis=0)
        pairedSingles.append(newLocation)
    
    return(pairedIndices, pairedSingles, numData)

def separateDoubles(doubles, numData, headerKeys):
    separatedDoubles = []
    for d in range(len(doubles)):
        shape = np.shape(numData)
        newLocation = shape[0]
        numCols = shape[1]
        newRow = numData[doubles[d],:]
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
        l = .25
        x1 = X+(l*math.sqrt(1/(l+slope2**2)))
        y1 = Y-(1*math.sqrt(l/(1+slope2**2)))
        x2 = X-(l*math.sqrt(1/(l+slope2**2)))
        y2 = Y+(1*math.sqrt(l/(1+slope2**2)))
        numData = np.append(numData, [newRow], axis=0)
        numData = np.append(numData, [newRow], axis=0)
        numData[newLocation, 0] = newLocation + 1 
        numData[newLocation, headerKeys['x']] = x2
        numData[newLocation, headerKeys['y']] = y2
        numData[newLocation, headerKeys['AR']] = AR*2
        numData[newLocation+1, headerKeys['x']] = x1
        numData[newLocation+1, headerKeys['y']] = y1
        numData[newLocation+1, headerKeys['AR']] = AR*2   
        singleLocations = [newLocation,newLocation+1]
        separatedDoubles.append(singleLocations)

    return(separatedDoubles, numData)

def calculateRings(rings, numData, headerKeys, edgeX=0, edgeY=0):
    ringLengths = []
    ringARs = []
    ringDistances = []
    for r in range(len(rings)):
        ringLengths.append(numData[rings[r], headerKeys['length']])
        ringARs.append(numData[rings[r], headerKeys['AR']])
        if edgeX is not None:
            distance = distanceFromEdge(rings[r], numData, headerKeys, edgeX, edgeY)
            ringDistances.append(distance)
    
    return(ringLengths, ringARs, ringDistances)

def distanceFromEdge(obj, numData, headerKeys, edgeX, edgeY):
    objX = numData[obj, headerKeys['x']]
    objY = numData[obj, headerKeys['y']]
    distToEdgeAll = []
    for p in range(len(edgeX)-1):
        edge1X = edgeX[p]
        edge1Y = edgeY[p]
        distToEdgeAll.append(math.sqrt((edge1X-objX)**2+(edge1Y-objY)**2))
    
    return(np.min(distToEdgeAll))

def titinFixed2D(i, numData, headerKeys, uploadBools, outputFolder, edgeX = None, edgeY = None, display = None, xres=1):
    
    if display is not None:
        imgsize = display.size
    else:
        imgsize = None

    if edgeX is not None:
        myofibrilHeaders = ['Myofibril','Number of Doublets', 'Average Spacing b/w Doublets', 
            'Persistence Length', 'Angle of Myofibril Long Axis',
            'Average Doublet Length', 'Distance from the Edge', 'Normalized Angle', 'Edge Angle']
        ringHeaders = ['Ring ID', 'Diameter', 'Aspect Ratio', 'Distance from the Edge']
        cellHeaders = ['Total Number of Myofibrils','Total Number of Doublets',
            'Average Myofibril Persistence Length','Average Doublet Length',
            'Average Doublet Spacing', 'Average Size of All Puncta', 'Total Number of Puncta',
            'Number of Rings', 'Average Ring Diameter', 'Average Ring Aspect Ratio', 'Average Doublet Distance from Edge', 
            'Closest Doublet Distance to Edge', 'Average Ring Distance from Edge', 'Closest Ring Distance to Edge']
        cellStats = np.zeros((1,14))
    else:
        myofibrilHeaders = ['Myofibril', 'Number of Doublets', 'Average Spacing b/w Doublets',
            'Persistence Length', 'Angle of Myofibril Long Axis', 'Average Doublet Length']
        ringHeaders = ['Ring ID', 'Diameter', 'Aspect Ratio']
        cellHeaders = ['Total Number of Myofibrils', 'Total Number of Doublets',
            'Average Myofibril Persistence Length', 'Average Doublet Length', 'Average Doublet Spacing', 'Average Size of All Puncta', 
            'Total Number of Puncta', 'Number of Rings', 'Average Ring Diameter', 'Average Ring Aspect Ratio']
        cellStats = np.zeros((1,10))

    path1 = os.path.join(outputFolder, 'titin_myofibrilResults{}.csv'.format(i))
    path2 = os.path.join(outputFolder, 'titin_ringResults{}.csv'.format(i))
    path3 = os.path.join(outputFolder, 'titin_cellResults{}.csv'.format(i))

    #partition singles and doubles from the dataset
    singles = np.where((numData[:, headerKeys['length']]>=0.5) & (numData[:,headerKeys['width']]<0.5) & (numData[:,headerKeys['AR']]>2) & (numData[:,headerKeys['area']]>0.2))
    singles = singles[0]
    doubles = np.where((numData[:, headerKeys['length']]>=1.7) & (numData[:,headerKeys['width']]>0.6) & (numData[:,headerKeys['circ']]<0.5) & (numData[:,headerKeys['area']]>0.2))
    doubles = doubles[0]
    pairedIndices, pairedSingles, numData = pairSingles(singles, numData, headerKeys)
   
    if (len(pairedSingles) > 0): 
        doubletIndices = np.concatenate((pairedSingles, doubles))
    else:
        doubletIndices = doubles
    
    #identify myofibrils and calculate stats
    if len(doubles) > 0:
        myofibrils = myofibrilSearch(numData, doubletIndices, headerKeys, 'titin')
        myofibrilStats, cellStats = calcMyofibrils(numData, myofibrils, headerKeys, edgeX, edgeY, xres, 'titin', display)
    else:
        myofibrils = []
        if (edgeX is not None):
            cellStats = np.zeros((1, 14))
        else:
            cellStats = np.zeros((1, 10))
        particles = np.where(numData[:, headerKeys['area']]>=0.2)
        numParticles = (np.shape(particles[0]))
        cellStats[0,0] = 0
        cellStats[0,1] = 0
        cellStats[0,2] = float("NaN")
        cellStats[0,3] = float("NaN")
        cellStats[0,4] = float("NaN")
        cellStats[0,5] = sum(numData[(numData[:,headerKeys['area']] >= 0.2), headerKeys['area']])/numParticles[0]
        cellStats[0,6] = numParticles[0]

    #calculate distance from edge for doublets
    if (len(doubletIndices) > 0) and (edgeX is not None):
        doubletDistances = []
        for d in doubletIndices:
            distance = distanceFromEdge(d, numData, headerKeys, edgeX, edgeY)
            doubletDistances.append(distance)
        cellStats[0,10] = np.nanmean(doubletDistances)
        try:
            min5idx = np.argpartition(doubletDistances, 5)
            doubletDistances = np.asarray(doubletDistances)
            cellStats[0,11] = np.mean(doubletDistances[min5idx[:5]])
        except ValueError:
            cellStats[0,11] = np.mean(doubletDistances)
            
    #identify rings and calculate stats
    notRings = np.union1d(singles, doubles) + 1
    notRingsIdx = (np.in1d(numData[:,0], notRings))
    rings = np.where((notRingsIdx==False) & (numData[:,headerKeys['AR']]<2) & (numData[:,headerKeys['area']]>0.2))
    rings = rings[0]
    if len(rings)>0:
        ringLengths, ringARs, ringDistances = calculateRings(rings, numData, headerKeys, edgeX, edgeY)
        ringCount = np.linspace(0,len(rings)-1,len(rings))
        cellStats[0,7] = len(rings)
        cellStats[0,8] = np.nanmean(ringLengths)
        cellStats[0,9] = np.nanmean(ringARs)
        if edgeX is not None:
            ringStats = np.transpose(np.stack((ringCount, ringLengths, ringARs, ringDistances)))
            cellStats[0,12] = np.nanmean(ringDistances)
            try:
                min5idx = np.argpartition(ringDistances, 5)
                ringDistances = np.asarray(ringDistances)
                cellStats[0,13] = np.mean(ringDistances[min5idx[:5]])
            except ValueError:
                cellStats[0,13] = np.mean(ringDistances)
        else:
            ringStats = np.transpose(np.stack((ringCount, ringLengths, ringARs)))
    else:
        cellStats[0,7] = 0
        cellStats[0,8] = float("NaN")
        cellStats[0,9] = float("NaN")
        if edgeX is not None:
            cellStats[0,12], cellStats[0,13] = float("NaN")

    if len(myofibrils) > 1:
        with open(path1,'w', newline='') as f:
            write = csv.writer(f)
            write.writerow(myofibrilHeaders)
            write.writerows(myofibrilStats)
    if len(rings) > 1:
        with open(path2, 'w', newline='') as f:
            write = csv.writer(f)
            write.writerow(ringHeaders)
            write.writerows(ringStats)
    with open(path3, 'w', newline='') as f:
        write = csv.writer(f)
        write.writerow(cellHeaders)
        write.writerows(cellStats)

    #AC: change G_SIZE based on screen resolution?
    G_SIZE = (600,600)
    (GX, GY) = G_SIZE

    if display is not None:
        image = display
        rawSize = image.size
        img_I = image.convert("I")
        img_array = np.array(img_I)
        
        if uploadBools[0]:
            img_adj = img_array
        else:
            img_adj = img_array*255
        
        img_pil = Image.fromarray(img_adj)
        img_to_display = img_pil.convert("RGB")
        img_to_display.thumbnail(G_SIZE)
        newSize = img_to_display.size
        scale = rawSize[0]/newSize[0]
        layout = [[sg.Graph(canvas_size=G_SIZE, graph_bottom_left=(0, GY), graph_top_right=(GX,0), enable_events=True, key='graph')],
                [sg.Button('Next')]]
        window = sg.Window('Titin', layout, finalize=True)
        graph = window['graph']
        image = graph.draw_image(data=conv2png(img_to_display), location = (0,0))
        
        #graph edge
        if edgeX is not None:
            edgeX2 = edgeX*xres/scale
            edgeY2 = edgeY*xres/scale
            points = np.stack((edgeX2, edgeY2), axis=1)
            x, y = points[0]

            for x1,y1 in points:
                graph.draw_line((x,y), (x1,y1), color = 'grey', width = 1)                
                x, y = x1, y1
        
        palette = ['#b81dda', '#2ed2d9', '#29c08c', '#f4f933', '#e08f1a']
        p = 0

        #This graphs doublets that are not part of a myofibril in pink
        #AC: do regular users need this?
        if len(doubles) > 1:
            for d in doubles:
                idx1 = d
                centerX1 = (numData[int(idx1), headerKeys['x']]*xres)/scale
                centerY1 = (numData[int(idx1), headerKeys['y']]*xres)/scale
                length1 = (numData[int(idx1), headerKeys['length']]*xres)/scale
                angle1 = numData[int(idx1), headerKeys['angle']]
                radAngle1 = np.deg2rad(180-angle1)
                slope1 = 1/np.tan(radAngle1)
                height1 = (length1/2)*np.sin(np.arctan(slope1))
                width1= (length1/2)*np.cos(np.arctan(slope1))
                X1_1 = centerX1 - height1
                Y1_1 = centerY1 - width1
                X2_1 = centerX1 + height1
                Y2_1 = centerY1 + width1
                line1 = graph.draw_line((X1_1,Y1_1),(X2_1,Y2_1), color = 'pink', width = 3)
 
        for m in range(len(myofibrils)):    
            myofib = myofibrils[m]
            for j in range(0, len(myofibrils[m])):
                centerX = (numData[int(myofib[j]-1), headerKeys['x']]*xres)/scale
                centerY = (numData[int(myofib[j]-1), headerKeys['y']]*xres)/scale
                length = (numData[int(myofib[j]-1), headerKeys['length']]*xres)/scale
                angle = numData[int(myofib[j]-1), headerKeys['angle']]
                radAngle = np.deg2rad(180-angle)
                slope = 1/np.tan(radAngle)
                height = (length/2)*np.sin(np.arctan(slope))
                width = (length/2)*np.cos(np.arctan(slope))
                X1 = centerX - height
                Y1 = centerY - width
                X2 = centerX + height
                Y2 = centerY + width
                line = graph.draw_line((X1,Y1),(X2,Y2), color = palette[p], width = 3)
            p = (p+1) % 5
        
        #graph rings
        if len(rings) > 1:
            for r in rings:
                centerX = (numData[int(r), headerKeys['x']]*xres)/scale
                centerY = (numData[int(r), headerKeys['y']]*xres)/scale
                diameter = (numData[int(r), headerKeys['length']]*xres)/scale
                circle = graph.draw_circle((centerX, centerY), radius = diameter/2, line_color = 'red')
        
        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED:
                break
            elif event == 'Next':
                break
        window.close()
    

    filename = "/titinImage{}.jpg".format(i)
    fig, ax = plt.subplots(dpi = 400)    
    
    if edgeX is not None:
        points = np.stack((edgeX*xres, edgeY*xres), axis=1)
        x, y = points[0]
        for x1,y1 in points:
            plt.plot([x,x1],[-y,-y1], color = 'grey', linewidth = 1)
            x, y = x1, y1
    palette = ['#b81dda', '#2ed2d9', '#29c08c', '#f4f933', '#e08f1a']
    p=0    
    
    for m in range(len(myofibrils)):    
        myofib = myofibrils[m]
        for j in range(0, len(myofibrils[m])):
            centerX = (numData[int(myofib[j]-1), headerKeys['x']]*xres)
            centerY = (numData[int(myofib[j]-1), headerKeys['y']]*xres)
            length = (numData[int(myofib[j]-1), headerKeys['length']]*xres)
            angle = numData[int(myofib[j]-1), headerKeys['angle']]
            radAngle = np.deg2rad(180-angle)
            slope = 1/np.tan(radAngle)
            height = (length/2)*np.sin(np.arctan(slope))
            width = (length/2)*np.cos(np.arctan(slope))
            X1 = centerX - height
            Y1 = centerY - width
            X2 = centerX + height
            Y2 = centerY + width
            plt.plot([X1,X2],[-Y1,-Y2], color = palette[p], linewidth = 2)
        p = (p+1) % 5
        
    if len(rings) > 1:
        for r in rings:
            centerX = (numData[int(r), headerKeys['x']]*xres)
            centerY = (numData[int(r), headerKeys['y']]*xres)
            diameter = (numData[int(r), headerKeys['length']]*xres)
            plt.plot(centerX, -centerY, 'o', markersize = diameter, mec = 'r', mfc = 'w')
        
    plt.axis('equal')
    plt.axis('off')
    plt.subplots_adjust(wspace=None, hspace=None)
    plt.tight_layout()        
    plt.savefig(os.path.join(outputFolder+filename),bbox_inches = 'tight', pad_inches = 0.0) 
    plt.close(fig)  
    

    return np.insert(cellStats,0,i)