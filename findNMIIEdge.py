import numpy as np
from skimage import filters
from skimage import morphology
from scipy import ndimage
from alpha_shapes.alpha_shapes import Alpha_Shaper
from skimage.segmentation import watershed

def findNMIIEdge(image, xres):
    image = np.array(image)
    triangle = filters.threshold_otsu(image)
    median = np.median(image)
    boundary = triangle / 4

    if triangle < 20: #if otsu detects mostly background
        if median > 0: #but the median makes sense
            triangle = median * 1.2
        else: #if median and otsu detection are mostly background
            triangle = np.mean(image) * 2.2
    elif median > triangle: #if the median is higher than otsu
        triangle = np.median(image)
    elif median < 5 and triangle >= 20: #if the median is zero but otsu seems fine
        if triangle > (3*np.mean(image)):
            triangle = triangle / 3
        else:
            triangle = triangle
    else:
        triangle = (triangle + median) / 2 #in all other situations, average the two boundaries

    if (triangle > (boundary * 2)) and (boundary > 5):
        boundary = triangle/1.5
    else:
        boundary = triangle

    markers = np.zeros_like(image)
    markers[image<30] = 1
    markers[image>boundary] = 2
    triImage = watershed(image, markers)
    triImage -= 1
    triBool = triImage.astype(bool)
    triDilate = ndimage.binary_dilation(triBool)
    triSmall = morphology.remove_small_objects(triDilate, min_size=250)
    triFilled = ndimage.binary_fill_holes(triSmall,structure=np.ones((10,10)))
    edge2 = filters.sobel(triFilled)
    coords = np.where(edge2 > 0)
    coords = np.flip(coords, axis=0)

    if len(coords[0]) == 0:
        triImage = image > (triangle+median+median) / 3
        triSmall = morphology.remove_small_objects(triImage, min_size=1000)
        triFilled = ndimage.binary_fill_holes(triSmall)
        edge2 = filters.sobel(triFilled)
        coords = np.where(edge2 > 0)
        coords = np.flip(coords, axis=0)

    x = coords[0] / xres
    y = coords[1] / xres
    points = np.stack((x, y), axis=1)

    try:
        shaper = Alpha_Shaper(points)    
        alpha_opt, alpha_shape = shaper.optimize()  
        alpha = 6.0                
        edgeX = None
        edgeY = None
        alpha_shape = shaper.get_shape(alpha=alpha)
        try:
            edgeX, edgeY = alpha_shape.exterior.coords.xy
            edgeX = np.array(edgeX)
            edgeY = np.array(edgeY)
            return edgeX, edgeY
        except AttributeError:
            alpha_shape = shaper.get_shape(alpha=1)
            try:
                edgeX, edgeY = alpha_shape.exterior.coords.xy
                edgeX = np.array(edgeX)
                edgeY = np.array(edgeY)
                return edgeX, edgeY, alpha_shape
            except AttributeError:
                return None, None, None
    except ValueError:
        #AC: print cell filename/ID
        print("No cell was found in this image")
        return None, None, None


   