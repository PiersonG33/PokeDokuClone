# This file will be used to generate the GUI for the settings menu.
# Users can decide what should be included as options for the puzzle
# E.g. no Legendaries, no Gen 8, etc
import PySimpleGUI as sg
from gui import generate_grid

def settings_gui(poke_data, options):
    layout = []

    # Add dropdown menu for selecting cutoff value
    cutoff_options = [i for i in range(1, 5)]
    layout.append([sg.Text("Minimum Pokemon per option:"), sg.Combo(cutoff_options, default_value=2, key="-CUTOFF-")])

    # Add checkbox to say if mythicals count as legendaries
    layout.append([sg.Text("Mythicals count as Legendaries:"), sg.Checkbox("", default=True, key="-MYTHICAL-")])

    # Add checkboxes to include or exclude generations
    layout.append([sg.Text("Regions to include:"), 
                   sg.Checkbox("Kanto", default=True, key="-Kanto-"), 
                   sg.Checkbox("Johto", default=True, key="-Johto-"), 
                   sg.Checkbox("Hoenn", default=True, key="-Hoenn-"), 
                   sg.Checkbox("Sinnoh", default=True, key="-Sinnoh-"), 
                   sg.Checkbox("Unova", default=True, key="-Unova-"), 
                   sg.Checkbox("Kalos", default=True, key="-Kalos-"), 
                   sg.Checkbox("Alola", default=True, key="-Alola-"), 
                   sg.Checkbox("Galar/Hisui", default=True, key="-Galar/Hisui-"),
                   sg.Checkbox("Paldea", default=True, key="-Paldea-")])
    
    # Add checkbox to include or exclude regions as a category
    layout.append([sg.Text("Regions as a category (Kanto, Johto):"), sg.Checkbox("", default=True, key="-REGIONS-")])

    # Add checkbox to include or exclude tags
    layout.append([sg.Text("Tags as a category (Legendary, Mythical):"), sg.Checkbox("", default=True, key="-TAGS-")])

    # Add checkbox to include or exclude egg groups
    layout.append([sg.Text("Egg Groups as a category (Monster, Human-Like):"), sg.Checkbox("", default=False, key="-EGG GROUPS-")])

    # Add text input for categories to not include
    layout.append([sg.Text("Specific labels to exclude (split by comma):"), sg.InputText(key="-EXCLUDE-")])

    # Add begin game button
    layout.append([sg.Button("Begin Game", key="-BEGIN-")])

    window = sg.Window("PokeDoku Settings", layout, finalize=True)

    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED:
            break

        elif event == "-BEGIN-":
            combo_dict = { # Default combo_dict
                "types": True,
                "abilities": False,
                "tags": True,
                "eggGroups": False,
                "generation": True,
                "moreTags": True,
                "evoTypes": True
            }
            valid_regions = [key for key in options if (options[key] == "generation" and values.get(f"-{key}-", False))]
            invalid_pokemon = [pokemon for pokemon in poke_data if not any([region in poke_data[pokemon].get("generation", []) for region in valid_regions])]
            for pokemon in invalid_pokemon:
                poke_data.pop(pokemon)
            
            cutoff = int(values["-CUTOFF-"])
            myth_leg = values["-MYTHICAL-"]
            if values["-TAGS-"]:
                if not myth_leg:
                    for pokemon in poke_data:
                        cTags = poke_data[pokemon].get("tags", [])
                        if "Mythical" in cTags and "Legendary" in cTags:
                            poke_data[pokemon]["tags"].remove("Legendary")
            else:
                combo_dict["tags"] = False

            combo_dict["generation"] = values["-REGIONS-"]
            
            combo_dict["eggGroups"] = values["-EGG GROUPS-"]

            # Users can decide on specific labels to exclude, like no Fire, or no Evolved By Trade
            # Though they do have to know the exact label
            exclude = [x.strip() for x in values["-EXCLUDE-"].split(",")]
            for label in exclude:
                if label in options:
                    options.pop(label)
            

            window.close()
            generate_grid(list(poke_data.keys()), poke_data, options, combo_dict, cutoff = cutoff)
            