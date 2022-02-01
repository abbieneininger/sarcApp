from actininDataset import ActininDataset
from prepareData import prepareData
import numpy as np
import csv
from binaryMeasure import binaryMeasure
from makeBinary import makeBinary
from getMetadata import getMetadata

def paxMeasure(i, numData, headerKeys, grey=False):
    cols = 2
    if grey:
        cols = 3
    adhesions = np.where(numData[:, headerKeys['area']] > 0.2)
    adhesions = adhesions[0]
    numAdhesions = len(adhesions)
    areas = []
    if numAdhesions > 0:
        cellAdhesionArea = np.zeros((len(adhesions), cols))
        for a in range(numAdhesions):
            area = numData[int(adhesions[a]), headerKeys['area']]
            areas.append(area)
            cellAdhesionArea[a,0] = a+1
            cellAdhesionArea[a,1] = area
        return adhesions, areas, cellAdhesionArea
    else:
        cellAdhesionArea = np.zeros((0,2))
        return [], [], cellAdhesionArea

def paxillinMain(folders, dtype, uploadBools):
    if dtype == 'Fixed 2D':
        cols = 4
        grey = False
        if grey:
            cols = 5
        loader = ActininDataset(folders)
        folderAdhesionData = np.zeros((len(loader), cols))
        for i in range(len(loader)):
            image, binary, data_path = loader[i]
            if uploadBools[2]:
                if image is not None:
                    xres = getMetadata(image)
                    display = image
                elif binary is not None:
                    xres = getMetadata(binary)
                    display = binary
                else:
                    display = None
                numData, headerKeys = prepareData(data_path)        
            elif uploadBools[0]:
                display = image
                xres = getMetadata(image)
                numData, headerKeys, bin = makeBinary(image, xres)
            elif uploadBools[1]:
                display = binary
                xres = getMetadata(binary)
                numData, headerKeys = binaryMeasure(binary, xres)
            adhesions, areas, cellAdhesionData = paxMeasure(i, numData, headerKeys, grey)
            folderAdhesionData[i,0] = i+1
            folderAdhesionData[i,1] = len(adhesions)
            folderAdhesionData[i,2] = sum(areas)
            folderAdhesionData[i,3] = np.mean(areas)
            if grey:
                adhesionHeaders = ['Adhesion', 'Area', 'Grey Levels']
                with open('adhesions_cell{}.csv'.format(i), 'w', newline='') as f:
                    write = csv.writer(f)
                    write.writerow(adhesionHeaders)
                    write.writerows(cellAdhesionData)
            else:
                adhesionHeaders = ['Adhesion', 'Area']
                with open('adhesions_cell{}.csv'.format(i), 'w', newline='') as f:
                    write = csv.writer(f)
                    write.writerow(adhesionHeaders)
                    write.writerows(cellAdhesionData)
        if grey:
            folderHeaders = ['Cell', 'Number of Adhesions', 'Average Adhesion Size', 'Average Adhesion Grey Level']
        else:
            folderHeaders = ['Cell', 'Number of Adhesions', 'Average Adhesion Size']
        with open('folder_Adhesions.csv', 'w', newline='') as f:
            write = csv.writer(f)
            write.writerow(folderHeaders)
            write.writerows(folderAdhesionData)
