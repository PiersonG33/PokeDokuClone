import json
import time
import random
# from gui import *
pokedex = dict()
options = dict()

def to_dict(json_name):
    #pokedex.json to dict:
    poke_data = json.load(open(json_name, encoding="utf8"))
    return poke_data

def generate_combos(options, types = True, abilities = True, tags = True, eggGroups = True, generation = True, 
                    invalid = []):
    possibilities = []
    for key in options:
        #print(key, options[key])
        if options[key] == "types" and types:
            possibilities.append(key)
        elif options[key] == "abilities" and abilities:
            possibilities.append(key)
        elif options[key] == "tags" and tags:
            possibilities.append(key)
        elif options[key] == "eggGroups" and eggGroups:
            possibilities.append(key)
        elif options[key] == "generation" and generation:
            possibilities.append(key)
        if (key in invalid) and (key in possibilities):
            possibilities.remove(key)

    puzzle = random.sample(possibilities, 6)
    return puzzle
    
def check_valid(row, col, dex, options, cutoff = 1):
    #print(dex)
    answer_key = []
    for r in row:
        for c in col:
            is_good = False
            count = 0
            for p in dex:
                pokemon = dex[p]
                r_key = options[r]#.lower()
                c_key = options[c]#.lower()
                # print(r_key, c_key)
                # print(pokemon)
                if r.lower() in [x.lower() for x in pokemon[r_key]] and c.lower() in [x.lower() for x in pokemon[c_key]]:
                    count += 1
                    # print(f"{p} is {r} and {c}")
                if count >= cutoff:
                    is_good = True
                    answer_key.append(p)
                    break
            if not is_good:
                # print("There is no {0} {1} pokemon!".format(r, c))
                return False
    return answer_key

def write_answer(answer_key, f_name = "answer_key.txt"):
    answer_grid = ""
    max_len = max([len(x) for x in answer_key])
    for row in range(3):
        for col in range(3):
            answer_grid += answer_key[row * 3 + col].ljust(max_len + 3)
        answer_grid += "\n"
    print(answer_grid, file=open(f_name, "w"))

def get_valid_labels(pokedict, stats, types = True, abilities = True, 
                     tags = True, eggGroups = True, generation = True, invalid = [], cutoff = 1):
    ready = False
    while not ready:
        puzzle = generate_combos(stats, types, abilities, tags, eggGroups, generation, invalid)
        rows = puzzle[:3]
        cols = puzzle[3:]
        ready = check_valid(rows, cols, pokedict, stats, cutoff = cutoff)
    write_answer(ready, "answer_key.txt")
    return rows, cols

def get_generation(name, num):
    gen = ""
    if (1 <= num <= 152):
        gen = "Generation 1"
    elif (152 < num <= 251):
        gen = "Generation 2"
    elif (251 < num <= 386):
        gen = "Generation 3"
    elif (386 < num <= 493):
        gen = "Generation 4"
    elif (493 < num <= 649):
        gen = "Generation 5"
    elif (649 < num <= 721):
        gen = "Generation 6"
    elif (721 < num <= 809):
        gen = "Generation 7"
    elif (809 < num <= 905):
        gen = "Generation 8"
    elif (905 < num):
        gen = "Generation 9"
    if "Alola" in name:
        gen = "Generation 7"
    elif "Galar" in name or "Hisui" in name:
        gen = "Generation 8"
    elif "Paldea" in name:
        gen = "Generation 9"
    return gen

def json_formatting(dict1):
    # Designed to change the formatting of the auto-generated json file from the ts file
    # into something that works better for PokeDoku
    new_dict = dict()
    options = dict()
    for key in dict1:
        cName = dict1[key]["name"]
        cTypes = dict1[key]["types"]
        cAbilities = list(dict1[key]["abilities"].values())
        cEggGroups = dict1[key]["eggGroups"]
        cTags = dict1[key].get("tags",[])
        cFormes = dict1[key].get("forme","")
        cFormes = [cFormes]
        if cFormes[0] == "":
            cFormes = []
        cNum = dict1[key]["num"]
        new_dict[cName] = dict()

        new_dict[cName]["types"] = cTypes
        for t in cTypes:
            options[t] = "types"

        new_dict[cName]["abilities"] = cAbilities
        for a in cAbilities:
            options[a] = "abilities"

        new_dict[cName]["eggGroups"] = cEggGroups
        for e in range(len(cEggGroups)):
            cEggGroups[e] = cEggGroups[e] + " (Egg Group)"
            options[cEggGroups[e]] = "eggGroups"

        for t in range(len(cTags)):
            # Are Mythical pokemon also legendary?
            the_tag = cTags[t]
            if "legendary" in the_tag.lower():
                cTags =["Legendary"]
                options["Legendary"] = "tags"
                break
            if "mythical" in the_tag.lower():
                cTags = ["Mythical", "Legendary"]
                options["Mythical"] = "tags"
                options["Legendary"] = "tags"
                break
        new_dict[cName]["tags"] = cTags

        new_dict[cName]["formes"] = cFormes
        for f in cFormes:
            options[f] = "formes"
        new_dict[cName]["num"] = cNum

        new_dict[cName]["generation"] = [get_generation(cName, cNum)]
        options[get_generation(cName, cNum)] = "generation"

    return new_dict, options