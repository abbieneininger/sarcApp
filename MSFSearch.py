import numpy as np
import math

def MSFSearch(numData, Zbodies, headerKeys, edgeX, edgeY, actin=False):
    maxDistance = 3
    maxAngleDifference = 15
    index = np.linspace(0,len(Zbodies)-1,len(Zbodies))
    index2 = np.zeros(shape=(len(Zbodies),))
    index = np.expand_dims(index,0)
    index2 = np.expand_dims(index2,0)
    index3 = np.concatenate((index, index2), axis = 0)
    MSFCount = 0
    for i in range(len(Zbodies)):
        if (numData[Zbodies[i], headerKeys['x']] > 0):
            X = numData[Zbodies[i], headerKeys['x']]
            Y = numData[Zbodies[i], headerKeys['y']]
            distToEdge = []
            for p in range(len(edgeX)):
                tmpX = edgeX[p]
                tmpY = edgeY[p]
                distToEdge.append(math.sqrt((tmpX-X)**2+(tmpY-Y)**2))
            edgeIdx = np.argmin(distToEdge)
            #find relative slope of the edge in this area
            for j in range(i+1,len(Zbodies)):
                XJ = numData[Zbodies[j], headerKeys['x']]
                if XJ == X:
                    XJ += 0.001
                YJ = numData[Zbodies[j], headerKeys['y']]
                distance = math.sqrt((Y-YJ)**2+(X-XJ)**2)
                if distance < maxDistance:
                    distToEdge2 = []
                    for p in range(len(edgeX)):
                        tmpX = edgeX[p]
                        tmpY = edgeY[p]
                        distToEdge2.append(math.sqrt((tmpX-X)**2+(tmpY-Y)**2))
                    edgeIdx2 = np.argmin(distToEdge2)
                    if ((edgeIdx == edgeIdx2) and (edgeIdx < len(edgeX))):
                        edgeIdx2 += 1
                    elif edgeIdx == len(edgeX):
                        edgeIdx2 = edgeIdx - 1
                    e1X = edgeX[int(edgeIdx)]
                    e1Y = edgeY[int(edgeIdx)]
                    e2X = edgeX[int(edgeIdx2)]
                    e2Y = edgeY[int(edgeIdx2)] 
                    if e1X == e2X:
                        e2X += 0.001
                    edgeSlope = 180-np.rad2deg(np.arctan(e2Y-e1Y)/(e2X-e1X))              
                    mC = (Y-YJ)/(X-XJ)
                    mA = 180-np.rad2deg(np.arctan(mC))
                    angleDifference = abs(mA-edgeSlope)
                    if angleDifference < maxAngleDifference:
                        if (index3[1, i] == 0 and index3[1, j] == 0):
                            MSFCount += 1
                            index3[1, i] = MSFCount
                            index3[1, j] = MSFCount
                        elif (index3[1, i] > 0 and index3[1, j] == 0):
                            index3[1, j] = index3[1, i]
                        elif (index3[1, i] == 0 and index3[1, j] > 0):
                            index3[1, i] = index3[1, j]
                        else:
                            MSFToDelete = index3[1, j]
                            index3[1, j] = index3[1, i]
                            for s in range(len(Zbodies)):
                                if index3[1, s] == MSFToDelete:
                                    index3[1, s] == index3[1, i]
    MSFIndices = np.unique(index3[1,:])-1
    minBodies = 4
    MSFCount = 0
    ZBodyCount = 0
    MSFIdentities = []
    for k in range(len(MSFIndices+1)):
        if np.sum(index3[1,:] == k+1) > minBodies:
            MSFCount += 1
            bodyIndices = np.where(index3[1, :] == k+1)
            bodyIndices = bodyIndices[0]
            ZBodyCount += len(bodyIndices)
            ZBodyIdentities = numData[Zbodies[bodyIndices],0]
            MSFIdentities.append(ZBodyIdentities)
    return(MSFIdentities)


# def main():
#     img_dir = "C:/Users/abbie/Documents/sarcApp/python/toy data/images"
#     img_samples =sorted(os.listdir(img_dir))
#     img_path = os.path.join(img_dir, img_samples[3])
#     image = Image.open(img_path)
#     xres = getMetadata(image)
#     data_dir = "C:/Users/abbie/Documents/sarcApp/python/toy data/data"
#     data_samples = sorted(os.listdir(data_dir))
#     data_path = os.path.join(data_dir, data_samples[3])
#     bin_dir = "C:/Users/abbie/Documents/sarcApp/python/toy data/binaries"
#     bin_samples = sorted(os.listdir(bin_dir))
#     numData, headerKeys = prepareData(data_path)
#     #separate Z lines and Z bodies based on length, at first
#     Zlines, Zbodies = separateObjects(numData, headerKeys['length'])
#     edgeX, edgeY, edge_shape = edgeDetection(numData, headerKeys)
#     MSFs = MSFSearch(numData, Zbodies, headerKeys, edgeX, edgeY)
#     #print(MSFs)
#     G_SIZE = (400, 600)
#     rawSize = image.size
#     img_I = image.convert("I")
#     img_array = np.array(img_I)
#     img_adj = img_array/25
#     img_pil = Image.fromarray(img_adj)
#     img_to_display = img_pil.convert("RGB")
#     img_to_display.thumbnail(G_SIZE)
#     newSize = img_to_display.size
#     scale = rawSize[0]/newSize[0]
#     layout = [[sg.Graph(canvas_size=G_SIZE, graph_bottom_left=(0, 600), graph_top_right=(400,0), enable_events=True, key='graph')],
#           [sg.Button('button')]]
#     window = sg.Window('Graph test', layout, finalize=True)
#     graph = window['graph']
#     #circle = graph.draw_circle((75, 75), 25, fill_color='black', line_color='white')
#     image = graph.draw_image(data=conv2png(img_to_display), location = (0,0))
#     edgeX = edgeX*xres/scale
#     edgeY = edgeY*xres/scale
#     points = np.stack((edgeX, edgeY), axis=1)
#     x, y = points[0]
#     for x1,y1 in points:
#         graph.draw_line((x,y), (x1,y1), color = 'grey', width = 1)
#         x, y = x1, y1
#     palette = ['#b81dda', '#2ed2d9', '#29c08c', '#f4f933', '#e08f1a']
#     p=0
#     for m in range(len(MSFs)):    
#         MSF = MSFs[m]
#         for b in range(0, len(MSF)):
#             centerX = (numData[int(MSF[b]-1), headerKeys['x']]*xres)/scale
#             centerY = (numData[int(MSF[b]-1), headerKeys['y']]*xres)/scale
#             diameter = (numData[int(MSF[b]-1), headerKeys['length']]*xres)/scale
#             circle = graph.draw_circle((centerX, centerY), radius = diameter/2, line_color = palette[p])
#         p = (p+1) % 5

#     while True:
#         event, values = window.read()
#         #print(event, values)
#         if event == sg.WIN_CLOSED:
#             break
#     window.close()

# if __name__ == '__main__':
#     main()