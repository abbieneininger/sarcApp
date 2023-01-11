import numpy as np
import PySimpleGUI as sg
from PIL import Image
from myofibrilSearch import myofibrilSearch
from calcMyofibrils import calcMyofibrils
import csv
from edgeDetection import edgeDetection
import math
from MSFSearch import MSFSearch
from calcMSFs import calcMSFs
from conv2png import conv2png
import os
import matplotlib.pyplot as plt
import pickle

def separateObjects(data, lengthColumn):
    Zlines = np.where(data[:, lengthColumn]>=1.4)
    Zbodies = np.where((data[:, lengthColumn]<1.4) & (data[:, lengthColumn]>0.2))
    return Zlines[0], Zbodies[0]

def solveH(numData, Zlines, headerKeys, hIdx):
    for h in range(len(hIdx)):
        shape = np.shape(numData)
        newID = shape[0]
        numCols = shape[1]
        loc = Zlines[hIdx[h]]
        newRow = numData[loc,:]
        width = numData[loc, headerKeys['width']]
        angle = numData[loc, headerKeys['angle']]
        AR = numData[loc, headerKeys['AR']]
        X = numData[loc, headerKeys['x']]
        Y = numData[loc, headerKeys['y']]
        radangle = np.deg2rad(angle)
        slope1 = np.tan(180-angle)
        if slope1 == 0:
            slope1 += 0.0001
        slope2 = -1/slope1
        l = (width-1)+0.25
        x1 = X+(1*math.sqrt(1/(l+slope2**2)))
        y1 = Y-(1*math.sqrt(l/(1+slope2**2)))
        x2 = X-(1*math.sqrt(1/(l+slope2**2)))
        y2 = Y+(1*math.sqrt(l/(1+slope2**2)))
        numData = np.append(numData, [newRow], axis=0)
        Zlines = np.append(Zlines, newID)
        numData[newID, 0] = newID + 1
        numData[newID, headerKeys['x']] = x2
        numData[newID, headerKeys['y']] = y2
        numData[newID, headerKeys['AR']] = AR*2
        numData[loc, headerKeys['x']] = x1
        numData[loc, headerKeys['y']] = y1
        numData[loc, headerKeys['AR']] = AR*2
    return Zlines, numData

