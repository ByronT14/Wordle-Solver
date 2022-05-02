from wordle_solver import wordle_functions as wf
from wordle_solver import file_imports
import pandas as pd
import json
import numpy as np
from definitions import ROOT_DIR
import os
import time

file_path = os.path.join(ROOT_DIR, "word_lists", "five_letter_words_no_caps.json")
csv_path = os.path.join(ROOT_DIR, "word_lists", "starter_words.csv")
guesses_path = os.path.join(ROOT_DIR, "word_lists", "wordle_candidates_nyt.json")
solutions_path = os.path.join(ROOT_DIR, "word_lists", "wordle_solutions_nyt.json")


def test_word_guesser(all_words, potential_words):
    first_guess_df = pd.DataFrame()
    for i in all_words: # ["raise","crane"]: #
        guess_results = wf.compute_wordle_colours_for_one_word(i, potential_words)
        sum_of_groups = wf.sum_groups_of_hints(guess_results)
        expected_words_left = wf.average_solutions_left_after_guess(sum_of_groups)
        potential_solution = wf.is_word_in_list(i, potential_words)
        guess_df = wf.create_guess_df(i, expected_words_left, sum_of_groups, potential_solution)
        first_guess_df = pd.concat([first_guess_df, guess_df])
    first_guess_df = first_guess_df.sort_values(by=["NumberOfGroups","PotentialSolution"], ascending=[False, False])
    return first_guess_df


def test_time_compute_wordle_colours_simple(all_words, potential_words):
    start_time = time.time()
    for i in all_words:
        for word in potential_words:
            wf.return_wordle_colours_list(i, word)

    duration = time.time() - start_time
    print(f'{len(all_words)} guesses for {len(potential_words)} solutions takes {duration}')
    pass


def test_time_return_corrected_wordle_clue(all_words, potential_words):
    start_time = time.time()
    for i in all_words:
        for word in potential_words:
            wf.return_corrected_wordle_clue(i, word)
    duration = time.time() - start_time
    print(f'{len(all_words)} guesses for {len(potential_words)} solutions takes {duration}')
    pass


def test_time_compute_wordle_colours(all_words, potential_words):
    start_time = time.time()
    for i in all_words:
        guess_results = wf.compute_wordle_colours_for_one_word(i, potential_words)
        sum_of_groups = wf.sum_groups_of_hints(guess_results)

    duration = time.time() - start_time
    print(f'{len(all_words)} guesses for {len(potential_words)} solutions takes {duration}')
    pass


def test_feedback(guess, word_to_guess,  potential_words):
    start_time = time.time()
    feedback = wf.return_corrected_wordle_clue(guess, word_to_guess)
    solutions = [i for i in potential_words if
                      wf.return_corrected_wordle_clue(guess, i) == feedback]
    duration = time.time() - start_time
    print(f'{len(potential_words)} guesses for {len(potential_words)} solutions takes {duration}')


def comp_duplicates(all_words):
    start_time = time.time()
    for entered_word in all_words:
        test_list = wf.identify_duplicate_letters(entered_word)
        wf.get_position_of_multiple_letters(entered_word, test_list)
    duration = time.time() - start_time
    print(f'{len(all_words)} guess takes {duration} using the simple way')

    start_time = time.time()
    for entered_word in all_words:
        test_list = wf.identify_duplicate_letters(entered_word)
        wf.get_position_of_multiple_letters_opt(entered_word, test_list)
    duration = time.time() - start_time
    print(f'{len(all_words)} guess takes {duration}using the optimised way')
    return



if __name__ == "__main__":
    five_letter_words = file_imports.import_json_to_list(file_path)
    allowed_guesses = file_imports.import_json_to_list(guesses_path)["words"]
    potential_solutions = file_imports.import_json_to_list(solutions_path)["words"]
    total_guesses = allowed_guesses + potential_solutions
    first_guess = "trace"
    secret_word = "olive"

    test_guesses = total_guesses # ["metes"] #
    test_solutions = potential_solutions
    #test_guesses = [i for i in total_guesses[:1000] if wf.identify_duplicate_letters(i)]
    print(test_guesses)

    # comp_duplicates(test_guesses)
    # test_time_compute_wordle_colours_simple(test_guesses, test_solutions)
    # test_time_return_corrected_wordle_clue(test_guesses, test_solutions)
    # test_time_compute_wordle_colours(test_guesses, test_solutions)

    test_feedback("trace","story", test_solutions)



    # start_time = time.time()
    # for i in range(100): # ["raise","crane"]: #
    #     entered_word = total_guesses[i]
    #     for word_to_guess in potential_solutions:
    #         simple_wordle_hint = wf.return_wordle_colours_list(entered_word, word_to_guess)
    #         # duplicates_wordle_hint = simple_wordle_hint.copy()
    #         #
    #         # dict_of_multiple_letters = wf.identify_duplicate_letters(entered_word)
    #     #guess_results = wf.compute_wordle_colours_for_one_word(total_guesses[i], potential_solutions)
    #     #sum_of_groups = wf.sum_groups_of_hints(guess_results)
    #
    # duration = time.time() - start_time
    # print(f'One guess takes {duration}')
    #
    # start_time = time.time()
    # test_word_guesser(total_guesses, potential_solutions)
    # duration = time.time() - start_time
    # print(f'Total guess dataframe takes {duration}')


    # if secret_word in allowed_guesses:
    #     print("the secret word is in the guess list")
    # else:
    #     print("ERROR")
    # try:
    #     secret_word in allowed_guesses
    # except:
    #     raise RuntimeError("secret word not in list of guesses")
    #
    # # test_colours = wf.return_wordle_colours_list("raise", secret_word)
    # # first_guess_results = wf.compute_wordle_colours_for_one_word("raise", potential_solutions)
    # # remaining_solutions = wf.eliminate_solutions_from_corpus(first_guess_results, test_colours)
    # remaining_solutions = potential_solutions.copy()
    # for i in range(6):
    #     if i == 0:
    #         guesses_list = [first_guess]
    #     else:
    #         guesses_list = total_guesses.copy()
    #     next_guess_df = test_word_guesser(guesses_list, remaining_solutions)
    #     suggested_guess = next_guess_df.iloc[0:9]
    #     print(suggested_guess)
    #     next_guess = input("please enter your 5 letter word")
    #     return_guess_colours = wf.return_wordle_colours_list(next_guess, secret_word)
    #     print("The colours after your guess are ", return_guess_colours)
    #     colour_feedback = list(input("Please enter your guess feedback"))
    #     next_guess_results = wf.compute_wordle_colours_for_one_word(next_guess, remaining_solutions)
    #     sum_of_groups_after_guess = wf.sum_groups_of_hints(next_guess_results)
    #     print(sum_of_groups_after_guess)
    #     remaining_solutions = wf.eliminate_solutions_from_corpus(next_guess_results, colour_feedback)
    #     print("This is guess number", i + 1)
    #     print("The next guess is: ", next_guess)
    #     print("the expected outcome is...")
    #     print(next_guess_df[next_guess_df["Guess"] == next_guess])
    #     print("The number of solutions remaining are: ", len(remaining_solutions))
    #     print("The number of groups left are: ", len(sum_of_groups_after_guess))
    #     if next_guess == secret_word:
    #         print("Wordle Solved", next_guess, secret_word)
    #         break



