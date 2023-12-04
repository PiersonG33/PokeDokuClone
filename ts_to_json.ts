import * as fs from 'fs';
import { Pokedex } from './pokedex';

// Convert the Pokedex data to a JSON string
const jsonData = JSON.stringify(Pokedex, null, 2); // The third argument (2) specifies the number of spaces to use for indentation

// Specify the file path where you want to save the JSON data
const filePath = 'pokedex_exp.json';

// Write the JSON data to the file
fs.writeFileSync(filePath, jsonData, 'utf-8');

console.log('Pokedex data has been exported to ${filePath}');
