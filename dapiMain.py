from actininDataset import ActininDataset
from prepareData import prepareData
import numpy as np
import csv
from binaryMeasure import binaryMeasure
from makeBinary import makeBinary
from getMetadata import getMetadata

def dapiMeasure(i, numData, headerKeys, grey=False):
    cols = 2
    if grey:
        cols = 3
    nuclei = np.where(numData[:, headerKeys['area']] > 20)
    nuclei = nuclei[0]
    numNuclei = len(nuclei)
    areas = []
    if numNuclei > 0:    
        cellDAPIData = np.zeros((len(nuclei), cols))
        for l in range(numNuclei):
            area = numData[int(nuclei[l]), headerKeys['area']]
            areas.append(area)
            cellDAPIData[l,0] = l+1
            cellDAPIData[l,1] = area
        return nuclei, areas, cellDAPIData
    else:
        cellDAPIData = np.zeros((0,2))
        return [], [], cellDAPIData

def dapiMain(folders, dtype, uploadBools):
    if dtype == 'Fixed 2D':
        cols = 4            
        grey = False
        if grey:
            cols = 5
        loader = ActininDataset(folders)
        folderDAPIData = np.zeros((len(loader), cols))
        #print(len(loader))
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
                print(i)
                print('hello')
                print(xres)
                print(image.format)
                numData, headerKeys, bin = makeBinary(image, xres)
            elif uploadBools[1]:
                display = binary
                xres = getMetadata(binary)
                numData, headerKeys = binaryMeasure(binary, xres)
            nuclei, areas, cellDAPIData = dapiMeasure(i, numData, headerKeys, grey)
            folderDAPIData[i, 0] = i+1
            folderDAPIData[i, 1] = len(nuclei)
            folderDAPIData[i, 2] = sum(areas)
            folderDAPIData[i, 3] = np.mean(areas)
            if grey:
                DAPIHeaders = ['Nucleus', 'Area', 'Grey Levels']
                with open('dapi_cell{}.csv'.format(i),'w', newline='') as f:
                    write = csv.writer(f)
                    write.writerow(DAPIHeaders)
                    write.writerows(cellDAPIData)
            else:
                DAPIHeaders = ['Nucleus', 'Area']
                with open('dapi_cell{}.csv'.format(i),'w', newline = '') as f:
                    write = csv.writer(f)
                    write.writerow(DAPIHeaders)
                    write.writerows(cellDAPIData)
        if grey:
            folderHeaders = ['Cell', 'Number of Nuclei', 'Sum Nuclei Area', 'Average Nucleus Size', 'Average Nucleus Grey Levels'] 
        else:
            folderHeaders = ['Cell', 'Number of Nuclei', 'Sum Nuclei Area', 'Average Nucleus Size']
        with open('folder_DAPI.csv', 'w', newline = '') as f:
            write = csv.writer(f)
            write.writerow(folderHeaders)
            write.writerows(folderDAPIData)