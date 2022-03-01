from actininDataset import ActininDataset
import numpy as np
import csv
from getMetadata import getMetadata
import os
import PySimpleGUI as sg
from PIL import Image, ImageGrab
from conv2png import conv2png
import os
from skimage.measure import label, regionprops, profile_line
import matplotlib.pyplot

def NMIIMain(image):
    G_SIZE = (600, 600)
    xres = getMetadata(image)
    rawSize = image.size
    img_I = image.convert("I")
    img_array = np.array(img_I)
    img_adj = img_array/25
    img_pil = Image.fromarray(img_adj)
    img_to_display = img_pil.convert("RGB")
    img_to_display.thumbnail(G_SIZE)
    newSize = img_to_display.size
    scale = rawSize[0]/newSize[0]
    layout = [[sg.Graph(canvas_size=G_SIZE, graph_bottom_left=(0, 600), graph_top_right=(600,0), enable_events=True, key='graph', drag_submits=True)],
                [sg.Button('Next'), sg.Button('Save', key='-SAVE-')]]
    window = sg.Window('Actinin2', layout, finalize=True)
    graph = window['graph']
    image = graph.draw_image(data=conv2png(img_to_display), location = (0,0))
    dragging = False
    final_start = final_end = None
    start_point = end_point = prior_rect = None
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        elif event == 'graph':
            x, y = values['graph']
            if not dragging:
                start_point = (x, y)
                dragging = True
                drag_figures = graph.get_figures_at_location((x,y))
                lastxy = x, y
            else:
                end_point = (x, y)
            if prior_rect:
                graph.delete_figure(prior_rect)
            delta_x, delta_y = x - lastxy[0], y - lastxy[1]
            lastxy = x,y
            if None not in (start_point, end_point):
                prior_rect = graph.draw_line(start_point, end_point, width=4)
        elif event.endswith('+UP'):  # The drawing has ended because mouse up
            final_start = start_point
            final_end = end_point
            start_point, end_point = None, None  # enable grabbing a new rect
            dragging = False
        elif event == "Next":
            break
    window.close()
    #print(final_start, final_end)
    final_start = list(final_start)
    final_end = list(final_end)
    final_start[0] = int((final_start[0]*scale))
    final_start[1] = int((final_start[1]*scale))
    final_end[0] = int((final_end[0]*scale))
    final_end[1] = int((final_end[1]*scale))
    final_start = tuple(final_start)
    final_end = tuple(final_end)
    scan1 = profile_line(img_array, final_start, final_end, mode='nearest')
    scan1pts = len(scan1)
    scan1X = np.linspace(0,scan1pts,num=scan1pts)
    #print(final_start, final_end)
    #print(scan1)

def main():
    img_dir = "C:/Users/abbie/Documents/sarcApp/python/toy data/NMII"
    img_samples = sorted(os.listdir(img_dir))
    img_path = os.path.join(img_dir, img_samples[0])
    img = Image.open(img_path)
    NMIIMain(img)

if __name__ == '__main__':
    main()