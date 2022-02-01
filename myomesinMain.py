from actininDataset import ActininDataset
from myomesinFixed2D import main as myomesinFixed2D
from binaryMeasure import binaryMeasure
from makeBinary import makeBinary
from prepareData import prepareData
from getMetadata import getMetadata

def myomesinMain(folders, dtype, uploadBools, channels=False):
    if (dtype == 'Fixed 2D'):
        #import data from folders
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
                    myomesinFixed2D(i, numData, headerKeys, uploadBools, channels, image, xres)
                elif uploadBools[1]:
                    myomesinFixed2D(i, numData, headerKeys, uploadBools, channels, binary, xres)
                elif uploadBools[2]:
                    myomesinFixed2D(i, numData, headerKeys, uploadBools, channels, display=None, xres=1)          
        else:
            if uploadBools[1]:
                for i in range(len(loader)):
                    image, binary, data_path = loader[i]
                    xres = getMetadata(binary)
                    numData, headerKeys = binaryMeasure(binary, xres)
                    myomesinFixed2D(i, numData, headerKeys, uploadBools, channels, binary, xres)
            elif uploadBools[0]:
                for i in range(len(loader)):
                    image, binary, data_path = loader[i]
                    xres = getMetadata(image)
                    numData, headerKeys, bin = makeBinary(image, xres)
                    myomesinFixed2D(i, numData, headerKeys, uploadBools, channels, image, xres)
