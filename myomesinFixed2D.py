import numpy as np
import PySimpleGUI as sg
from PIL import Image
from myofibrilSearch import myofibrilSearch
from calcMyofibrils import calcMyofibrils
import csv
from conv2png import conv2png
import os
import matplotlib.pyplot as plt

def separateObjects(data, lengthColumn):
    lines = np.where(data[:, lengthColumn]>=1.4)
    return lines[0]

def myomesinFixed2D(i, numData, headerKeys, uploadBools, outputFolder, edgeX = None, edgeY = None, display = None, xres=1):
    #format the data
    #separate Z lines and Z bodies based on length, at first
    Mlines = separateObjects(numData, headerKeys['length'])
    prefix = 'M-'
    myofibrils = myofibrilSearch(numData, Mlines, headerKeys, 'myomesin')   
    
    if display is not None:
        imgsize = display.size
    else:
        imgsize = None
    
    cellHeaders = ['Total Number of Myofibrils','Total Number of {}Lines'.format(prefix),
            'Average Myofibril Persistence Length','Average {}Line Length'.format(prefix), 
            'Average {}Line Spacing'.format(prefix),'Average Size of All Puncta', 'Total Number of Puncta']
    
    if edgeX is not None:
        myofibrilHeaders = ['Myofibril','Number of {}Lines'.format(prefix),'Average Spacing',
            'Persistence Length','Angle of Myofibril Long Axis',
            'Average {}Line Length'.format(prefix), 'Distance from the Edge', 'Edge Angle', 'Normalized Myofibril Angle Compared to Edge']  
    else:
        myofibrilHeaders = ['Myofibril','Number of {}Lines'.format(prefix),'Average Spacing',
            'Persistence Length','Angle of Myofibril Long Axis',
            'Average {}Line Length'.format(prefix)]
    
    myofibrilStats, cellStats = calcMyofibrils(numData, myofibrils, headerKeys, edgeX, edgeY, xres, 'myomesin', display)
    
    path1 = os.path.join(outputFolder, 'myomesin_mfResults{}.csv'.format(i))
    path2 = os.path.join(outputFolder, 'myomesin_cellResults{}.csv'.format(i))
    
    if len(myofibrils) > 1:
        with open(path1,'w', newline='') as f:
            write = csv.writer(f)
            write.writerow(myofibrilHeaders)
            write.writerows(myofibrilStats)
    with open(path2, 'w', newline='') as f:
        write = csv.writer(f)
        write.writerow(cellHeaders)
        write.writerows(cellStats)

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
        filename = "/myomesinImage{}.jpg".format(i)
        fig, ax = plt.subplots(dpi = 400)
        layout = [[sg.Graph(canvas_size=G_SIZE, graph_bottom_left=(0, GY), graph_top_right=(GX,0), enable_events=True, key='graph')],
                [sg.Button('Next'), sg.Button('Save', key='-SAVE-')]]

        window = sg.Window('Myomesin', layout, finalize=True)
        graph = window['graph']
        image = graph.draw_image(data=conv2png(img_to_display), location = (0,0))
        if edgeX is not None:
            edgeX = edgeX*xres/scale
            edgeY = edgeY*xres/scale
            points = np.stack((edgeX, edgeY), axis=1)
            x, y = points[0]

            for x1,y1 in points:
                graph.draw_line((x,y), (x1,y1), color = 'grey', width = 1)
                plt.plot([x,x1],[-y,-y1], color = 'grey', linewidth = 1)
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
                line = graph.draw_line((X1,Y1),(X2,Y2), color = palette[p], width = 1)
                plt.plot([X1,X2],[-Y1,-Y2], color = palette[p], linewidth = 2)
            p = (p+1) % 5

        plt.axis('equal')
        plt.axis('off')
        plt.subplots_adjust(wspace=None, hspace=None)
        plt.tight_layout()        
        plt.savefig(os.path.join(outputFolder+filename),bbox_inches = 'tight', pad_inches = 0.0) 
        
        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED:
                break
            elif event == 'Next':
                break
        window.close()

    return np.insert(cellStats,0,i)