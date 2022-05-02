import nltk
from nltk.corpus import words
import pandas as pd
import itertools
import numpy as np
import json
import pickle

word_list = words.words()

alphabet_list = [
    "a", "b", "c", "d", "e", "f", "g", "h", "i", "j",
    "k", "l", "m", "n", "o", "p", "q", "r", "s", "t",
    "u", "v", "w", "x", "y", "z"
]

starter_words = ["raise", "arise"]
test_words = ["raise", "arise", "fuzzy"]


def letter_analysis(list_of_letters, starting_words):
    """

    :param list_of_letters:
    :param starting_words:
    :return:
    """
    word_counter = dict()
    for letter in list_of_letters:
        counter = 0
        for word in starting_words:
            if letter in word:
                counter += 1
        word_counter[letter] = [counter]
    return word_counter


def remove_duplicate_letters(text_string):
    """

    :param text_string:
    :return:
    """
    return set(text_string)


def word_coverage(word_corpus):
    word_to_word_coverage = dict()
    for word in word_corpus:
        words_covered = set()
        for letter in word:
            for new_word in word_corpus:
                if letter in new_word:
                    words_covered.add(new_word)
        word_to_word_coverage[word] = len(words_covered)
    return word_to_word_coverage


def word_green_coverage(word_corpus):
    word_to_word_coverage = dict()
    for word in word_corpus:
        words_covered = dict()
        for i in range(5):
            count = 0
            for new_word in word_corpus:
                if word[i] == new_word[i]:
                    count += 1
            words_covered[i] = count
        word_to_word_coverage[word] = words_covered
    return word_to_word_coverage


def word_green_coverage_sum(word_green_dict):
    sum_dict = dict()
    for key in word_green_dict:
        new_dict = word_green_dict[key]
        words = sum(list(new_dict.values()))
        sum_dict[key] = words
    return sum_dict



def word_to_word_letter_coverage(starting_words, letter_counter):
    word_dict = dict()
    for word in starting_words:
        counter = 0
        word_letter_dict = dict()
        unique_letters = remove_duplicate_letters(word)
        for letter in unique_letters:
            if letter == letter.upper():
                pass
            else:
                #counter += letter_counter[letter]
                word_letter_dict[letter] = letter_counter[letter]
        word_dict[word] = word_letter_dict
    return word_dict


def sum_word_letter_coverage(word_counting_dict):
    starter_coverage_dict = dict()
    for key in word_counting_dict:
        starter_coverage_dict[key] = sum(word_counting_dict[key].values())
    return starter_coverage_dict


def return_sorted_df_from_dict(word_counting_dict):
    df = pd.DataFrame.from_dict(word_counting_dict, orient="index", columns=["count"])
    df = df.sort_values(by="count", ascending=False)
    return df


def position_checker(starter_word_list, all_words):
    position_dict = dict()
    for starter_word in starter_word_list:
        green_counter_dict = dict()
        for i in range(5):
            green = 0
            for word in all_words:
                if starter_word[i] == word[i]:
                    green += 1
            green_counter_dict[i] = green
        position_dict[starter_word] = green_counter_dict
    return position_dict


def all_colour_combinations():
    colours = ["B", "Y", "G"]
    combos = list(itertools.product(colours, repeat=5))
    return combos


def colour_combo_starting_dict(colour_combos):
    colour_combo_dict = dict()
    for i in colour_combos:
        colour_combo_dict[i] = 0
    return colour_combo_dict


def return_wordle_colours(entered_word, word_to_guess):
    colour_output = list()
    for i in range(5):
        letter = entered_word[i]
        if letter == word_to_guess[i]:
            colour = "G"
        elif letter in word_to_guess:
            colour = "Y"
        else:
            colour = "B"
        colour_output.append(colour)
    return tuple(colour_output)


def all_word_combos(starting_corpus, word_corpus, starting_dict):
    word_dict = dict()
    counter = 0
    for entered_word in starting_corpus:
        # print(word_dict)
        counter_dict = starting_dict.copy()
        for word in word_corpus:
            colour_output = return_wordle_colours(entered_word, word)
            counter_value = counter_dict[colour_output]
            counter_value += 1
            counter_dict[colour_output] = counter_value
        word_dict[entered_word] = counter_dict
        # word_dict[entered_word[colour_output]] = counter
        counter +=1
        print(counter)
    return word_dict


def product_probs(word_dict, word_corpus):
    total_words = len(word_corpus)
    output = dict()
    for word in word_dict.keys():
        new_dict = word_dict[word]
        dict_values = np.array(list(new_dict.values()))
        prob_list = dict_values/np.array(total_words)
        total_prob = dict_values*prob_list
        output[word] = sum(total_prob)
    return output


def return_best_word(prob_dict):
    word_df = pd.DataFrame.from_dict(prob_dict, orient="index", columns=["word_count"])
    word_df = word_df.sort_values(by=["word_count"], ascending=[True])
    best_word = word_df.iloc[0]
    print(word_df.index[0])
    return word_df.index[0]


if __name__ == "__main__":
    print(list("raise"))
    print(len(keep_n_letter_words(word_list, 5)))
    five_letter_words = keep_n_letter_words(word_list, 5)
    print("number of fiver letter words ", len(five_letter_words))
    five_letter_words_no_caps = remove_words_with_capitals(five_letter_words)
    possible_combos = all_colour_combinations()
    combo_dict = colour_combo_starting_dict(possible_combos)
    # test_word_combos = all_word_combos(five_letter_words_no_caps, five_letter_words_no_caps, combo_dict)
    # with open('file1.pkl', 'wb') as f:
    #     pickle.dump(test_word_combos, f)
    test_word_combos = pickle.load(open("file1.pkl", "rb"))
    word_average_probs = product_probs(test_word_combos, five_letter_words_no_caps)
    # word_average_df = pd.DataFrame.from_dict(word_average_probs, orient="index", columns=["word_count"])
    # word_average_df = word_average_df.sort_values(by=["word_count"], ascending=[True])
    best_word = return_best_word(word_average_probs)
    colour_set = return_wordle_colours("raise", "arise")
    print(len(possible_combos))
    print("test")

    # print("number of five letter words with no caps: ", len(five_letter_words_no_caps))
    # letter_count = letter_analysis(alphabet_list, five_letter_words_no_caps)
    # print(letter_count)
    # letter_df = pd.DataFrame.from_dict(letter_count, orient="index", columns=["word_count"])
    # letter_df = letter_df.sort_values(by=["word_count"], ascending=[False])
    # #letter_df = letter_df.sort_values(by=1)
    # word_coverage_green = word_green_coverage(five_letter_words_no_caps)
    # word_coverage_sum = word_green_coverage_sum(word_coverage_green)
    # word_green_df = pd.DataFrame.from_dict(word_coverage_sum, orient="index", columns=["word_count"])
    # word_green_df = word_green_df.sort_values(by=["word_count"], ascending=[False])
    # word_coverage_dict = word_coverage(five_letter_words_no_caps)
    # # word_coverage_dict = word_to_word_letter_coverage(five_letter_words_no_caps, letter_count)
    # word_df = pd.DataFrame.from_dict(word_coverage_dict, orient="index", columns=["word_count"])
    # word_df = word_df.sort_values(by=["word_count"], ascending=[False])
    # coverage_dict_summary = sum_word_letter_coverage(word_coverage_dict)
    # # word_counter_df = return_sorted_df_from_dict(coverage_dict_summary)
    # # green_counter = position_checker(starter_words, five_letter_words_no_caps)