import PySimpleGUI as sg
from implement2factor import implement2factor

def makeWindow():
    sg.theme('Reddit')
    subLayout = [   [sg.Text('yoU-Net')],
                        [sg.FolderBrowse(button_text='Training Image Folder',enable_events = True, key='-TIMG-')],
                        [sg.Text(text = '', k ='-TIPATH-')],
                        [sg.FolderBrowse(button_text='Training Binary (Ground Truth) Folder',enable_events = True, key='-TGT-')],
                        [sg.Text(text = '', k ='-TGTPATH-')],
                        [sg.FolderBrowse(button_text = 'Validation Image Folder',enable_events = True, key='-VIMG-')],
                        [sg.Text(text = '', k ='-VIPATH-')],
                        [sg.FolderBrowse(button_text = 'Validation Binary (Ground Truth) Folder',enable_events = True, key='-VGT-')],
                        [sg.Text(text = '', k ='-VGTPATH-')],
                        [sg.FolderBrowse(button_text = 'Output Folder for Validation Predictions',enable_events = True, key='-OUT-')],
                        [sg.Text(text = '', k ='-OUTPATH-')],
                        [sg.Text(text='# feature maps'),sg.Combo(values=['16','32'], default_value='16',k='fmaps')],
                        [sg.Text(text='# Epochs'),sg.Input(default_text='100',k='epochs')],
                        [sg.Button('go')]
                    ]
    return sg.Window('yoU-Net',subLayout)

def main():
    window = makeWindow()
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED: # if user closes window
            break
        if event == 'go':
            keys_to_extract = {'-TIMG-', '-TGT-', '-VIMG-', '-VGT-','-OUT-'}
            folders = {key: values[key] for key in values.keys() & keys_to_extract}
            fmaps = int(values['fmaps'])
            epochs = int(values['epochs'])
            print("implementing!")
            implement2factor(folders,fmaps,epochs)
            break
        if event == '-TIMG-':
            window['-TIPATH-'].update(values['-TIMG-'])
        if event == '-TGT-':
             window['-TGTPATH-'].update(values['-TGT-'])
        if event == '-VIMG-':
            window['-VIPATH-'].update(values['-VIMG-'])
        if event == '-VGT-':
            window['-VGTPATH-'].update(values['-VGT-'])
        if event == '-OUT-':
            window['-OUTPATH-'].update(values['-OUT-'])
    window.close()

if __name__ == '__main__':
    main()