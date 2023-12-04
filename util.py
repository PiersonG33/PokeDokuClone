import json
import time
import random
from gui import *
pokedex = dict()
options = dict()

def to_json(ts, json_name):
    with open(ts, "r") as f:
        past = 0
        current = 0
        cName = ""
        cTypes = []
        cAbilities = []
        cTags = []
        cEggGroups = []
        cFormes = []
        first_pokemon = ["Chikorita", "Treecko", "Turtwig", "Victini", "Chespin", "Rowlet", "Grookey", "Sprigatito"]
        generation = 1
        for line in f:
            line = line.strip()
            if line.startswith("name: "):
                cName = (line[7:])
                cName = cName.replace('"', "").replace(",", "")
                cTags = []
                cFormes = []
                if cName in first_pokemon:
                    generation += 1
                #print(cName)
            if line.startswith("forme: "):
                cForme = (line[8:])
                cForme = cForme.replace('"', "").replace(",", "").strip()
                cFormes.append(cForme)
            if line.startswith("types: "):
                cTypes = (line[8:])
                cTypes = cTypes.replace('"', "").replace(",", "").replace("[", "").replace("]", "").split()
                #print(cTypes)
            if line.startswith("abilities: "):
                cAbilities = (line[12:])
                cAbilities = cAbilities.replace('"', "").replace("{", "").replace("}", "").split(",")
                cAbilities = [x.strip() for x in cAbilities if x.strip()]
                cAbilities = [x[3:] for x in cAbilities]
                #print(cAbilities)
            if line.startswith("tags: "):
                cTags = (line[7:])
                cTags = cTags.replace('"', "").replace("[", "").replace("]", "").split(",")
                cTags = [x.strip() for x in cTags if x.strip()]
                #print(cTags)
            if line.startswith("eggGroups: "):
                cEggGroups = (line[11:])
                cEggGroups = cEggGroups.replace('"', "").replace("[", "").replace("]", "").split(",")
                cEggGroups = [x.strip() for x in cEggGroups if x.strip()]
                current += 1
                #print(cEggGroups)
            if current != past:
                subDict = dict()
                subDict["types"] = cTypes
                for t in cTypes:
                    options[t] = "types"
                subDict["abilities"] = cAbilities
                for a in cAbilities:
                    options[a] = "abilities"
                if len(cTags) != 0:
                    if cTags[0] == "Mythical":
                        cTags = ["Mythical", "Legendary"] #Mythical pokemon are also legendary
                    elif cTags[0] != "Paradox":
                        cTags = ["Legendary"] #Groups sub and restricted legendary pokemon together
                subDict["tags"] = cTags
                for t in cTags:
                    options[t] = "tags"
                subDict["eggGroups"] = cEggGroups
                for e in cEggGroups:
                    options[e] = "egg groups"
                subDict["generation"] = ["Generation " + str(generation)]
                options["Generation " + str(generation)] = "generation"
                subDict["formes"] = cFormes
                for f in cFormes:
                    options[f] = "formes"
                if len(cFormes) > 0:
                    the_form = cFormes[0]
                    if the_form.startswith("Alola"):
                        subDict["generation"] = ["Generation 7"]
                    elif the_form.startswith("Galar"):
                        subDict["generation"] = ["Generation 8"]
                    elif the_form.startswith("Hisui"):
                        subDict["generation"] = ["Generation 9"]
                pokedex[cName] = subDict
                past = current
                # cTypes.clear()
                # cAbilities.clear()
                # cTags.clear()
                # cEggGroups.clear()
    #print(pokedex, file=open("pokedex.txt", "w"))
    print(json.dumps(pokedex, indent=4), file=open(json_name, "w"))
    #options.pop("")
    print(json.dumps(options, indent=4), file=open("options.json", "w"))

def to_dict(json_name):
    #pokedex.json to dict:
    poke_data = json.load(open(json_name))
    return poke_data


def generate_combos(options, types = True, abilities = True, tags = True, eggGroups = True, generation = True):
    possibilities = []
    for key in options:
        #print(key, options[key])
        if options[key] == "types" and types:
            possibilities.append(key)
        elif options[key] == "abilities" and abilities:
            possibilities.append(key)
        elif options[key] == "tags" and tags:
            possibilities.append(key)
        elif options[key] == "egg groups" and eggGroups:
            possibilities.append(key)
        elif options[key] == "generation" and generation:
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
                r_key = options[r].lower()
                c_key = options[c].lower()
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