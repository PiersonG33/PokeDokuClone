import json
import time
import random
# from gui import *
pokedex = dict()
options = dict()

def search_database(term1, term2, pokedict, stats):
    t1_key = stats[term1]
    t2_key = stats[term2]
    all_valid = []
    for key in pokedict:
        pokemon = pokedict[key]
        if term1 in pokemon.get(t1_key, []) and term2 in pokemon.get(t2_key, []):
            all_valid.append(key)
    return all_valid

def to_dict(json_name):
    #pokedex.json to dict:
    poke_data = json.load(open(json_name, encoding="utf-8"))
    return poke_data

def generate_combos(options, combo_dict, invalid = []):
    possibilities = []
    for key in options:
        option_type = options[key]
        if combo_dict.get(option_type, False):
            possibilities.append(key)

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
                if r.lower() in [x.lower() for x in pokemon.get(r_key, [])] and c.lower() in [x.lower() for x in pokemon.get(c_key, [])]:
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

def get_valid_labels(pokedict, stats, combo_dict, invalid = [], cutoff = 1):
    ready = False
    while not ready:
        puzzle = generate_combos(stats, combo_dict, invalid)
        rows = puzzle[:3]
        cols = puzzle[3:]
        ready = check_valid(rows, cols, pokedict, stats, cutoff = cutoff)
    write_answer(ready, "answer_key.txt")
    return rows, cols

def get_generation(name, num):
    gen = ""
    if (1 <= num <= 151):
        gen = "Kanto"
    elif (151 < num <= 251):
        gen = "Johto"
    elif (251 < num <= 386):
        gen = "Hoenn"
    elif (386 < num <= 493):
        gen = "Sinnoh"
    elif (493 < num <= 649):
        gen = "Unova"
    elif (649 < num <= 721):
        gen = "Kalos"
    elif (721 < num <= 809):
        gen = "Alola"
    elif (809 < num <= 905):
        gen = "Galar/Hisui"
    elif (905 < num):
        gen = "Paldea"
    if "Alola" in name:
        gen = "Alola"
    elif "Galar" in name or "Hisui" in name:
        gen = "Galar/Hisui"
    elif "Paldea" in name:
        gen = "Paldea"
    return gen

def json_formatting(dict1):
    # Designed to change the formatting of the auto-generated json file from the ts file
    # into something that works better for PokeDoku
    evo_format = {
        "levelFriendship": "Evolved by Friendship",
        "useItem": "Evolved by Item",
        "trade": "Evolved by Trade"
    }
    new_dict = dict()
    options = dict()
    for key in dict1:
        cName = dict1[key]["name"]

        # Fix unicode characters for Farfetch'd, Sirfetch'd, and Flabebe
        cName = cName.replace("’", "'").replace("é", "e")

        cTypes = dict1[key]["types"]
        cAbilities = list(dict1[key]["abilities"].values())
        cEggGroups = dict1[key]["eggGroups"]
        cTags = dict1[key].get("tags",[])
        cFormes = dict1[key].get("forme","")
        cFormes = [cFormes]
        if cFormes[0] == "":
            cFormes = []
        cNum = dict1[key]["num"]

        cEvoTypes = dict1[key].get("evoType", "")
        cEvoTypes = [evo_format.get(cEvoTypes, "")]
        if cEvoTypes[0] == "":
            cEvoTypes = []
        else:
            options[cEvoTypes[0]] = "evoTypes"

        new_dict[cName] = dict()

        new_dict[cName]["evoTypes"] = cEvoTypes

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

        # give alt forms the same tags of the previous form
        baseSpecies = dict1[key].get("baseSpecies", "").replace("’", "'")
        if baseSpecies:
            base_tags = new_dict[baseSpecies].get("tags", [])
            new_dict[cName]["tags"] = base_tags
            # print(f"{cName} has the same tags as {baseSpecies}")

        moreTags = []
        if len(cTypes) == 1:
            moreTags.append("Mono-Type")
            options["Mono-Type"] = "moreTags"
            new_dict[cName]["moreTags"] = moreTags

    return new_dict, options