from Dataset import Dataset
from binaryMeasure import binaryMeasure
from makeBinary import makeBinary
from prepareData import prepareData
from titinFixed2D import titinFixed2D
from getMetadata import getMetadata
import csv
import numpy as np
import os
import pickle

def titinMain(folders, dtype, uploadBools, edgeMarker = None, edgeFolder = None):
    edgeX = None
    edgeY = None

    if (dtype == 'Fixed 2D'):
        #import data from folders
        loader = Dataset(folders)
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
                if edgeMarker is not None:
                    edgeShape = pickle.load(open(os.path.join(edgeFolder+"/" + "edgeShape_{}".format(i)), "rb"))
                    edgeX, edgeY = edgeShape.exterior.coords.xy
                    edgeX = np.array(edgeX)
                    edgeY = np.array(edgeY)
                if uploadBools[0]:
                    cellStats = titinFixed2D(i, numData, headerKeys, uploadBools, outputFolder, edgeX, edgeY, image, xres)
                elif uploadBools[1]:
                    cellStats = titinFixed2D(i, numData, headerKeys, uploadBools, outputFolder, edgeX, edgeY, binary, xres)
                elif uploadBools[2]:
                    cellStats = titinFixed2D(i, numData, headerKeys, uploadBools, outputFolder, edgeX, edgeY, display=None, xres=1)
                totalCellStats.append(cellStats)          
        else:
            if uploadBools[1]:
                for i in range(len(loader)):
                    image, binary, data_path = loader[i]
                    xres = getMetadata(binary)
                    numData, headerKeys = binaryMeasure(binary, xres)
                    if edgeMarker is not None:
                        edgeShape = pickle.load(open(os.path.join(edgeFolder+"/"+"edgeShape_{}".format(i)),"rb"))
                        edgeX, edgeY = edgeShape.exterior.coords.xy
                        edgeX = np.array(edgeX)
                        edgeY = np.array(edgeY)
                    cellStats = titinFixed2D(i, numData, headerKeys, uploadBools, outputFolder, edgeX, edgeY, binary, xres)
                    totalCellStats.append(cellStats)
            elif uploadBools[0]:
                for i in range(len(loader)):
                    image, binary, data_path = loader[i]
                    xres = getMetadata(image)
                    numData, headerKeys, bin = makeBinary(image, xres)
                    if edgeMarker is not None:
                        edgeShape = pickle.load(open(os.path.join(edgeFolder+"/"+"edgeShape_{}".format(i)), "rb"))
                        edgeX, edgeY = edgeShape.exterior.coords.xy
                        edgeX = np.array(edgeX)
                        edgeY = np.array(edgeY)
                    cellStats = titinFixed2D(i, numData, headerKeys, uploadBools, outputFolder, edgeX, edgeY, image, xres)
                    totalCellStats.append(cellStats)

        if (edgeMarker is not None):
            cellHeaders = ['Cell', 'Total Number of Myofibrils','Total Number of Doublets',
            'Average Myofibril Persistence Length','Average Doublet Length',
            'Average Doublet Spacing', 'Average Size of All Puncta', 'Total Number of Puncta',
            'Number of Rings', 'Average Ring Diameter', 'Average Ring Aspect Ratio', 'Average Doublet Distance from Edge', 
            'Closest Doublet Distance to Edge', 'Average Ring Distance from Edge', 'Closest Ring Distance to Edge']
            folderHeaders = ['Average Myofibrils/Cell', 'Average Doublets/Cell', 'Average Myofibril Persistence Length', 
            'Average Doublet Length', 'Average Doublet Spacing', 'Average Size of All Puncta', 'Average Puncta/Cell',
            'Average Rings/Cell', 'Average Ring Diameter', 'Average Ring Aspect Ratio', 'Average Doublet Distance from Edge',
            'Average Closest Doublet Distance to Edge', 'Average Ring Distance from Edge', 'Average Closest Ring Distance to Edge']
        else:
            cellHeaders = ['Cell', 'Total Number of Myofibrils','Total Number of Doublets',
            'Average Myofibril Persistence Length','Average Doublet Length',
            'Average Doublet Spacing', 'Average Size of All Puncta', 'Total Number of Puncta',
            'Number of Rings', 'Average Ring Diameter', 'Average Ring Aspect Ratio']
            folderHeaders = ['Average Myofibrils/Cell', 'Average Doublets/Cell', 'Average Myofibril Persistence Length', 
            'Average Doublet Length', 'Average Doublet Spacing', 'Average Size of All Puncta', 'Average Puncta/Cell',
            'Average Rings/Cell', 'Average Ring Diameter', 'Average Ring Aspect Ratio']
        
        path1 = os.path.join(outputFolder, "titin_totalResults.csv")
        path2 = os.path.join(outputFolder, "titin_folderMeans.csv")

        with open(path1,'w', newline='') as f:
            write = csv.writer(f)
            write.writerow(cellHeaders)
            write.writerows(totalCellStats) 
            
        totalCellStats = np.asarray(totalCellStats, dtype=object)
        totalCellStats = totalCellStats[:,1:]
        folderMeans = np.nanmean(totalCellStats,axis=0)
        
        with open(path2,'w', newline='') as f:
            write = csv.writer(f)
            write.writerow(folderHeaders)
            write.writerow(folderMeans) 