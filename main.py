from util import *
from gui import *

if __name__ == "__main__":
    # to_json("pokedex.ts", "pokedex.json")
    data = to_dict("pokedex.json")
    options = to_dict("options.json")
    generate_grid(list(data.keys()), data, options)
    
    