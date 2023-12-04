from util import *
from gui import *

if __name__ == "__main__":
    # data = to_dict("pokedex_exp.json") # json exported from pokedex.ts conversion
    # data, options = json_formatting(data)
    # print(json.dumps(data, indent=4), file=open("pokedex.json", "w"))
    # print(json.dumps(options, indent=4), file=open("options.json", "w"))
    data = to_dict("pokedex.json")
    options = to_dict("options.json")
    generate_grid(list(data.keys()), data, options, cutoff = 2)
    
    
    