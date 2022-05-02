import nltk
from nltk.corpus import words
import pandas as pd
import itertools
import numpy as np
import json
import pickle


def keep_n_letter_words(starting_words, no_of_letters):
    """
    Passes a list of words and outputs a list containing a specified number of letters

    :param starting_words: (list): list of words
    :param no_of_letters: (int): integer to specify the legnth of words to keep
    :return: all_words (list): list of words of the required length
    """
    all_words = set()
    for word in starting_words:
        if len(word) == no_of_letters:
            all_words.add(word)
    return all_words


def remove_words_with_capitals(list_of_words: object):
    """
    Takes a list of words and removes any words containing capital letters

    :type list_of_words: object
    """
    assert isinstance(list_of_words, set)
    output_list = list(list_of_words).copy()
    words_to_remove = set()
    for word in output_list:
        if word[0] == word[0].upper():
            words_to_remove.add(word)
    for new_word in words_to_remove:
        output_list.remove(new_word)
    return output_list
