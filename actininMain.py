from actininDataset import ActininDataset
from actininFixed2D import actininFixed2D
from binaryMeasure import binaryMeasure
from makeBinary import makeBinary
from prepareData import prepareData
from getMetadata import getMetadata
import csv
import numpy as np
import os

def actininMain(folders, dtype, uploadBools):
    if (dtype == 'Fixed 2D'):
        loader = ActininDataset(folders)
        totalCellStats = []
        outputFolder = folders['-OUT-']
        if uploadBools[2]:
            for i in range(len(loader)):
                image, binary, data_path = loader[i]
                if image is not None:
                    xres = getMetadata(image)
                elif binary is not None:
                    xres = getMetadata(binary)
                numData, headerKeys = prepareData(data_path)
                if uploadBools[0]:
                    cellStats = actininFixed2D(i, numData, headerKeys, uploadBools, outputFolder, image, xres)
                elif uploadBools[1]:
                    cellStats = actininFixed2D(i, numData, headerKeys, uploadBools, outputFolder, binary, xres)
                elif uploadBools[2]:
                    cellStats = actininFixed2D(i, numData, headerKeys, uploadBools, outputFolder, display=None, xres=1)
                totalCellStats.append(cellStats)          
        else:
            if uploadBools[1]:
                for i in range(len(loader)):
                    img, bin, data = loader[i]
                    xres = getMetadata(bin)
                    numData, headerKeys = binaryMeasure(bin, xres)
                    cellStats = actininFixed2D(i, numData, headerKeys, uploadBools, outputFolder, bin, xres)
                    totalCellStats.append(cellStats)
            elif uploadBools[0]:
                for i in range(len(loader)):
                    image, bin, data = loader[i]
                    xres = getMetadata(image)
                    numData, headerKeys, bin = makeBinary(image, xres)
                    cellStats = actininFixed2D(i, numData, headerKeys, uploadBools, outputFolder, image, xres)
                    totalCellStats.append(cellStats)
                    
        cellHeaders = ['Cell','Myofibrils','Total Z-lines',
            'Average Myofibril Persistence Length','Average Z-Line Length', 
            'Average Z-Line Spacing','Average Size of All Puncta', 'Total Puncta',
            'MSFs', 'Total Z-Bodies', 'Average MSF Persistence Length', 
            'Average Z-Body Length', 'Average Z-Body Spacing']
        folderHeaders = ['Average Myofibrils/Cell','Average Z-Lines/Cell',
            'Average Myofibril Persistence Length','Average Z-Line Length', 
            'Average Z-Line Spacing','Average Size of All Puncta', 'Average Puncta/Cell',
            'Average MSFs/Cell', 'Average Z-Bodies/Cell', 'Average MSF Persistence Length', 
            'Average Z-Body Length', 'Average Z-Body Spacing']

        path1 = os.path.join(outputFolder, "actinin_totalResults.csv")
        with open(path1,'w', newline='') as f:
            write = csv.writer(f)
            write.writerow(cellHeaders)
            write.writerows(totalCellStats)        
        totalCellStats = np.asarray(totalCellStats)
        totalCellStats = totalCellStats[:,1:]
        folderMeans = np.nanmean(totalCellStats,axis=0)

        path2 = os.path.join(outputFolder, "actinin_folderMeans.csv")
        with open(path2,'w', newline='') as f:
            write = csv.writer(f)
            write.writerow(folderHeaders)
            write.writerow(folderMeans) 