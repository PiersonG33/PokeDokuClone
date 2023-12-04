from util import *

if __name__ == "__main__":
    # to_json("pokedex.ts", "pokedex.json")
    data = to_dict("pokedex.json")
    options = to_dict("options.json")
    ready = False
    while not ready:
        puzzle = generate_combos(options, abilities = False, eggGroups = False)
        rows = puzzle[:3]
        cols = puzzle[3:]
        ready = check_valid(rows, cols, data, options, cutoff = 1)
    write_answer(ready, "answer_key.txt")
    generate_grid(list(data.keys()), cols, rows, data, options)
    
    