import numpy as np
from alpha_shapes.alpha_shapes import Alpha_Shaper

def centroid(edgeX, edgeY, scale):
    cx = sum(edgeX) / len(edgeX)
    cy = sum(edgeY) / len(edgeY)
    edgeX = (scale * (edgeX - cx)) + cx
    edgeY = (scale * (edgeY - cy)) + cy
    return edgeX, edgeY

def edgeDetection(numData, headerKeys):
    x = numData[:, headerKeys['x']]
    y = numData[:, headerKeys['y']]
    points = np.stack((x, y), axis=1)
    shaper = Alpha_Shaper(points)
    alpha = 6.0
    while alpha > 0:
        alpha_shape = shaper.get_shape(alpha=alpha)
        try:
            edgeX, edgeY = alpha_shape.exterior.coords.xy
        except AttributeError:
            alpha -=1
        else:
            break
    edgeX = np.array(edgeX)
    edgeY = np.array(edgeY)
    edgeX, edgeY = centroid(edgeX, edgeY, 1.1)
    return edgeX, edgeY, alpha_shape