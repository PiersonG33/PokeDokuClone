# PokeDokuClone
A clone of [PokeDoku](https://pokedoku.com/) where users try to fill in a 3x3 grid of Pokemon. Made in Python using PySimpleGUI.

Pokemon data sources from [Pokemon Showdown's](https://github.com/smogon/pokemon-showdown/blob/master/data/pokedex.ts) GitHub repository. The data is processed into a `JSON` file via `ts_to_json.ts`, and then refined further in `util.py` and the comments of `main.py`. Users do not need to know this, since the `pokedex.json` and `options.json` file are included. However, this is good to know for future generations of Pokemon.