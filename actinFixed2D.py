import numpy as np
import os
from PIL import Image
import PySimpleGUI as sg
from conv2png import conv2png
from findActinEdge import findEdge

def actinFixed2D(i, uploadBools, outputFolder = 0, channels = False, display = None, xres = 1):
    image = display
    edgeX, edgeY = findEdge(image, xres)
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
                [sg.Button('Next'), sg.Button('Save', key='-SAVE-')]]

    window = sg.Window('Actin', layout, finalize=True)
    graph = window['graph']
    image = graph.draw_image(data=conv2png(img_to_display), location = (0,0))
    edgeX = edgeX*xres/scale
    edgeY = edgeY*xres/scale
    points = np.stack((edgeX, edgeY), axis=1)
    x, y = points[0]
    for x1,y1 in points[1:]:
        graph.draw_line((x,y), (x1,y1), color = 'white', width = 1)
        x, y = x1, y1

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        elif event == '-SAVE-':
            pass
        elif event == 'Next':
            break
    window.close()

def main():
    i=0
    img_dir = "E:/Blebbistatin MYH6-7 Project/24H_BB_FixPerm_031421/MaxIPs/actin/BB50/images_ROIs"
    img_samples =sorted(os.listdir(img_dir))
    img_path = os.path.join(img_dir, img_samples[21])
    img = Image.open(img_path)
    xres = 9.0909
    uploadBools = [True, False, False]
    outputFolder = "E:/Blebbistatin MYH6-7 Project/24H_BB_FixPerm_031421/MaxIPs/actin/BB50/output"
    actinFixed2D(i, uploadBools, outputFolder, channels=False, display = img, xres=xres)

if __name__ == '__main__':
    main()
