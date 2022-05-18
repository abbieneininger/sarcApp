from actininDataset import ActininDataset
from binaryMeasure import binaryMeasure
from makeBinary import makeBinary
from prepareData import prepareData
from titinFixed2D import titinFixed2D
from getMetadata import getMetadata
import csv
import numpy as np
import os
from findActinEdge import findActinEdge
from findNMIIEdge import findNMIIEdge
from PIL import Image
from edgeDetection import edgeDetection


def titinMain(folders, dtype, uploadBools, edgeFolders = None, edgeBools = None, edgeMarker = None):
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

    if edgeMarker == 'actinin':
        edgeImageFolder = None
        data_dir = edgeFolders['-DATA-']
        data_samples = sorted(os.listdir(data_dir))

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
                    edgeX, edgeY = edgeDetection(numData, headerKeys)
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
                    img, bin, data = loader[i]
                    xres = getMetadata(bin)
                    numData, headerKeys = binaryMeasure(bin, xres)
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
                        edgeX, edgeY = edgeDetection(numData, headerKeys)
                    cellStats = titinFixed2D(i, numData, headerKeys, uploadBools, outputFolder, edgeX, edgeY, binary, xres)
                    totalCellStats.append(cellStats)
            elif uploadBools[0]:
                for i in range(len(loader)):
                    image, bin, data = loader[i]
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
                        edgeX, edgeY = edgeDetection(numData, headerKeys)
                    cellStats = titinFixed2D(i, numData, headerKeys, uploadBools, outputFolder, edgeX, edgeY, image, xres)
                    totalCellStats.append(cellStats)

        if (edgeImageFolder is not None) and (data_dir is not None):
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
            
        #print(totalCellStats)
        #totalCellStats = totalCellStats[0]
        #print(totalCellStats)
        totalCellStats = np.asarray(totalCellStats, dtype=object)
        #print(totalCellStats)
        totalCellStats = totalCellStats[:,1:]
        #print(totalCellStats)
        folderMeans = np.nanmean(totalCellStats,axis=0)
        
        with open(path2,'w', newline='') as f:
            write = csv.writer(f)
            write.writerow(folderHeaders)
            write.writerow(folderMeans) 