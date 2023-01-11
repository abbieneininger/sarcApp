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

def myomesinMain(folders, dtype, uploadBools, edgeFolders = None, edgeBools = None, edgeMarker = None):
    data_dir = None
    if (edgeFolders is not None) and (edgeBools is not None):
        if edgeBools[0]:
            edgeImageFolder = edgeFolders['-IMG-']
        else:
            edgeImageFolder = None
            edgeX = None
            edgeY = None
    else:
        edgeImageFolder = None
        edgeX = None
        edgeY = None

    #AC: is there a better way to do this? save the edge info first
    #Then use it later? What if the edge marker is actinin but no
    #data, only an image/binary? etc.
    #Open the pickles I saved? Make sure to run in order, starting with edge
    
    if edgeMarker == 'actinin':
        edgeImageFolder = None
        data_dir = edgeFolders['-DATA-']
        data_samples = sorted(os.listdir(data_dir))

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
                if edgeImageFolder is not None:
                    img_dir = edgeImageFolder
                    img_samples =sorted(os.listdir(img_dir))
                    img_path = os.path.join(img_dir, img_samples[i])
                    img = Image.open(img_path)
                    xres = getMetadata(img)
                    if edgeMarker == 'actin':
                        edgeX, edgeY = findActinEdge(img, xres)
                    elif edgeMarker == 'NMIIA/B':
                        edgeX, edgeY = findNMIIEdge(img, xres)
                elif edgeMarker == 'actinin':
                    data_path = os.path.join(data_dir, data_samples[i])
                    numData, headerKeys = prepareData(data_path)
                    edgeX, edgeY, shape = edgeDetection(numData, headerKeys)
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
                    if edgeImageFolder is not None:
                        img_dir = edgeImageFolder
                        img_samples =sorted(os.listdir(img_dir))
                        img_path = os.path.join(img_dir, img_samples[i])
                        img = Image.open(img_path)
                        if edgeMarker == 'actin':
                            edgeX, edgeY = findActinEdge(img, xres)
                        elif edgeMarker == 'NMIIA/B':
                            edgeX, edgeY = findNMIIEdge(img, xres)
                    elif edgeMarker == 'actinin':
                        data_path = os.path.join(data_dir, data_samples[i])
                        numData, headerKeys = prepareData(data_path)
                        edgeX, edgeY, shape = edgeDetection(numData, headerKeys)
                    cellStats = myomesinFixed2D(i, numData, headerKeys, uploadBools, outputFolder, edgeX, edgeY, binary, xres)
                    totalCellStats.append(cellStats)
            elif uploadBools[0]:
                for i in range(len(loader)):
                    image, binary, data_path = loader[i]
                    xres = getMetadata(image)
                    numData, headerKeys, bin = makeBinary(image, xres)
                    if edgeImageFolder is not None:
                        img_dir = edgeImageFolder
                        img_samples =sorted(os.listdir(img_dir))
                        img_path = os.path.join(img_dir, img_samples[i])
                        img = Image.open(img_path)
                        if edgeMarker == 'actin':
                            edgeX, edgeY = findActinEdge(img, xres)
                        elif edgeMarker == 'NMIIA/B':
                            edgeX, edgeY = findNMIIEdge(img, xres)
                    elif edgeMarker == 'actinin':
                        data_path = os.path.join(data_dir, data_samples[i])
                        numData, headerKeys = prepareData(data_path)
                        edgeX, edgeY, shape = edgeDetection(numData, headerKeys)
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
