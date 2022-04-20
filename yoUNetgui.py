#youuuuuu
#soulja boy tell em
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
            folders = values
            implement2factor(folders)
        if event == '-TIMG-':
            window['-TIPATH-'].update(values['-TIMG-'])
        if event == '-TGT-':
             window['-TGTPATH-'].update(values['-TGT-'])
        if event == '-VIMG-':
            window['-VIPATH-'].update(values['-VIMG-'])
        if event == '-VGT-':
            window['-VGTPATH-'].update(values['-VGT-'])
    window.close()

if __name__ == '__main__':
    main()