from wordle_solver import wordle_functions as wf
from wordle_solver import file_imports
import pandas as pd
import json
import numpy as np
from definitions import ROOT_DIR
import os

guesses_path = os.path.join(ROOT_DIR, "word_lists", "wordle_candidates_nyt.json")
solutions_path = os.path.join(ROOT_DIR, "word_lists", "wordle_solutions_nyt.json")
csv_path = os.path.join(ROOT_DIR, "word_lists", "starter_words.csv")

allowed_guesses = file_imports.import_json_to_list(guesses_path)["words"]
potential_solutions = file_imports.import_json_to_list(solutions_path)["words"]
total_guesses = allowed_guesses + potential_solutions


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

# def create_first_guess_df(starting_word, words_left, word_groups):
#     df = pd.DataFrame()
#     df["Guess"] = [starting_word]
#     df["AverageRemainingSolutions"] = [words_left]
#     df["NumberOfGroups"] = [len(word_groups)]
#     df["WordsPerGroup"] = [sum(word_groups.values()) / len(word_groups)]
#     return df


if  __name__ == "__main__":
    # first_guess_df = pd.DataFrame()
    # for i in five_letter_words: # ["raise","crane"]: #
    #     guess_results = wf.compute_wordle_colours_for_one_word(i, five_letter_words)
    #     sum_of_groups = wf.sum_groups_of_hints(guess_results)
    #     expected_words_left = wf.average_solutions_left_after_guess(sum_of_groups)
    #     guess_df = create_first_guess_df(i, expected_words_left, sum_of_groups)
    #     first_guess_df = pd.concat([first_guess_df, guess_df])

    first_guess_output = test_word_guesser(total_guesses, potential_solutions)
    first_guess_output.to_csv(csv_path, index=False)