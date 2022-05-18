from actininMain import actininMain
from myomesinMain import myomesinMain
from paxillinMain import paxillinMain
from dapiMain import dapiMain
from titinMain import titinMain
from NMIIMain import NMIIMain
from actinMain import actinMain

def actininAssign(folders, dtype, uploadBools):
    if uploadBools == [True, True, True]:
        pass
    elif uploadBools == [True, False, False]:
        print('first we gotta make a binary')
        print('then we gotta analyze it')
    elif uploadBools == [True, True, False]:
        print('we just have to analyze the binary you made!')
    elif uploadBools == [False, True, False]:
        print('we just have to analyze the binary you made!')
        print('no image though so there wont be grey level data')
    elif uploadBools == [False, False, False]:
        print('u didnt upload any data')
    else:
        print('you already have data but are either missing the image, binary, or both')
        print('no worries!')
    actininMain(folders, dtype, uploadBools)

def actinAssign(folders, dtype, uploadBools):
    actinMain(folders, dtype, uploadBools)

def paxillinAssign(folders, dtype, uploadBools):
    if uploadBools == [True, True, True]:
        pass
    elif uploadBools == [True, False, False]:
        print('first we gotta make a binary')
        print('then we gotta analyze it')
    elif uploadBools == [True, True, False]:
        print('we just have to analyze the binary you made!')
    elif uploadBools == [False, True, False]:
        print('we just have to analyze the binary you made!')
        print('no image though so there wont be grey level data')
    elif uploadBools == [False, False, False]:
        print('u didnt upload any data')
    else:
        print('you already have data but are either missing the image, binary, or both')
        print('no worries!')
    paxillinMain(folders, dtype, uploadBools)

def myomesinAssign(folders, dtype, uploadBools, edgeFolders, edgeBools, edgeMarker):
    if uploadBools == [True, True, True]:
        pass
    elif uploadBools == [True, False, False]:
        print('first we gotta make a binary')
        print('then we gotta analyze it')
    elif uploadBools == [True, True, False]:
        print('we just have to analyze the binary you made!')
    elif uploadBools == [False, True, False]:
        print('we just have to analyze the binary you made!')
        print('no image though so there wont be grey level data')
    elif uploadBools == [False, False, False]:
        print('u didnt upload any data')
    else:
        print('you already have data but are either missing the image, binary, or both')
        print('no worries!')

    myomesinMain(folders, dtype, uploadBools, edgeFolders, edgeBools, edgeMarker)

def titinAssign(folders, dtype, uploadBools, edgeFolders, edgeBools, edgeMarker):
    if uploadBools == [True, True, True]:
        pass
    elif uploadBools == [True, False, False]:
        print('first we gotta make a binary')
        print('then we gotta analyze it')
    elif uploadBools == [True, True, False]:
        print('we just have to analyze the binary you made!')
    elif uploadBools == [False, True, False]:
        print('we just have to analyze the binary you made!')
        print('no image though so there wont be grey level data')
    elif uploadBools == [False, False, False]:
        print('u didnt upload any data')
    else:
        print('you already have data but are either missing the image, binary, or both')
        print('no worries!')
    titinMain(folders, dtype, uploadBools, edgeFolders, edgeBools, edgeMarker)

def NMIIAssign(folders, dtype, uploadBools):
    pass
    #NMIIMain(folders, dtype, uploadBools)

def alphaBetaAssign(folders, dtype, uploadBools):
    pass

def dapiAssign(folders, dtype, uploadBools):
    if uploadBools == [True, True, True]:
        pass
    elif uploadBools == [True, False, False]:
        print('first we gotta make a binary')
        print('then we gotta analyze it')
    elif uploadBools == [True, True, False]:
        print('we just have to analyze the binary you made!')
    elif uploadBools == [False, True, False]:
        print('we just have to analyze the binary you made!')
        print('no image though so there wont be grey level data')
    elif uploadBools == [False, False, False]:
        print('u didnt upload any data')
    else:
        print('you already have data but are either missing the image, binary, or both')
        print('no worries!')
    dapiMain(folders, dtype, uploadBools)

def channelAssignments(channels, folders, numCh, edgeStain, edgeMarker):
    dtype = "Fixed 2D"
    edgeBools = None
    edgeFolders = None
    for i in range(numCh):
        key = '-C{}-'.format(i+1)
        if key == edgeStain:
            edgeFolders = folders[i]
            edgeBools = [bool(folders[i].get('-IMG-')), bool(folders[i].get('-BIN-')), bool(folders[i].get('-DATA-'))]

    for i in range(numCh):
        key = '-C{}-'.format(i+1)
        stain = channels[key]
        uploadBools = [bool(folders[i].get('-IMG-')), bool(folders[i].get('-BIN-')), bool(folders[i].get('-DATA-'))]
        if stain == 'actinin':
            actininAssign(folders[i],dtype,uploadBools)
        elif stain == 'actin':
            actinAssign(folders[i],dtype,uploadBools)
        elif stain == 'paxillin':
            paxillinAssign(folders[i],dtype,uploadBools)
        elif stain == 'myomesin':
            myomesinAssign(folders[i],dtype,uploadBools, edgeFolders, edgeBools, edgeMarker)
        elif stain == 'titin N':
            titinAssign(folders[i],dtype,uploadBools, edgeFolders, edgeBools, edgeMarker)
        elif stain == 'NMIIA/B':
            NMIIAssign(folders[i],dtype,uploadBools)
        elif stain == 'alpha/beta':
            alphaBetaAssign(folders[i],dtype,uploadBools, edgeFolders, edgeBools)
        elif stain == 'dapi':
            dapiAssign(folders[i],dtype,uploadBools)
