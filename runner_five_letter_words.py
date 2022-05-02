from wordle_solver import create_starting_list as csl
from nltk.corpus import words
import pandas as pd
import json


word_list = words.words()


if __name__ == "__main__":
    five_letter_words = csl.keep_n_letter_words(word_list, 5)
    print("number of fiver letter words ", len(five_letter_words))
    five_letter_words_no_caps = csl.remove_words_with_capitals(five_letter_words)
    print(len(five_letter_words_no_caps))
    jsonString = json.dumps(five_letter_words_no_caps)
    jsonFile = open("word_lists/five_letter_words_no_caps.json", "w")
    jsonFile.write(jsonString)
    jsonFile.close()