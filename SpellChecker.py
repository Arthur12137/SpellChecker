import datetime
import os
import json
from difflib import SequenceMatcher,get_close_matches

class SpellChecker:
    def __init__(self, dict_file="EnglishWords.txt", definition_file="data.json"):
        """
        Initializes the SpellChecker with a dictionary and a definition database.

        Parameters:
            dict_file (str): Path to the file containing a list of valid words.
            definition_file (str): Path to the JSON file containing word definitions.
        """
        self.dictionary = self.load_dictionary(dict_file)
        self.definitions = self.load_definitions(definition_file)

    def load_dictionary(self, file_name):
        """
        Load the dictionary from the specified file.

        Parameters:
            file_name (str): Path to the file containing a list of valid words.

        Returns:
            set: A set containing valid words.
        """
        with open(file_name, 'r') as file:
            return set(line.strip().lower() for line in file)

    def load_definitions(self, file_name):
        """
        Load word definitions from the specified JSON file.

        Parameters:
            file_name (str): Path to the JSON file containing word definitions.

        Returns:
            dict: A dictionary containing word definitions.
        """
        with open(file_name, 'r') as file:
            return json.load(file)

    def check_sentence(self, sentence):
        """
        Check the spelling of each word in a sentence.

        Parameters:
            sentence (str): The sentence to be checked.

        Returns:
            dict: Dictionary containing correct and incorrect words.
        """
        words = [word.lower() for word in sentence.split()]
        results = {
            "correct": [],
            "incorrect": []
        }
        for word in words:
            clean_word = ''.join(filter(str.isalpha, word))
            if clean_word in self.dictionary:
                results["correct"].append(clean_word)
            elif clean_word:
                results["incorrect"].append(clean_word)
        return results

    def check_file(self, file_name):
        """
        Check the spelling of each word in a file.

        Parameters:
            file_name (str): Path to the file to be checked.

        Returns:
            dict: Dictionary containing correct and incorrect words.
        """
        with open(file_name, 'r') as file:
            text = file.read()
        return self.check_sentence(text)

    def suggest_correction(self, word):
        """
        Suggest a correction for an incorrectly spelled word.

        Parameters:
            word (str): The word for which a correction is to be suggested.

        Returns:
            str: The suggested correct spelling.
        """
        score = 0
        suggestion = None
        for dict_word in self.dictionary:
            current_score = SequenceMatcher(None, word, dict_word).ratio()
            if current_score > score:
                score = current_score
                suggestion = dict_word
        return suggestion

    def add_to_dictionary(self, word):
        """
        Add a word to the dictionary.

        Parameters:
            word (str): The word to be added.
        """
        self.dictionary.add(word.lower())
        with open("EnglishWords.txt", 'a') as file:
            file.write('\n' + word.lower())

    def print_report(self, results, elapsed_time):
        print("Number of words:", len(results["correct"]) + len(results["incorrect"]))
        print("Number of correctly spelt words:", len(results["correct"]))
        print("Number of incorrectly spelt words:", len(results["incorrect"]))
        print(f"Time elapsed: {elapsed_time.microseconds} microseconds")

    def check_word_meaning(self, word):
        """
        Retrieve the meaning of a word from the definitions database.

        Parameters:
            word (str): The word whose meaning is to be retrieved.

        Returns:
            str: The meaning of the word or a message if the word is not found.
        """
        word = word.lower()
        if word in self.definitions:
            return self.definitions[word]
        elif len(get_close_matches(word, self.definitions.keys()))> 0:
            yn = input("Did you mean %s instead? Enter Y if yes, or N if no: " % get_close_matches(word, self.definitions.keys())[0])
            if yn == "Y":
                return self.definitions[get_close_matches(word,self.definitions.keys())[0]]
            elif yn =="N":
                return "The word doesn't exist. Please double check it"
            else:
                return "I didn't understand your entry. Please do it again"
        else:
            return f"The word '{word}' doesn't exist in the definitions. Please double check it."

    def spell_check_interface(self):
        """
        Provide an interface for the user to interact with the spell checker.
        """
        start_time = datetime.datetime.now()
        choice = input("Choose an option: \n1. Check a file\n2. Check a sentence\n3. Check word meaning\n0. Quit\nChoice: ")

        if choice == "1":
            file_name = input("Enter the file name to spellcheck: ")
            while not os.path.isfile(file_name):
                file_name = input("Enter a valid file name to spellcheck: ")
            results = self.check_file(file_name)
            for word in results["incorrect"]:
                suggestion = self.suggest_correction(word)
                print(f"Word '{word}' not found in dictionary. Did you mean '{suggestion}'?")
            self.print_report(results, datetime.datetime.now() - start_time)

        elif choice == "2":
            sentence = input("Enter a sentence to spellcheck: ")
            results = self.check_sentence(sentence)
            for word in results["incorrect"]:
                suggestion = self.suggest_correction(word)
                print(f"Word '{word}' not found in dictionary. Did you mean '{suggestion}'?")
            self.print_report(results, datetime.datetime.now() - start_time)

        elif choice == "3":
            word = input("Enter a word to check its meaning: ")
            print(self.check_word_meaning(word))

        elif choice == "0":
            return
        else:
            print("Invalid choice. Exiting...")
            return

if __name__ == "__main__":
    checker = SpellChecker()
    checker.spell_check_interface()
