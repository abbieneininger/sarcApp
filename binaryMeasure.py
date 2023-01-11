from skimage.measure import label, regionprops
import numpy as np
import math

def binaryMeasure(binary, xres):
    binary = np.array(binary)
    mask = binary > 0
    label_img = label(mask)
    regions = regionprops(label_img)
    headerKeys = {"x": 1, 
                    "y": 2, 
                    "length": 3, 
                    "width": 4, 
                    "angle": 6, 
                    "AR": 5,
                    "area": 7,
                    "circ": 8
                    }
    numData = np.zeros((len(regions), 9))
    for i in range(len(regions)):
        if regions[i].minor_axis_length > 0:
            numData[i, 0] = i+1
            centroid = regions[i].centroid
            numData[i, 1] = centroid[1] / xres
            numData[i, 2] = centroid[0] / xres
            numData[i, 3] = regions[i].major_axis_length / xres
            numData[i, 4] = regions[i].minor_axis_length / xres
            if regions[i].minor_axis_length > 0:
                numData[i, 5] = regions[i].major_axis_length / regions[i].minor_axis_length
            radangle = regions[i].orientation
            degangle = np.rad2deg(radangle)
            angle = 90 + degangle
            numData[i, 6] = angle
            numData[i, 7] = regions[i].area / (xres*xres)
            numData[i, 8] = (4*math.pi)*(regions[i].area / regions[i].perimeter)

    return numData, headerKeys

