import pandas as pd
import itertools
import numpy as np
from collections import Counter


def all_colour_combinations():
    """
    Function to return all potential combinations of Black, Yellow and Green for a 5 letter guess
    :return: list of lists ie. [["Y","Y","Y","Y","Y"],["Y","Y","Y","Y","B"]]
    """
    colours = ["B", "Y", "G"]
    combos = list(itertools.product(colours, repeat=5))
    return combos


def return_wordle_colours_list(entered_word, word_to_guess):
    """
    Function to return the colours or hint after a word has been guessed. Requires the function to know
    what the secret word is.
    Green, Yellow and Black hints are returned as "G", "Y" and "B"
    Note that this function does not take into account the way Wordle handles duplicate letters. This will be dealt
    with in another function

    :param entered_word:
    :param word_to_guess:
    :return: a list of letters denoting Green, Yellow or Black eg ["G","G","G","G","G"] for a correct guess
    """
    returned_colours = list()
    for i in range(len(entered_word)):
        letter = entered_word[i]
        if letter == word_to_guess[i]:
            colour = "G"
        elif letter in word_to_guess:
            colour = "Y"
        else:
            colour = "B"
        returned_colours.append(colour)
    return returned_colours


def return_wordle_colours_str(entered_word, word_to_guess):
    """
    Function to return the colours or hint after a word has been guessed. Requires the function to know
    what the secret word is.
    Green, Yellow and Black hints are returned as "G", "Y" and "B"
    Note that this function does not take into account the way Wordle handles duplicate letters. This will be dealt
    with in another function

    :param entered_word:
    :param word_to_guess:
    :return: a list of letters denoting Green, Yellow or Black eg ["G","G","G","G","G"] for a correct guess
    """
    returned_colours = str()
    for i in range(len(entered_word)):
        letter = entered_word[i]
        if letter == word_to_guess[i]:
            colour = "G"
        elif letter in word_to_guess:
            colour = "Y"
        else:
            colour = "B"
        returned_colours = returned_colours + colour
    return returned_colours

# def return_wordle_colours_speed(entered_word, word_to_guess):


def identify_duplicate_letters(entered_word):
    """
    Function to identify if duplicate letters exist in the guess and returns a dictionairy noting their frequency

    :param entered_word:
    :return:
    """
    unique_letters = set(list(entered_word))
    # multiple_letters_dict = dict()
    entered_word_as_list = list(entered_word)
    duplicate_letters_list = [i for i in unique_letters if entered_word_as_list.count(i) > 1]
    # for i in unique_letters:
    #     word_freq = entered_word_as_list.count(i)
    #     if word_freq > 1:
    #         multiple_letters_dict[i] = word_freq
    return duplicate_letters_list


def get_position_of_multiple_letters(entered_word, multiple_letters_list):
    """
    Function to identify the position of duplicate letters in a word
    :param entered_word: Word that has been entered as a guess
    :param multiple_letters_list: Dictionary that contains the letters that are duplicate
    :return: a dictionary that contains duplicate letters and the positions in the guessed word where they appear
    """
    multiple_letters_position_dict = dict()
    if len(multiple_letters_list) > 0:
        # multiple_letters_position_dict = {l: [pos for pos, char in enumerate(entered_word) if char == l]
        #                                   for l in multiple_letters_list}
        for key in multiple_letters_list:
            pos_list = list()
            for pos in range(len(entered_word)):
                if entered_word[pos] == key:
                    pos_list.append(pos)
            multiple_letters_position_dict[key] = pos_list
    return multiple_letters_position_dict


def get_position_of_multiple_letters_opt(entered_word, multiple_letters_list):
    if len(multiple_letters_list) < 1:
        multiple_letters_position_dict = dict()
        return multiple_letters_position_dict
    else:
        multiple_letters_position_dict = {l: [pos for pos, char in enumerate(entered_word) if char == l]
                                          for l in multiple_letters_list}
        return multiple_letters_position_dict


def correct_hint_colours_for_duplicates(dict_of_multiple_letters_position, letter, simple_wordle_hint, word_to_guess):
    """
    Function to add in the logic of changing duplicate letters labelled as "Y" to "B" if they appear more frequently
    in the guessed word than the secret word.

    Takes in the "hint" colour list created earlier and corrects it if required for any letters identified as duplicate
    if required.

    :param dict_of_multiple_letters_position:
    :param letter:
    :param simple_wordle_hint:
    :param word_to_guess:
    :return:
    """
    # colours = list()
    duplicates_wordle_hint = list(simple_wordle_hint) #simple_wordle_hint.copy()

    if [i for i in dict_of_multiple_letters_position[letter] if duplicates_wordle_hint[i] == "G"]:
        for index in dict_of_multiple_letters_position[letter]:
            if duplicates_wordle_hint[index] == "Y":
                duplicates_wordle_hint[index] = "B"
    else:
        no_of_instances_guess = len(dict_of_multiple_letters_position[letter])
        no_of_instances_secret = list(word_to_guess).count(letter)
        extra_instances = no_of_instances_guess - no_of_instances_secret
        last_instance_yellow = no_of_instances_guess - extra_instances - 1
        list_of_positions = dict_of_multiple_letters_position[letter]

        for i in range(len(list_of_positions)):
            if i > last_instance_yellow:
                index = list_of_positions[i]
                duplicates_wordle_hint[index] = "B"
    return "".join(duplicates_wordle_hint)


