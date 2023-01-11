from actininMain import actininMain
from myomesinMain import myomesinMain
from paxillinMain import paxillinMain
from dapiMain import dapiMain
from titinMain import titinMain
from NMIIFixed2D import NMIIFixed2D
from actinFixed2D import actinFixed2D

def actininAssign(folders, dtype, uploadBools):
    if uploadBools == [True, True, True]:
        print('sarcApp will now analyze the data and graph the results on your image')
    elif uploadBools == [True, False, False]:
        print('First, sarcApp will generate a binary based on your image')
        print('Then, it will be analyzed')
    elif uploadBools == [True, True, False]:
        print('sarcApp will now use your binary to measure features and graph the results on your image')
    elif uploadBools == [False, True, False]:
        print('sarcApp will now use your binary to measure features and graph the results on your binary')
    elif uploadBools == [False, False, False]:
        print('No data uploaded: Try again')
    else:
        print('sarcApp will now analyze the data: no image or binary uploaded')

    actininMain(folders, dtype, uploadBools)

def actinAssign(folders, dtype, uploadBools):
    print("sarcApp will find the cell edge and save it in the output folder")

    actinFixed2D(folders, dtype, uploadBools)

def paxillinAssign(folders, dtype, uploadBools):
    if uploadBools == [True, True, True]:
        print('sarcApp will now analyze the data, including grey levels')
        #AC: check that this is accurate
    elif uploadBools == [True, False, False]:
        print('First, sarcApp will generate a binary based on your image')
        print('Then, it will be analyzed')
    elif uploadBools == [True, True, False]:
        print('sarcApp will now use your binary to measure features, including grey levels')
    elif uploadBools == [False, True, False]:
        print('sarcApp will now use your binary to measure features, not including grey levels')
    elif uploadBools == [False, False, False]:
        print('No data uploaded: Try again')
    else:
        print('sarcApp will now analyze the data: no image or binary uploaded')

    paxillinMain(folders, dtype, uploadBools)

def myomesinAssign(folders, dtype, uploadBools, edgeFolders, edgeBools, edgeMarker):
    if uploadBools == [True, True, True]:
        print('sarcApp will now analyze the data and graph the results on your image')
    elif uploadBools == [True, False, False]:
        print('First, sarcApp will generate a binary based on your image')
        print('Then, it will be analyzed')
    elif uploadBools == [True, True, False]:
        print('sarcApp will now use your binary to measure features and graph the results on your image')
    elif uploadBools == [False, True, False]:
        print('sarcApp will now use your binary to measure features and graph the results on your binary')
    elif uploadBools == [False, False, False]:
        print('No data uploaded: Try again')
    else:
        print('sarcApp will now analyze the data: no image or binary uploaded')

    myomesinMain(folders, dtype, uploadBools, edgeFolders, edgeBools, edgeMarker)

def titinAssign(folders, dtype, uploadBools, edgeFolders, edgeBools, edgeMarker):
    if uploadBools == [True, True, True]:
        print('sarcApp will now analyze the data and graph the results on your image')
    elif uploadBools == [True, False, False]:
        print('First, sarcApp will generate a binary based on your image')
        print('Then, it will be analyzed')
        print('Be aware that a base Otsu threshold of titin might not result in meaningful data')
    elif uploadBools == [True, True, False]:
        print('sarcApp will now use your binary to measure features and graph the results on your image')
    elif uploadBools == [False, True, False]:
        print('sarcApp will now use your binary to measure features and graph the results on your binary')
    elif uploadBools == [False, False, False]:
        print('No data uploaded: Try again')
    else:
        print('sarcApp will now analyze the data: no image or binary uploaded')

    titinMain(folders, dtype, uploadBools, edgeFolders, edgeBools, edgeMarker)

def NMIIAssign(folders, dtype, uploadBools):
    print("sarcApp will find the cell edge and save it in the output folder")

    NMIIFixed2D(folders, dtype, uploadBools)

def dapiAssign(folders, dtype, uploadBools):
    if uploadBools == [True, True, True]:
        print('sarcApp will now analyze the data, including grey levels')
        #AC: check that this is accurate
    elif uploadBools == [True, False, False]:
        print('First, sarcApp will generate a binary based on your image')
        print('Then, it will be analyzed')
    elif uploadBools == [True, True, False]:
        print('sarcApp will now use your binary to measure features, including grey levels')
    elif uploadBools == [False, True, False]:
        print('sarcApp will now use your binary to measure features, not including grey levels')
    elif uploadBools == [False, False, False]:
        print('No data uploaded: Try again')
    else:
        print('sarcApp will now analyze the data: no image or binary uploaded')

    dapiMain(folders, dtype, uploadBools)

