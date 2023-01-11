import numpy as np
import os
from PIL import Image
import PySimpleGUI as sg
from conv2png import conv2png
from findActinEdge import findActinEdge
import matplotlib.pyplot as plt
import pickle
from Dataset import Dataset
from getMetadata import getMetadata

#def actinFixed2D(i, uploadBools, outputFolder = 0, channels = False, display = None, xres = 1):
def actinFixed2D(folders, dtype, uploadBools):
    if dtype == 'Fixed 2D':
        loader = Dataset(folders)
        outputFolder = folders['-OUT-']
        if uploadBools[0]:
            for i in range(len(loader)):
                image, binary, data_path = loader[i]
                xres = getMetadata(image)
                edgeX, edgeY, edge_shape = findActinEdge(image, xres)
                f = open(os.path.join(outputFolder + "/edgeShape_{}".format(i)), "wb")
                pickle.dump(edge_shape, f)
                f.close()
                #AC: change G_SIZE based on screen resolution?
                G_SIZE = (600, 600)
                (GX, GY) = G_SIZE
                rawSize = image.size
                img_I = image.convert("I")
                img_array = np.array(img_I)
                if uploadBools[0]:
                    img_adj = img_array
                else:
                    img_adj = img_array
                img_pil = Image.fromarray(img_adj)
                img_to_display = img_pil.convert("RGB")
                img_to_display.thumbnail(G_SIZE)
                newSize = img_to_display.size
                scale = rawSize[0]/newSize[0]
                layout = [[sg.Graph(canvas_size=G_SIZE, graph_bottom_left=(0, GY), graph_top_right=(GX, 0), enable_events=True, key='graph')],
                            [sg.Button('Next')]]

                window = sg.Window('Actin', layout, finalize=True)
                graph = window['graph']
                image = graph.draw_image(data=conv2png(img_to_display), location = (0,0))
                edgeX = edgeX*xres/scale
                edgeY = edgeY*xres/scale
                points = np.stack((edgeX, edgeY), axis=1)
                x, y = points[0]
                filename = "/actinEdgeImage{}.jpg".format(i)
                fig, ax = plt.subplots(dpi = 400)
                for x1,y1 in points[1:]:
                    graph.draw_line((x,y), (x1,y1), color = 'white', width = 1)
                    plt.plot([x,x1],[-y,-y1], color = 'grey', linewidth = 1)
                    x, y = x1, y1
                
                plt.axis('equal')
                plt.axis('off')
                plt.subplots_adjust(wspace=None, hspace=None)
                plt.tight_layout()        
                plt.savefig(os.path.join(outputFolder+filename),bbox_inches = 'tight', pad_inches = 0.0) 
                
                while True:
                    event, values = window.read()
                    if event == sg.WIN_CLOSED:
                        break
                    elif event == 'Next':
                        break
                window.close()
