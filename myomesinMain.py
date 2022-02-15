from actininDataset import ActininDataset
from myomesinFixed2D import myomesinFixed2D
from binaryMeasure import binaryMeasure
from makeBinary import makeBinary
from prepareData import prepareData
from getMetadata import getMetadata
import csv
import numpy as np
import os

def myomesinMain(folders, dtype, uploadBools, channels=False):
    if (dtype == 'Fixed 2D'):
        #import data from folders
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
                    cellStats = myomesinFixed2D(i, numData, headerKeys, uploadBools, outputFolder, channels, image, xres)
                elif uploadBools[1]:
                    cellStats = myomesinFixed2D(i, numData, headerKeys, uploadBools, outputFolder, channels, binary, xres)
                elif uploadBools[2]:
                    cellStats = myomesinFixed2D(i, numData, headerKeys, uploadBools, outputFolder, channels, display=None, xres=1)
                totalCellStats.append(cellStats)          
        else:
            if uploadBools[1]:
                for i in range(len(loader)):
                    image, binary, data_path = loader[i]
                    xres = getMetadata(binary)
                    numData, headerKeys = binaryMeasure(binary, xres)
                    cellStats = myomesinFixed2D(i, numData, headerKeys, uploadBools, outputFolder, channels, binary, xres)
                    totalCellStats.append(cellStats)
            elif uploadBools[0]:
                for i in range(len(loader)):
                    image, binary, data_path = loader[i]
                    xres = getMetadata(image)
                    numData, headerKeys, bin = makeBinary(image, xres)
                    cellStats = myomesinFixed2D(i, numData, headerKeys, uploadBools, outputFolder, channels, image, xres)
                    totalCellStats.append(cellStats)
        cellHeaders = ['Cell','Myofibrils','Total M-lines',
            'Average Myofibril Persistence Length','Average M-Line Length', 
            'Average M-Line Spacing','Average Size of All Puncta', 'Total Puncta']
        folderHeaders = ['Mean Myofibrils/Cell','Mean Z-Lines/Cell',
            'Average Myofibril Persistence Length','Average Z-Line Length', 
            'Average Z-Line Spacing','Average Size of All Puncta', 'Mean Puncta/Cell']
        path1 = os.path.join(outputFolder, "myomesin_totalResults.csv")
        with open(path1,'w', newline='') as f:
            write = csv.writer(f)
            write.writerow(cellHeaders)
            write.writerows(totalCellStats)        
        totalCellStats = np.asarray(totalCellStats)
        totalCellStats = totalCellStats[:,1:]
        folderMeans = np.nanmean(totalCellStats,axis=0)
        path2 = os.path.join(outputFolder, "myomesin_folderMeans.csv")
        with open(path2,'w', newline='') as f:
            write = csv.writer(f)
            write.writerow(folderHeaders)
            write.writerow(folderMeans) 