def channelAssignments(channels, folders, numCh):
    dtype = "Fixed 2D"
    edgeBools = None
    edgeFolders = None
    edgeMarker = None

    if 'actinin' in channels.values():
        i = list(channels.values()).index('actinin')
        uploadBools = [bool(folders[i].get('-IMG-')), bool(folders[i].get('-BIN-')), bool(folders[i].get('-DATA-'))]
        actininAssign(folders[i],dtype,uploadBools)
        edgeFolders = folders[i]
        edgeBools = [bool(folders[i].get('-IMG-')), bool(folders[i].get('-BIN-')), bool(folders[i].get('-DATA-'))]
        edgeMarker = 'actinin'
        if 'actin' in channels.values():
            i = list(channels.values()).index('actin')
            uploadBools = [bool(folders[i].get('-IMG-')), bool(folders[i].get('-BIN-')), bool(folders[i].get('-DATA-'))]
            actinAssign(folders[i], dtype, uploadBools)
        if 'NMIIA/B' in channels.values():
            i = list(channels.values()).index('NMIIA/B')
            uploadBools = [bool(folders[i].get('-IMG-')), bool(folders[i].get('-BIN-')), bool(folders[i].get('-DATA-'))]
            NMIIAssign(folders[i], dtype, uploadBools)
    elif 'actin' in channels.values():
        i = list(channels.values()).index('actin')
        uploadBools = [bool(folders[i].get('-IMG-')), bool(folders[i].get('-BIN-')), bool(folders[i].get('-DATA-'))]
        actinAssign(folders[i], dtype, uploadBools)
        edgeFolders = folders[i]
        edgeBools = [bool(folders[i].get('-IMG-')), bool(folders[i].get('-BIN-')), bool(folders[i].get('-DATA-'))]
        edgeMarker = 'actin'
        if 'NMIIA/B' in channels.values():
            i = list(channels.values()).index('NMIIA/B')
            uploadBools = [bool(folders[i].get('-IMG-')), bool(folders[i].get('-BIN-')), bool(folders[i].get('-DATA-'))]
            NMIIAssign(folders[i], dtype, uploadBools)
    elif 'NMIIA/B' in channels.values():
        i = list(channels.values()).index('NMIIA/B')
        uploadBools = [bool(folders[i].get('-IMG-')), bool(folders[i].get('-BIN-')), bool(folders[i].get('-DATA-'))]
        NMIIAssign(folders[i], dtype, uploadBools)
        edgeFolders = folders[i]
        edgeBools = [bool(folders[i].get('-IMG-')), bool(folders[i].get('-BIN-')), bool(folders[i].get('-DATA-'))]
        edgeMarker = 'NMIIA/B'    
    
    if 'paxillin' in channels.values():
        i = list(channels.values()).index('paxillin')
        uploadBools = [bool(folders[i].get('-IMG-')), bool(folders[i].get('-BIN-')), bool(folders[i].get('-DATA-'))]
        paxillinAssign(folders[i],dtype,uploadBools)
    if 'myomesin' in channels.values():
        i = list(channels.values()).index('myomesin')
        uploadBools = [bool(folders[i].get('-IMG-')), bool(folders[i].get('-BIN-')), bool(folders[i].get('-DATA-'))]
        myomesinAssign(folders[i],dtype,uploadBools, edgeFolders, edgeBools, edgeMarker)
    if 'titin N' in channels.values():
        i = list(channels.values()).index('titin N')
        uploadBools = [bool(folders[i].get('-IMG-')), bool(folders[i].get('-BIN-')), bool(folders[i].get('-DATA-'))]
        titinAssign(folders[i],dtype,uploadBools, edgeFolders, edgeBools, edgeMarker)
    if 'dapi' in channels.values():
        i = list(channels.values()).index('dapi')
        uploadBools = [bool(folders[i].get('-IMG-')), bool(folders[i].get('-BIN-')), bool(folders[i].get('-DATA-'))]
        dapiAssign(folders[i],dtype,uploadBools)