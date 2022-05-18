import numpy as np
from skimage import filters
from skimage import morphology
from scipy import ndimage
from alpha_shapes.alpha_shapes import Alpha_Shaper
import matplotlib.pyplot as plt
from skimage.color import rgb2gray
from PIL import Image
from skimage.filters import gaussian
from skimage.segmentation import active_contour
from skimage.draw import polygon_perimeter
from skimage import measure
from skimage.measure import approximate_polygon

def findActinEdge(image, xres):
    image = np.array(image)
    rawSize = np.shape(image)
    triangle = filters.threshold_otsu(image)
    median = np.median(image)
    print(triangle, median, np.mean(image))
    if triangle < 5:
        if median > 0:
            triangle = median * 1.2
        else:
            triangle = np.mean(image) * 2.2
    elif median > triangle:
        triangle = np.median(image)
    elif median == 0 and triangle >= 5:
        triangle = triangle
    else:
        triangle = (triangle + median) / 2
    triImage = image > (triangle*1)
    triSmall = morphology.remove_small_objects(triImage, min_size=1000)
    triFilled = ndimage.binary_fill_holes(triSmall)
    edge2 = filters.sobel(triFilled)
    coords = np.where(edge2 > 0)
    coords = np.flip(coords, axis=0)
    print(len(coords[0]))
    if len(coords[0]) == 0:
        print("help")
        print(triangle)
        triImage = image > np.median(image)
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
        #print(alpha_opt)    
        alpha = 40                
        edgeX = None
        edgeY = None
        #while alpha > 0:
        alpha_shape = shaper.get_shape(alpha=alpha)
        try:
            edgeX, edgeY = alpha_shape.exterior.coords.xy
        except AttributeError:
            alpha_shape = shaper.get_shape(alpha=1)
            edgeX, edgeY = alpha_shape.exterior.coords.xy
        edgeX = np.array(edgeX)
        edgeY = np.array(edgeY)
        return edgeX, edgeY
    except ValueError:
        print("no cell was found in this image")
        return None, None


   