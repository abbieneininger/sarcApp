from actininDataset import ActininDataset
from binaryMeasure import binaryMeasure
from makeBinary import makeBinary
from prepareData import prepareData
from titinFixed2D import titinFixed2D
from getMetadata import getMetadata

def titinMain(folders, dtype, uploadBools, channels=False):
    if (dtype == 'Fixed 2D'):
        #print('data type is fixed 2-dimensional data')
        #import data from folders
        #for now (12/17/21) I'm going to work as if all three folders were chosen
        loader = ActininDataset(folders)
        if uploadBools[2]:
            for i in range(len(loader)):
                image, binary, data_path = loader[i]
                if image is not None:
                    xres = getMetadata(image)
                elif binary is not None:
                    xres = getMetadata(binary)
                numData, headerKeys = prepareData(data_path)
                if uploadBools[0]:
                    titinFixed2D(i, numData, headerKeys, uploadBools, channels=False, display=image, xres=xres)
                elif uploadBools[1]:
                    titinFixed2D(i, numData, headerKeys, uploadBools, channels=False, display=binary, xres=xres)
                elif uploadBools[2]:
                    titinFixed2D(i, numData, headerKeys, uploadBools, channels-False, display=None, xres=1)          
        else:
            if uploadBools[1]:
                for i in range(len(loader)):
                    img, bin, data = loader[i]
                    xres = getMetadata(bin)
                    numData, headerKeys = binaryMeasure(bin, xres)
                    titinFixed2D(i, numData, headerKeys, uploadBools, channels = False, display=bin, xres=xres)
            elif uploadBools[0]:
                for i in range(len(loader)):
                    image, bin, data = loader[i]
                    xres = getMetadata(image)
                    numData, headerKeys, bin = makeBinary(image, xres)
                    titinFixed2D(i, numData, headerKeys, uploadBools, channels = False, display=image, xres=xres)