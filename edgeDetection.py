import numpy as np
from alpha_shapes.alpha_shapes import Alpha_Shaper

def centroid(edgeX, edgeY, scale):
    cx = sum(edgeX) / len(edgeX)
    cy = sum(edgeY) / len(edgeY)
    edgeX = (scale * (edgeX - cx)) + cx
    edgeY = (scale * (edgeY - cy)) + cy
    return edgeX, edgeY

def edgeDetection(numData, headerKeys):
#def main():
    # data_dir = "C:/Users/abbie/Documents/sarcApp/python/toy data/data"
    # data_samples = sorted(os.listdir(data_dir))
    # data_path = os.path.join(data_dir, data_samples[2])
    #img_dir = "C:/Users/abbie/Documents/sarcApp/python/toy data/images"
    #img_samples =sorted(os.listdir(img_dir))
    #img_path = os.path.join(img_dir, img_samples[0])
    #image = Image.open(img_path)
    #rawSize = image.size
    #xres = 9.0909
    # numData, headerKeys = prepareData(data_path)
    x = numData[:, headerKeys['x']]
    y = numData[:, headerKeys['y']]
    points = np.stack((x, y), axis=1)
    #print(np.shape(points))
    shaper = Alpha_Shaper(points)
    alpha = 6.0
    alpha_shape = shaper.get_shape(alpha=alpha)
    edgeX, edgeY = alpha_shape.exterior.coords.xy
    edgeX = np.array(edgeX)
    edgeY = np.array(edgeY)
    #alpha2 = shapely.affinity.scale(alpha_shape, xres, xres, origin=(0,0))
    # edgeX = edgeX.astype(int)
    # edgeY = edgeY.astype(int)
    #alpha2 = shapely.affinity.scale(alpha_shape, xres, xres, origin=(0,0))
    #points2 = list(alpha2.exterior.coords)
    #print(alpha_shape.type, alpha2.type)
    edgeX, edgeY = centroid(edgeX, edgeY, 1.1)
    #points = np.array(alpha_shape.exterior.coords)
    #points = np.asarray(alpha_shape.exterior.coords)
    #points = points * xres
    #points = points.astype(int)
    #print(points)
    #points = points * xres
    #points = points.astype(int)
    #points = list(points)
    #points = list(edgeX, edgeY)
    #points = [(100, 100), (150, 200), (200, 50), (400, 400)]
    #print(points)
    # img = Image.new("L", (rawSize))
    # ImageDraw.Draw(img).polygon(points2, fill='white')
    # img.show()
    # binary = np.array(img)
    # mask = binary > 0
    # label_img = label(mask)
    # regions = regionprops(label_img)
    # headerKeys = {"x": 1, 
    #                 "y": 2, 
    #                 "length": 3, 
    #                 "width": 4, 
    #                 "angle": 6, 
    #                 "AR": 5,
    #                 "area": 7}
    # numData = np.zeros((len(regions), 9))
    # for i in range(len(regions)):
    #     if regions[i].minor_axis_length > 0:
    #         numData[i, 0] = i+1
    #         centroid = regions[i].centroid
    #         numData[i, 1] = centroid[1] / xres
    #         numData[i, 2] = centroid[0] / xres
    #         numData[i, 3] = regions[i].major_axis_length / xres
    #         numData[i, 4] = regions[i].minor_axis_length / xres
    #         if regions[i].minor_axis_length > 0:
    #             numData[i, 5] = regions[i].major_axis_length / regions[i].minor_axis_length
    #         radangle = regions[i].orientation
    #         degangle = np.rad2deg(radangle)
    #         angle = 90 + degangle
    #         numData[i, 6] = angle
    #         numData[i,7] = regions[i].area / (xres*xres)
    #         numData[i, 8] = radangle
    # print(numData[0, headerKeys['angle']])        
    #fig, ax = plt.subplots()
    #fig.tight_layout(pad=0)
    #ax.imshow(img)
    #ax.fill(edgeX, edgeY, facecolor='white')
    #ax.fill(edge2X, edge2Y, facecolor='green')
    #data = np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8)
    #data = data.reshape(fig.canvas.get_width_height()[::-1] + (3,))
    #ax.add_patch(PolygonPatch(points, alpha=0.2, color='r'))
    #print(np.sum(np.array(img) == True))
    #img2 = ImageDraw.Draw(img)
#     #img2.polygon(points, fill = 'white')
    
#     fig, ax1 = plt.subplots()
#     ax1.scatter(*zip(*points))
#     ax1.add_patch(PolygonPatch(alpha_shape, alpha=0.2, color='r'))
#     ax1.set_title(f"$\\alpha={alpha:.2}$")
#     print(alpha_shape)
#     plt.show()
    return edgeX, edgeY, alpha_shape

# if __name__ == '__main__':
#     main()