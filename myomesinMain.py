from re import I
from Dataset import Dataset
from myomesinFixed2D import myomesinFixed2D
from binaryMeasure import binaryMeasure
from makeBinary import makeBinary
from prepareData import prepareData
from getMetadata import getMetadata
import csv
import numpy as np
import os
from findActinEdge import findActinEdge
from findNMIIEdge import findNMIIEdge
from edgeDetection import edgeDetection
from PIL import Image
from alpha_shapes.alpha_shapes import Alpha_Shaper
import pickle

def myomesinMain(folders, dtype, uploadBools, edgeMarker = None, edgeFolder = None):

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
                    cellStats = myomesinFixed2D(i, numData, headerKeys, uploadBools, outputFolder, edgeX, edgeY, image, xres)
                elif uploadBools[1]:
                    cellStats = myomesinFixed2D(i, numData, headerKeys, uploadBools, outputFolder, edgeX, edgeY, binary, xres)
                elif uploadBools[2]:
                    cellStats = myomesinFixed2D(i, numData, headerKeys, uploadBools, outputFolder, edgeX, edgeY, display=None, xres=1)
                totalCellStats.append(cellStats)          
        else:
            if uploadBools[1]:
                for i in range(len(loader)):
                    image, binary, data_path = loader[i]
                    xres = getMetadata(binary)
                    numData, headerKeys = binaryMeasure(binary, xres)
                    if edgeMarker is not None:
                        edgeShape = pickle.load(open(os.path.join(edgeFolder+"/"+"edgeShape_{}".format(i)), "rb"))
                        edgeX, edgeY = edgeShape.exterior.coords.xy
                        edgeX = np.array(edgeX)
                        edgeY = np.array(edgeY)
                    cellStats = myomesinFixed2D(i, numData, headerKeys, uploadBools, outputFolder, edgeX, edgeY, binary, xres)
                    totalCellStats.append(cellStats)
            elif uploadBools[0]:
                for i in range(len(loader)):
                    image, binary, data_path = loader[i]
                    xres = getMetadata(image)
                    numData, headerKeys, bin = makeBinary(image, xres)
                    if edgeMarker is not None:
                        edgeShape = pickle.load(open(os.path.join(edgeFolder+"/"+"edgeShape_{}".format(i)),"rb"))
                        edgeX, edgeY = edgeShape.exterior.coords.xy
                        edgeX = np.array(edgeX)
                        edgeY = np.array(edgeY)
                    cellStats = myomesinFixed2D(i, numData, headerKeys, uploadBools, outputFolder, edgeX, edgeY, image, xres)
                    totalCellStats.append(cellStats)
                    
        cellHeaders = ['Cell','Myofibrils','Total M-lines',
            'Average Myofibril Persistence Length','Average M-Line Length', 
            'Average M-Line Spacing','Average Size of All Puncta', 'Total Puncta']
        folderHeaders = ['Average Myofibrils/Cell','Average M-Lines/Cell',
            'Average Myofibril Persistence Length','Average M-Line Length', 
            'Average Z-Line Spacing','Average Size of All Puncta', 'Average Puncta/Cell']
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
