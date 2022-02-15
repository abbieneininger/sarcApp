from actininDataset import ActininDataset
from actininFixed2D import actininFixed2D
from binaryMeasure import binaryMeasure
from makeBinary import makeBinary
from prepareData import prepareData
from getMetadata import getMetadata
import csv
import numpy as np
import os

def actininMain(folders, dtype, uploadBools):
    if (dtype == 'Fixed 2D'):
        #import data from folders
        #for now (12/17/21) I'm going to work as if all three folders were chosen
        loader = ActininDataset(folders)
        totalCellStats = []
        outputFolder = folders['-OUT-']
        if uploadBools[2]:
            for i in range(len(loader)):
                image, binary, data_path = loader[i]
                if image is not None:
                    xres = getMetadata(image)
                elif binary is not None:
                    xres = getMetadata(binary)
                numData, headerKeys = prepareData(data_path)
                if uploadBools[0]:
                    cellStats = actininFixed2D(i, numData, headerKeys, uploadBools, outputFolder, image, xres)
                elif uploadBools[1]:
                    cellStats = actininFixed2D(i, numData, headerKeys, uploadBools, outputFolder, binary, xres)
                elif uploadBools[2]:
                    cellStats = actininFixed2D(i, numData, headerKeys, uploadBools, outputFolder, display=None, xres=1)
                totalCellStats.append(cellStats)          
        else:
            if uploadBools[1]:
                for i in range(len(loader)):
                    img, bin, data = loader[i]
                    xres = getMetadata(bin)
                    numData, headerKeys = binaryMeasure(bin, xres)
                    cellStats = actininFixed2D(i, numData, headerKeys, uploadBools, outputFolder, bin, xres)
                    totalCellStats.append(cellStats)
            elif uploadBools[0]:
                for i in range(len(loader)):
                    image, bin, data = loader[i]
                    xres = getMetadata(image)
                    numData, headerKeys, bin = makeBinary(image, xres)
                    cellStats = actininFixed2D(i, numData, headerKeys, uploadBools, outputFolder, image, xres)
                    totalCellStats.append(cellStats)
        #totalCellStats = np.insert(totalCellStats,0,cellCounts)
        cellHeaders = ['Cell','Myofibrils','Total Z-lines',
            'Average Myofibril Persistence Length','Average Z-Line Length', 
            'Average Z-Line Spacing','Average Size of All Puncta', 'Total Puncta',
            'MSFs', 'Total Z-Bodies', 'Average MSF Persistence Length', 
            'Average Z-Body Length', 'Average Z-Body Spacing']
        folderHeaders = ['Mean Myofibrils/Cell','Mean Z-Lines/Cell',
            'Average Myofibril Persistence Length','Average Z-Line Length', 
            'Average Z-Line Spacing','Average Size of All Puncta', 'Mean Puncta/Cell',
            'Mean MSFs/Cell', 'Mean Z-Bodies/Cell', 'Average MSF Persistence Length', 
            'Average Z-Body Length', 'Average Z-Body Spacing']
        path1 = os.path.join(outputFolder, "actinin_totalResults.csv")
        with open(path1,'w', newline='') as f:
            write = csv.writer(f)
            write.writerow(cellHeaders)
            write.writerows(totalCellStats)        
        totalCellStats = np.asarray(totalCellStats)
        totalCellStats = totalCellStats[:,1:]
        folderMeans = np.nanmean(totalCellStats,axis=0)
        path2 = os.path.join(outputFolder, "actinin_folderMeans.csv")
        with open(path2,'w', newline='') as f:
            write = csv.writer(f)
            write.writerow(folderHeaders)
            write.writerow(folderMeans) 


"""         if (uploadBools[0] or uploadBools[1]):
            G_SIZE = (400, 500)
            graph = sg.Graph(canvas_size = G_SIZE, graph_bottom_left=(0, 0), graph_top_right=G_SIZE)
            layout = [[sg.Button('Previous'),graph,sg.Button('Next')],
                    [sg.Button('Draw Edge'), sg.Button('Restart Edge')],
                    [sg.Button('Remove cell'), sg.Button('Break'), sg.Button('Auto Adj LUTs')],
                    #[sg.Slider((1,30),disable_number_display=True, enable_events=True,
                    #       size=(50, 20),orientation='h',key='BRIGHTNESS',default_value=10)],
                    #[sg.Slider((1,30),disable_number_display=True, enable_events=True,
                    #       size=(50, 20), orientation='h',key='CONTRAST',default_value=5)],
                    [sg.Text('Image'), sg.Text(k='-IMGID-'), sg.Text('out of'), sg.Text(k='-N-')]]
            window = sg.Window('actinin', layout, finalize = True)
            i=0
            img, bin, data = loader[0]
            if img is not None:
                img_to_display = img
            else:
                img_to_display = bin
            n = len(loader)
            img_to_display = img_to_display.convert("I")
            img_to_display.thumbnail(G_SIZE)
            img_to_display = conv2png(img_to_display)

            while True:
                imageID = graph.draw_image(data=(img_to_display), location=(0,G_SIZE[1]))
                window['-IMGID-'].update((i+1))
                window['-N-'].update(n)
                event, values = window.read()

                if event == sg.WIN_CLOSED:
                    break
                if event == 'Next':
                    i = (i + 1) % n
                    img, tmpbin, tmpdata = loader[i]
                    img_to_display = img.convert("I")
                    img_to_display.thumbnail(G_SIZE)
                    img_to_display = conv2png(img_to_display)
                if event == 'Draw Edge':
                    pass
                if event == 'Restart Edge':
                    pass
                if event == 'Remove Edge':
                    pass
                if event == 'Break':
                    break
                if event == 'Previous':
                    i = (i + (n-1)) % n
                    img, tmpbin, tmpdata = loader[i]
                    img_to_display = img.convert("I")
                    img_to_display.thumbnail(G_SIZE)
                    img_to_display = conv2png(img_to_display)
                if event == 'Remove Cell':
                    pass
                if event == 'Auto Adj LUTs':
                    img, tmpbin, tmpdata = loader[i]
                    img_to_display = img.convert("I")
                    img_to_display.thumbnail(G_SIZE)
                    img_to_display = conv2png(img_to_display)
                    stat = ImageStat.Stat(img_to_display)
                    print(stat.extrema, img_to_display.size)
                #if event == 'BRIGHTNESS':
                #    value_b = values['BRIGHTNESS']*0.1
                #    img_to_display = ImageEnhance.Brightness(img_to_display.convert('L')).enhance(value_b)
                #if event == 'CONTRAST':
                #    value_c = values['CONTRAST']*0.1
                #    #img_to_display.mode = 'L'
                #    img_to_display = ImageEnhance.Contrast(img_to_display.convert('L')).enhance(value_c)
            window.close() """

#if __name__ == '__main__':
#    main()