import PySimpleGUI as sg
from channelAssignments import channelAssignments

def makeMainWindow():
    sg.theme('Reddit')   # Color theme
    possibleChannels = ['none','actinin', 'actin', 'paxillin', 'myomesin', 'titin N', 'NMIIA/B', 'alpha/beta', 'dapi']
    # Setup window layout
    layout = [  [sg.Text('sarcApp')],
                [sg.Text('channel 1'), sg.Combo(values = possibleChannels, default_value='actinin',k='-C1-')],
                [sg.Text('channel 2'), sg.Combo(values = possibleChannels, default_value='none',k='-C2-')],
                [sg.Text('channel 3'), sg.Combo(values = possibleChannels, default_value='none',k='-C3-')],
                [sg.Text('channel 4'), sg.Combo(values = possibleChannels, default_value='none',k='-C4-')],
                [sg.Button('go'), sg.Button('clear')] 
            ]
    return sg.Window('sarcApp',layout)
    
def makeSubWindows(channelID, channelType):
    subLayout = [   [sg.Text('upload data for channel:'), sg.Text(channelID), sg.Text(channelType)],
                        [sg.FolderBrowse(button_text='Image Folder',enable_events = True, key='-IMG-')],
                        [sg.Text(text = '', k ='-IPATH-')],
                        [sg.FolderBrowse(button_text='Binary Folder',enable_events = True, key='-BIN-')],
                        [sg.Text(text = '', k ='-BPATH-')],
                        [sg.FolderBrowse(button_text = 'Data Folder',enable_events = True, key='-DATA-')],
                        [sg.Text(text = '', k ='-DPATH-')],
                        [sg.Button('go')]
                    ]
    return sg.Window('upload data',subLayout)

def main():
    window = makeMainWindow()
    channels = False
    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED: # if user closes window
            break
        if event == 'go':
            channels = values
            break
    window.close()
    numCh = 0
    folders = []
    if channels:
        if channels['-C1-'] != 'none':
            numCh += 1
            print('upload channel 1 data')
            window2 = makeSubWindows(1, channels['-C1-'])
            while True:
                event, values = window2.read()
                if event == sg.WIN_CLOSED:
                    break
                if event == 'go':
                    C1folders = values
                    folders.append(C1folders)
                    break
                if event == '-IMG-':
                    window2['-IPATH-'].update(values['-IMG-'])
                if event == '-BIN-':
                    window2['-BPATH-'].update(values['-BIN-'])
                if event == '-DATA-':
                    window2['-DPATH-'].update(values['-DATA-'])
    
        if channels['-C2-'] != 'none':
            numCh += 1
            print('upload channel 2 data')
            window3 = makeSubWindows(2, channels['-C2-'])
            while True:
                event, values = window3.read()
                if event == sg.WIN_CLOSED:
                    break
                if event == 'go':
                    C2folders = values
                    folders.append(C2folders)
                    break
                if event == '-IMG-':
                    window3['-IPATH-'].update(values['-IMG-'])
                if event == '-BIN-':
                    window3['-BPATH-'].update(values['-BIN-'])
                if event == '-DATA-':
                    window3['-DPATH-'].update(values['-DATA-'])
    
        if channels['-C3-'] != 'none':
            numCh += 1
            print('upload channel 3 data')
            window4 = makeSubWindows(3, channels['-C3-'])
            while True:
                event, values = window4.read()
                if event == sg.WIN_CLOSED:
                    break
                if event == 'go':
                    C3folders = values
                    folders.append(C3folders)
                    break
                if event == '-IMG-':
                    window4['-IPATH-'].update(values['-IMG-'])
                if event == '-BIN-':
                    window4['-BPATH-'].update(values['-BIN-'])
                if event == '-DATA-':
                    window4['-DPATH-'].update(values['-DATA-'])

        if channels['-C4-'] != 'none':
            numCh += 1
            print('upload channel 4 data')
            window5 = makeSubWindows(4, channels['-C4-'])
            while True:
                event, values = window5.read()
                if event == sg.WIN_CLOSED:
                    break
                if event == 'go':
                    C4folders = values
                    folders.append(C4folders)
                    break
                if event == '-IMG-':
                    window5['-IPATH-'].update(values['-IMG-'])
                if event == '-BIN-':
                    window5['-BPATH-'].update(values['-BIN-'])
                if event == '-DATA-':
                    window5['-DPATH-'].update(values['-DATA-'])
    else:
        print("you didn't pick anything: try again")
    
    #Abbie note 122021: there has to be a better way to do the below section
    #abbie note 123021: yes there is, i haven't done it yet but maybe append a list?
    # if numCh == 1:
    #     folders = [C1folders]
    # elif numCh == 2:
    #     folders = [C1folders, C2folders]
    # elif numCh == 3:
    #     folders = [C1folders, C2folders, C3folders]
    # elif numCh == 4:
    #     folders = [C1folders, C2folders, C3folders, C4folders]

    if numCh > 0:
        channelAssignments(channels, folders, numCh)      

if __name__ == '__main__':
    main()