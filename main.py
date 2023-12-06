from util import *
from gui import *
from settings_gui import *

def update_files():
    data = to_dict("pokedex_exp.json") # json exported from pokedex.ts conversion
    data, options = json_formatting(data)
    print(json.dumps(data, indent=4), file=open("pokedex.json", "w"))
    print(json.dumps(options, indent=4), file=open("options.json", "w"))

if __name__ == "__main__":
    # update_files()
    data = to_dict("pokedex.json")
    options = to_dict("options.json")
    # settings_gui()
    generate_grid(list(data.keys()), data, options, invalid = [], cutoff = 2)
    
    
    