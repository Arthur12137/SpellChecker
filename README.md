# SpellChecker

`SpellChecker` is a comprehensive tool that allows users to check the spelling of words in a sentence or file, and even retrieve word definitions. It utilizes a combination of a word dictionary and a word definition database to provide corrections and definitions, respectively.

## Features

- **Spell Check**: Validates words in a given sentence or file against a predefined dictionary. 
- **Word Suggestion**: Suggests the correct spelling for misspelled words using a sequence matching algorithm.
- **Word Definition**: Retrieves the definition of a given word from a JSON-based database.

## Getting Started

### Prerequisites

- Python 3.x
- `data.json` containing word definitions.

### Usage

1. Clone the repository or download the `SpellChecker.py` file.
2. Make sure you have `EnglishWords.txt` (or your custom dictionary file) and `data.json` in the same directory.
3. Run the program:
   
   ```bash
   python SpellChecker.py
