import numpy as np
import csv

#AC: come back to this, should I get grey level data?
def prepareData(data_path):
    with open(data_path, 'r') as f:
        data = list(csv.reader(f))
    headers = np.array(data[0])
    numData = np.array(data[1:]).astype(float)
    #find header information
    xColumn = np.where(headers == 'X')
    xColumn = xColumn[0]
    yColumn = np.where(headers == 'Y')
    yColumn = yColumn[0]
    lengthColumn = np.where(headers == 'Major')
    lengthColumn = lengthColumn[0]
    widthColumn = np.where(headers == 'Minor')
    widthColumn = widthColumn[0]
    angleColumn = np.where(headers == 'Angle')
    angleColumn = angleColumn[0]
    aspectRatioColumn = np.where(headers == 'AR')
    aspectRatioColumn = aspectRatioColumn[0]
    areaColumn = np.where(headers == 'Area')
    areaColumn = areaColumn[0]
    circColumn = np.where(headers == 'Circ.')
    circColumn = circColumn[0]
    headerKeys = {"x": xColumn[0], 
                    "y": yColumn[0], 
                    "length": lengthColumn[0], 
                    "width": widthColumn[0], 
                    "angle": angleColumn[0], 
                    "AR": aspectRatioColumn[0],
                    "area": areaColumn[0],
                    "circ": circColumn[0]}
    return numData, headerKeys