def actininFixed2D(i, numData, headerKeys, uploadBools, outputFolder, display = None, xres=1):
    #separate Z lines and Z bodies based on length, at first
    Zlines, Zbodies = separateObjects(numData, headerKeys['length'])
    edgeX, edgeY, edge_shape = edgeDetection(numData, headerKeys)
    f = open(os.path.join(outputFolder + "/edgeShape_{}".format(i)), "wb")
    pickle.dump(edge_shape, f)
    f.close()
    
    #solve any H-shaped structures in the Z lines
    hbool = np.logical_and(numData[Zlines,headerKeys['AR']]<2,numData[Zlines,headerKeys['width']]>1.5)
    hIdx = np.where(hbool)
    Zlines,numData = solveH(numData, Zlines, headerKeys, hIdx[0])
    
    #assign z-lines to myofibrils and z-bodies to msfs
    myofibrils = myofibrilSearch(numData, Zlines, headerKeys, 'actinin') 
    MSFs = MSFSearch(numData, Zbodies, headerKeys, edgeX, edgeY, actin=False)

    #setup headers
    prefix = 'Z-'
    if display is not None:
        imgsize = display.size
    else:
        imgsize = None
    myofibrilHeaders = ['Myofibril','Number of {}Lines'.format(prefix),'Average Spacing',
            'Persistence Length','Angle of Myofibril Long Axis',
            'Average {}Line Length'.format(prefix), 'Distance from the Edge', 'Normalized Angle', 'Edge Angle']
    cellHeaders = ['Total Number of Myofibrils','Total Number of {}Lines'.format(prefix),
            'Average Myofibril Persistence Length','Average {}Line Length'.format(prefix), 
            'Average {}Line Spacing'.format(prefix),'Average Size of All Puncta', 'Total Number of Puncta',
            'Total Number of MSFs', 'Total Number of Z-Bodies', 'Average MSF Persistence Length', 
            'Average Z-Body Length', 'Average Z-Body Spacing']
    MSFHeaders = ['MSF', 'Number of Z-Bodies', 'Average Spacing', 'Persistence Length', 
                'Average Z-Body Length', 'Distance From the Edge']
    
    #calculate stats for myofibrils and MSFs
    myofibrilStats, cellStats1 = calcMyofibrils(numData, myofibrils, headerKeys, edgeX, edgeY, xres, 'actinin', display)
    MSFStats, cellStats2 = calcMSFs(numData, MSFs, headerKeys, edgeX, edgeY)
    
    cellStats = np.concatenate((cellStats1[0], cellStats2[0]))
    
    path1 = os.path.join(outputFolder, 'actinin_mfResults{}.csv'.format(i))
    path2 = os.path.join(outputFolder, 'actinin_msfResults{}.csv'.format(i))
    path3 = os.path.join(outputFolder, 'actinin_cellResults{}.csv'.format(i))
    
    if len(myofibrils) > 1:
        with open(path1,'w', newline='') as f:
            write = csv.writer(f)
            write.writerow(myofibrilHeaders)
            write.writerows(myofibrilStats)
    if len(MSFs) > 1:
        with open(path2, 'w', newline='') as f:
            write = csv.writer(f)
            write.writerow(MSFHeaders)
            write.writerows(MSFStats)
    with open(path3, 'w', newline='') as f:
        write = csv.writer(f)
        write.writerow(cellHeaders)
        write.writerow(cellStats)
    
    #AC: change G_SIZE based on screen resolution?
    G_SIZE = (600, 600)
    (GX, GY) = G_SIZE

    if display is not None:
        image = display
        rawSize = image.size
        img_I = image.convert("I")
        img_array = np.array(img_I)
        if uploadBools[0]:
            img_adj = img_array/25
        else:
            img_adj = img_array
        img_pil = Image.fromarray(img_adj)
        img_to_display = img_pil.convert("RGB")
        img_to_display.thumbnail(G_SIZE)
        newSize = img_to_display.size
        scale = rawSize[0]/newSize[0]

        layout = [[sg.Graph(canvas_size=G_SIZE, graph_bottom_left=(0, GY), graph_top_right=(GX, 0), enable_events=True, key='graph')],
                [sg.Button('Next')]]
        window = sg.Window('Actinin2', layout, finalize=True)
        graph = window['graph']
        image = graph.draw_image(data=conv2png(img_to_display), location = (0,0))
        edgeX2 = edgeX*xres/scale
        edgeY2 = edgeY*xres/scale
        points = np.stack((edgeX2, edgeY2), axis=1)
        x, y = points[0]
   
        for x1,y1 in points:
            graph.draw_line((x,y), (x1,y1), color = 'grey', width = 1)
            x, y = x1, y1
            
        #AC: check all palettes for continuity
        palette = ['#b81dda', '#2ed2d9', '#29c08c', '#f4f933', '#e08f1a']
        p=0

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
                line = graph.draw_line((X1,Y1),(X2,Y2), color = palette[p], width = 2)
            p = (p+1) % 5
        
        for q in range(len(MSFs)):
            MSF = MSFs[q]
            for b in range(0, len(MSF)):
                centerX = (numData[int(MSF[b]-1), headerKeys['x']]*xres)/scale
                centerY = (numData[int(MSF[b]-1), headerKeys['y']]*xres)/scale
                diameter = (numData[int(MSF[b]-1), headerKeys['length']]*xres)/scale
                circle = graph.draw_circle((centerX, centerY), radius = diameter/2, line_color = 'red')

        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED:
                break
            elif event == 'Next':
                break
        window.close()
    
    points = np.stack((edgeX*xres, edgeY*xres), axis=1)
    x, y = points[0]
    filename = "/actininImage{}.jpg".format(i)
    fig, ax = plt.subplots(dpi = 400)

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
        
    for q in range(len(MSFs)):
        MSF = MSFs[q]
        for b in range(0, len(MSF)):
            centerX = (numData[int(MSF[b]-1), headerKeys['x']]*xres)
            centerY = (numData[int(MSF[b]-1), headerKeys['y']]*xres)
            diameter = (numData[int(MSF[b]-1), headerKeys['length']]*xres)
            plt.plot(centerX, -centerY, 'o', markersize = diameter, mec = 'r', mfc = 'w')
        
    plt.axis('equal')
    plt.axis('off')
    plt.subplots_adjust(wspace=None, hspace=None)
    plt.tight_layout()        
    plt.savefig(os.path.join(outputFolder+filename),bbox_inches = 'tight', pad_inches = 0.0) 

    return np.insert(cellStats,0,i)
