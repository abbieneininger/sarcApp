from skimage import filters
from skimage.measure import label, regionprops
import numpy as np

def makeBinary(image, xres):
    image = np.array(image)
    threshold=filters.threshold_otsu(image)
    mask = image > threshold
    label_img = label(mask)
    regions = regionprops(label_img)
    headerKeys = {"x": 1, 
                    "y": 2, 
                    "length": 3, 
                    "width": 4, 
                    "angle": 6, 
                    "AR": 5,
                    "area": 7}
    numData = np.zeros((len(regions), 8))
    for i in range(len(regions)):            
        numData[i, 0] = i+1
        if regions[i].minor_axis_length > 0:
            centroid = regions[i].centroid
            numData[i, 1] = centroid[1] / xres
            numData[i, 2] = centroid[0] / xres
            numData[i, 3] = regions[i].major_axis_length / xres
            numData[i, 4] = regions[i].minor_axis_length / xres
            numData[i, 5] = regions[i].major_axis_length / regions[i].minor_axis_length
            radangle = regions[i].orientation
            degangle = np.rad2deg(radangle)
            angle = 90 + degangle
            numData[i, 6] = angle
            numData[i, 7] = regions[i].area / (xres * xres)
    return numData, headerKeys, mask