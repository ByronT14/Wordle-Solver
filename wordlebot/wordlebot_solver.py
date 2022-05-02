import pandas as pd
import itertools
import numpy as np
import json
import os
import time

from wordle_solver.wordle_functions import (compute_wordle_colours_for_one_word, eliminate_solutions_from_corpus,
                                            return_corrected_wordle_colours_list, return_corrected_wordle_clue,
                                            return_wordle_colours_list, sum_groups_of_hints,
                                            average_solutions_left_after_guess, is_word_in_list, create_guess_df)

from wordle_solver import file_imports
from definitions import ROOT_DIR

file_path = os.path.join(ROOT_DIR, "word_lists", "five_letter_words_no_caps.json")
csv_path = os.path.join(ROOT_DIR, "word_lists", "starter_words.csv")
guesses_path = os.path.join(ROOT_DIR, "word_lists", "wordle_candidates_nyt.json")
solutions_path = os.path.join(ROOT_DIR, "word_lists", "wordle_solutions_nyt.json")


def test_word_guesser(all_words, potential_words):
    first_guess_df = pd.DataFrame()
    for i in all_words:  # ["raise","crane"]: #
        guess_results = compute_wordle_colours_for_one_word(i, potential_words)
        sum_of_groups = sum_groups_of_hints(guess_results)
        expected_words_left = average_solutions_left_after_guess(sum_of_groups)
        potential_solution = is_word_in_list(i, potential_words)
        guess_df = create_guess_df(i, expected_words_left, sum_of_groups, potential_solution)
        first_guess_df = pd.concat([first_guess_df, guess_df])
    first_guess_df = first_guess_df.sort_values(by=["NumberOfGroups", "PotentialSolution"],
                                                ascending=[False, False])
    return first_guess_df


class Wordle():
    def __init__(self, candidates, solutions, solution=None, verbose=True):
        self.guesses = []
        self.feedback = []
        self.candidates = candidates
        self.solutions = solutions
        self.solution = solution
        self.step = 0
        self.solved = False
        self.verbose = verbose

        if solution:
            self.solution = solution
            if solution not in solutions:
                raise ValueError('The solution given is not in the recorded list of solutions')
        else:
            self.solution = None

    def enter_guess(self, guess, solution = None, feedback = None):
        #next_guess_results = compute_wordle_colours_for_one_word(guess, self.solutions)
        if self.solution:
            feedback = return_corrected_wordle_clue(guess, self.solution)
        else:
            # maybe need to manually enter feedback
            if not feedback:
                #TODO: Why is a list still required?
                feedback = input("Please enter the wordle feedback provided")
                #raise ValueError('Please provide feedback')

        print(feedback)

        if feedback:
            #self.solutions = eliminate_solutions_from_corpus(next_guess_results, feedback)
            self.solutions = [i for i in self.solutions if
                              return_corrected_wordle_clue(guess, i) == feedback]

        #save data
        self.guesses.append(guess)
        self.feedback.append(feedback)
        self.step += 1

        if self.verbose:
            print(f'{guess} --> {feedback}: {len(self.solutions)} solutions remaining.')

        if feedback == 'GGGGG':
            self.solved = True
            if self.verbose:
                print(f'{self.guesses} --> {self.solution} in {self.step} steps')

    def calculate_next_guess(self):
        if len(self.solutions) == 1:
            guess_priority_df = test_word_guesser(self.solutions, self.solutions)
        else:
            guess_priority_df = test_word_guesser(self.candidates, self.solutions)
        return guess_priority_df

    def records(self):
        return {
            'steps': self.step,
            'words': self.guesses,
            'feedback': self.feedback,
        }




five_letter_words = file_imports.import_json_to_list(file_path)
allowed_guesses = file_imports.import_json_to_list(guesses_path)["words"]
potential_solutions = file_imports.import_json_to_list(solutions_path)["words"]
total_guesses = allowed_guesses + potential_solutions


def play_game(input_word, solution):
    game = Wordle(total_guesses, potential_solutions, solution=solution, verbose=True)

    while not game.solved:
        start_time = time.time()
        if game.step == 0:
            game.enter_guess(input_word)
        else:
            guess_df = game.calculate_next_guess()
            if game.solution:
                game.enter_guess(guess_df.Guess.iloc[0])
            else:
                print(guess_df.iloc[:10])
                manual_guess = input("Enter your guess")
                game.enter_guess(manual_guess)
        duration = time.time() - start_time
        print(f'This guess took {duration} seconds to process')

        # if not game.solved:
        #     game.optimise(method=METHOD.lower(), n_jobs=-2)
        #     if game.optimisations[METHOD.lower()][METHOD.lower()].nunique() == 1 and \
        #             game.solutions.shape[0] > 3:
        #         df_splitter = game.split_duplicates()
        #         if df_splitter is not None:
        #             game.guess(df_splitter.word.iloc[0])
        #             continue

    return game.records()



if __name__ == '__main__':
    play_game("trace", None)