def return_corrected_wordle_clue(entered_word, word_to_guess):
    simple_wordle_hint = return_wordle_colours_str(entered_word, word_to_guess)
    duplicates_wordle_hint = simple_wordle_hint #simple_wordle_hint.copy()
    list_of_multiple_letters = identify_duplicate_letters(entered_word)
    dict_of_multiple_letters_position = get_position_of_multiple_letters_opt(entered_word, list_of_multiple_letters)

    if not dict_of_multiple_letters_position: # (dict_of_multiple_letters) < 1:
        pass
    else:
        # print("Duplicate Letters Exist In Guess ")
        # print(dict_of_multiple_letters_position)
        for letter in dict_of_multiple_letters_position.keys():
            if letter not in word_to_guess:
                pass
            elif len(dict_of_multiple_letters_position[letter]) == list(word_to_guess).count(letter):
                pass
            else:
                duplicates_wordle_hint = correct_hint_colours_for_duplicates(dict_of_multiple_letters_position, letter,
                                                                             simple_wordle_hint, word_to_guess)
    return duplicates_wordle_hint


def return_corrected_wordle_colours_list(entered_word, word_to_guess, dict_of_multiple_letters_position=None):
    """
    Combine functions to return the corrected colours hint once duplicate letters have been taken into account
    :param entered_word:
    :param word_to_guess:
    :param dict_of_multiple_letters_position:
    :return:
    """
    simple_wordle_hint = return_wordle_colours_str(entered_word, word_to_guess)
    duplicates_wordle_hint = simple_wordle_hint #simple_wordle_hint.copy()
    #dict_of_multiple_letters = identify_duplicate_letters(entered_word)

    if not dict_of_multiple_letters_position: # (dict_of_multiple_letters) < 1:
        pass
    else:
        # print("Duplicate Letters Exist In Guess ")
        # print(dict_of_multiple_letters_position)
        for letter in dict_of_multiple_letters_position.keys():
            if letter not in word_to_guess:
                pass
            elif len(dict_of_multiple_letters_position[letter]) == list(word_to_guess).count(letter):
                pass
            else:
                duplicates_wordle_hint = correct_hint_colours_for_duplicates(dict_of_multiple_letters_position, letter,
                                                                             simple_wordle_hint, word_to_guess)
    return duplicates_wordle_hint


def compute_wordle_colours_for_one_word(entered_word, potential_solutions):
    """
    Compare the hint given for all remaining words in a wordset against the guessed word and return a dictionary
    of words and hints.
    :param entered_word:
    :param potential_solutions:
    :return:
    """
    dict_of_possible_guesses = dict()
    list_of_duplicate_letters = identify_duplicate_letters(entered_word)
    if not list_of_duplicate_letters:
        for word in potential_solutions:
            guess_colours = return_wordle_colours_str(entered_word, word) #return_wordle_colours_list(entered_word, word)
            dict_of_possible_guesses[word] = guess_colours
    else:
        for word in potential_solutions:
            dict_of_multiple_letters_position = get_position_of_multiple_letters_opt(entered_word,
                                                                                     list_of_duplicate_letters)
            guess_colours = return_corrected_wordle_colours_list(entered_word, word, dict_of_multiple_letters_position)
            dict_of_possible_guesses[word] = guess_colours
    return dict_of_possible_guesses


def sum_groups_of_hints(hints):
    """
    Takes the input of a dictionary of words and hints produce a dictionary of the number of instances of each type of
    hint
    :param hints:
    :return:
    """
    # dict_of_groups = dict()
    dict_of_groups = Counter(list(hints.values()))
    # for key in hints:
    #     group = str(hints[key])
    #     if group in dict_of_groups.keys():
    #         words_in_group_count = dict_of_groups[group] + 1
    #         dict_of_groups[group] = words_in_group_count
    #     else:
    #         dict_of_groups[group] = 1
    return dict_of_groups


def average_solutions_left_after_guess(dict_of_hints):
    """
    Calcultes the average remaining number of solutions expected after a guess by looking at the probability
    of each outcome
    :param dict_of_hints:
    :return:
    """
    total_words = sum(dict_of_hints.values())
    dict_values = np.array(list(dict_of_hints.values()))
    prob_list = dict_values / np.array(total_words)
    total_prob = dict_values * prob_list
    average_number_of_words = sum(total_prob)
    return average_number_of_words


def is_word_in_list(word, list_of_words):
    """
    Checks if a word is present in a list of words or not. Used to indicate whether a guess could be a potential
    answer and thus prioritised as a guess.
    :param word:
    :param list_of_words:
    :return:
    """
    if word in list_of_words:
        return 1
    else:
        return 0


def create_guess_df(starting_word, words_left, word_groups, possible_solution):
    df = pd.DataFrame()
    df["Guess"] = [starting_word]
    df["AverageRemainingSolutions"] = [words_left]
    df["NumberOfGroups"] = [len(word_groups)]
    df["WordsPerGroup"] = [sum(word_groups.values()) / len(word_groups)]
    df["PotentialSolution"] = [possible_solution]
    return df


def create_guess_list(starting_word, words_left, word_groups, possible_solution):
    NumberOfGroups = len(word_groups)
    WordsPerGroup = sum(word_groups.values()) / len(word_groups)
    output_list = [starting_word, words_left, NumberOfGroups, WordsPerGroup, possible_solution]
    return output_list


def eliminate_solutions_from_corpus(word_dict, hint):
    word_corpus = list()
    for key in word_dict:
        if word_dict[key] == hint:
            word_corpus.append(key)
    return word_corpus


if __name__ == "__main__":
    print(dev_return_wordle_colours_list("teeth", "saver"))
