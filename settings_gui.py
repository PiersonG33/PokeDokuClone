# This file will be used to generate the GUI for the settings menu.
# Users can decide what should be included as options for the puzzle
# E.g. no Legendaries, no Gen 8, etc
import PySimpleGUI as sg

def settings_gui():
    layout = []

    # Add dropdown menu for selecting cutoff value
    cutoff_options = [i for i in range(1, 5)]
    layout.append([sg.Text("Minimum Pokemon per option:"), sg.Combo(cutoff_options, default_value=2, key="-CUTOFF-")])

    # Add checkbox to say if mythicals count as legendaries
    layout.append([sg.Text("Mythicals count as Legendaries:"), sg.Checkbox("", default=True, key="-MYTHICAL-")])

    # Add checkboxes to include or exclude generations
    layout.append([sg.Text("Generations to include:"), 
                   sg.Checkbox("Gen 1", default=True, key="-GEN1-"), 
                   sg.Checkbox("Gen 2", default=True, key="-GEN2-"), 
                   sg.Checkbox("Gen 3", default=True, key="-GEN3-"), 
                   sg.Checkbox("Gen 4", default=True, key="-GEN4-"), 
                   sg.Checkbox("Gen 5", default=True, key="-GEN5-"), 
                   sg.Checkbox("Gen 6", default=True, key="-GEN6-"), 
                   sg.Checkbox("Gen 7", default=True, key="-GEN7-"), 
                   sg.Checkbox("Gen 8", default=True, key="-GEN8-"),
                   sg.Checkbox("Gen 9", default=True, key="-GEN9-")])

    # Add checkbox to include or exclude tags
    layout.append([sg.Text("Tags as a category (Legendary, Mythical):"), sg.Checkbox("", default=True, key="-TAGS-")])

    # Add text input for categories to not include
    layout.append([sg.Text("Categories to exclude (split by comma):"), sg.InputText(key="-EXCLUDE-")])

    # Add begin game button
    layout.append([sg.Button("Begin Game", key="-BEGIN-")])

    window = sg.Window("PokeDoku Settings", layout, finalize=True)

    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED:
            break

        elif event == "-CUTOFF-":
            cutoff = int(values["-CUTOFF-"])
            print(cutoff)

        elif event == "-MYTHICAL-":
            mythical = values["-MYTHICAL-"]

        elif event == "-EXCLUDE-":
            exclude = values["-EXCLUDE-"]

        elif event == "-BEGIN-":
            window.close()
            