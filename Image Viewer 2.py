import PySimpleGUI as sg
import os.path

themes = sg.ListOfLookAndFeelValues()
selected_theme = 'SystemDefault1'
current_them = sg.LOOK_AND_FEEL_TABLE[selected_theme]
sg.ChangeLookAndFeel(selected_theme)

file_list_column = [
    [
        sg.Text("Image Folder"),
        sg.In(size=(25,1), enable_events=True, key="-FOLDER-"),
        sg.FolderBrowse(),
    ],
    [
            sg.Listbox(
                values=[], enable_events=True, size=(60,30),
                key="-FILE LIST-"
            )
    ],
]

image_viewer_column = [
    [sg.Text("Choose an image from the list on the left:")],
    [sg.Text(size=(40,1), key="-TOUT-")],
    [sg.Image(key="-IMAGE-")],
]

layout = [
    [
        sg.Column(file_list_column),
        sg.VSeparator(),
        sg.Column(image_viewer_column),
        [sg.Text('Select Background:'),
        sg.Combo(values=themes, default_value=selected_theme, size=(15, 1), enable_events=True, key='-SELECT-THEME-')],
    ]
]

window = sg.Window("Image Viewer", layout)

while True:
    event, values = window.read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        break
    if event == "-FOLDER-":
        folder = values["-FOLDER-"]
        try:
            file_list = os.listdir(folder)
        except:
            fle_list = []

        fnames = [
            f
            for f in file_list
            if os.path.isfile(os.path.join(folder, f))
            and f.lower().endswith((".png", ".gif"))
        ]
        window["-FILE LIST-"].update(fnames)
    if event is None:
        break
    elif event == '-SELECT-THEME-':
        selected_theme = values['-SELECT-THEME-']
        print(selected_theme)
        current_them = sg.LOOK_AND_FEEL_TABLE[selected_theme]
        try:
            window_bkg = current_them.get('BACKGROUND')
            window.TKroot.config(background=window_bkg)
        except Exception as event:
            print(event)

        for values, element in window.AllKeysDict.items():
            try:
                color = current_them.get(element.Type.upper())
                if color:
                    if element.Type == 'button':
                        element.Widget.config(foreground=color[0])
                    else:
                        element.Widget.config(background=color[0])
                    element.update()
            except Exception as event:
                print(event)

window.close()