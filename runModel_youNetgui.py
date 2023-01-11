import PySimpleGUI as sg
from runModel2factor import runModel2factor
from iconGrab import iconGrab

def makeWindow():
    icon = iconGrab()
    sg.theme('Reddit')
    subLayout = [   [sg.Text('yoU-Net: run pre-trained model')],
                        [sg.FolderBrowse(button_text='Image Folder',enable_events = True, key='-IMG-')],
                        [sg.Text(text = '', k ='-IMGPATH-')],
                        [sg.FolderBrowse(button_text='Output Folder',enable_events = True, key='-OUT-')],
                        [sg.Text(text = '', k ='-OUTPATH-')],
                        [sg.FileBrowse(button_text = 'Model Path',enable_events = True, key='-MODEL-')],
                        [sg.Text(text = '', k ='-MPATH-')],
                        [sg.Text(text='# feature maps'),sg.Combo(values=['16','32'], default_value='16',k='fmaps')],
                        [sg.Button('go')]
                    ]
    return sg.Window('yoU-Net',subLayout, icon=icon)

def main():
    window = makeWindow()
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED: # if user closes window
            break
        if event == 'go':
            keys_to_extract = {'-IMG-', '-OUT-', '-MODEL-'}
            folders = {key: values[key] for key in values.keys() & keys_to_extract}
            fmaps = int(values['fmaps'])
            print("running!")
            runModel2factor(folders, fmaps)
            break
        if event == '-IMG-':
            window['-IMGPATH-'].update(values['-IMG-'])
        if event == '-OUT-':
             window['-OUTPATH-'].update(values['-OUT-'])
        if event == '-MODEL-':
            window['-MPATH-'].update(values['-MODEL-'])
    window.close()

if __name__ == '__main__':
    main()