import PySimpleGUI as sg

# Function to create a dropdown element
def create_dropdown(key, pokemon):
    return sg.DropDown(values=pokemon, key=key)

def is_valid(sub_dict, stats, row_label, col_label):
    row_type = stats[row_label]
    col_type = stats[col_label]
    if (row_label in sub_dict.get(row_type, [])) and (col_label in sub_dict.get(col_type, [])):
        return True
    return False

def generate_grid(pokemon, col_labels, row_labels, pokedict, stats):

    options = pokemon

    layout = []
    for row in range(4):
        row_layout = []
        if row == 0:
            row_layout.append(sg.Text("", size=(10, 1)))
            for col in range(3):
                row_layout.append(sg.Text(col_labels[col], size=(35, 2)))
        else:
            row_layout.append(sg.Text(row_labels[row-1], size=(10, 2)))
            for col in range(3):
                row_layout.append(sg.Column([
                    [sg.Text("")],
                    [sg.InputText(key=f"-INPUT-{(row-1) * 3 + col + 1}-", 
                                  enable_events=True, size=(10, 1)), 
                                  sg.Listbox(values=options, size=(20, 4), 
                                             key=f"-LIST-{(row-1) * 3 + col + 1}-", enable_events=True)],
                    [sg.Button("Okey Doku", key=f"-BUTTON-{(row-1) * 3 + col + 1}-")]
                ]))
        layout.append(row_layout)

    # Create the window
    window = sg.Window("PokeDoku", layout, finalize=True)

    # Event loop
    while True:
        event, values = window.read()

        # Handle events
        if event == sg.WINDOW_CLOSED:
            break

        for row in range(3):
            for col in range(3):
                if event == f"-INPUT-{row * 3 + col + 1}-":
                    search_term = values[f"-INPUT-{row * 3 + col + 1}-"].strip().lower()
                    filtered_options = [option for option in options if search_term in option.lower()]
                    window[f"-LIST-{row * 3 + col + 1}-"].update(values=filtered_options)

                elif event == f"-LIST-{row * 3 + col + 1}-":
                    selected_option = values[f"-LIST-{row * 3 + col + 1}-"][0]
                    window[f"-INPUT-{row * 3 + col + 1}-"].update(value=selected_option)

                elif event == f"-BUTTON-{row * 3 + col + 1}-":
                    input_value = values[f"-INPUT-{row * 3 + col + 1}-"]
                    print(f"Button Pressed: Okey Doku, Input Value: [{input_value}]")
                    
                    # The dictionary of the selected pokemon
                    poke_data = pokedict.get(input_value, dict())

                    # The labels of the selected row and column
                    c_row_label = row_labels[row]
                    c_col_label = col_labels[col]
                    
                    #If the pokemon fits the criteria, then it is valid
                    validity = is_valid(poke_data, stats, c_row_label, c_col_label)
                    if validity:
                        #Change button color to green
                        window[f"-BUTTON-{row * 3 + col + 1}-"].update(button_color=('white', 'green'))
                    else:
                        #Change button color to red
                        window[f"-BUTTON-{row * 3 + col + 1}-"].update(button_color=('white', 'red'))

    # Close the window
    window.close()
