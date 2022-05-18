import numpy as np
from skimage import filters
from skimage import morphology
from scipy import ndimage
from alpha_shapes.alpha_shapes import Alpha_Shaper
import matplotlib.pyplot as plt
from skimage.color import rgb2gray
from PIL import Image
from skimage.filters import gaussian, try_all_threshold
from skimage.segmentation import active_contour, watershed
from skimage.draw import polygon_perimeter
from skimage import measure
from skimage.measure import approximate_polygon
from skimage import feature

def findNMIIEdge(image, xres):
    image = np.array(image)
    rawSize = np.shape(image)
    #fig, ax = try_all_threshold(image, figsize=(10, 8), verbose=False)
    #plt.show()
    #edges1 = feature.canny(image, sigma = 10)
    #edges2 = feature.canny(image, sigma = 5)
    triangle = filters.threshold_otsu(image)
    median = np.median(image)
    print(triangle, median, np.mean(image))
    boundary = triangle / 4
    if triangle < 20: #if otsu detects mostly background
        if median > 0: #but the median makes sense
            triangle = median * 1.2
            print("eee")
        else: #if median and otsu detection are mostly background
            triangle = np.mean(image) * 2.2
    elif median > triangle: #if the median is higher than otsu
        triangle = np.median(image)
    elif median < 5 and triangle >= 20: #if the median is zero but otsu seems fine
        if triangle > (3*np.mean(image)):
            print('hello')
            triangle = triangle / 3
        else:
            triangle = triangle
    else:
        triangle = (triangle + median) / 2 #in all other situations, average the two boundaries
    print(triangle, boundary)
    if (triangle > (boundary * 2)) and (boundary > 5):
        boundary = triangle/1.5
    else:
        boundary = triangle
    #boundary = triangle
    markers = np.zeros_like(image)
    markers[image<30] = 1
    print(boundary, 'is being used')
    markers[image>boundary] = 2
    #triImage = image > (triangle/4)
    triImage = watershed(image, markers)
    triImage -= 1
    triBool = triImage.astype(bool)
    triDilate = ndimage.binary_dilation(triBool)
    #print(np.min(triImage), np.max(triImage))
    #print(triBool)
    triSmall = morphology.remove_small_objects(triDilate, min_size=250)
    triFilled = ndimage.binary_fill_holes(triSmall,structure=np.ones((10,10)))
    #edge1 = feature.canny(triImage, sigma = 10)
    #triFilledSmall = morphology.remove_small_objects(triFilled, min_size=1000)
    edge2 = filters.sobel(triFilled)
    
    # fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(8, 3))

    # ax[0].imshow(triSmall, cmap='gray')
    # ax[0].set_title('tri small', fontsize=20)

    # ax[1].imshow(triImage, cmap='gray')
    # ax[1].set_title(r'watershed', fontsize=20)

    # ax[2].imshow(triFilled, cmap='gray')
    # ax[2].set_title(r'holes filled', fontsize=20)

    # for a in ax:
    #     a.axis('off')

    # fig.tight_layout()
    # plt.show()


    coords = np.where(edge2 > 0)
    coords = np.flip(coords, axis=0)
    print(len(coords[0]))
    if len(coords[0]) == 0:
        print("help")
        print(triangle)
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
        print(alpha_opt)    
        alpha = 6.0                
        edgeX = None
        edgeY = None
        #while alpha > 0:
        alpha_shape = shaper.get_shape(alpha=alpha)
        try:
            edgeX, edgeY = alpha_shape.exterior.coords.xy
            edgeX = np.array(edgeX)
            edgeY = np.array(edgeY)
            return edgeX, edgeY
        except AttributeError:
            print('error')
            alpha_shape = shaper.get_shape(alpha=1)
            try:
                edgeX, edgeY = alpha_shape.exterior.coords.xy
                edgeX = np.array(edgeX)
                edgeY = np.array(edgeY)
                return edgeX, edgeY
            except AttributeError:
                return None, None
    except ValueError:
        print("no cell was found in this image")
        return None, None


   