import pandas as pd
import numpy as np
import pickle
import itertools

from wordle_solver import starter_words as sw
from wordle_solver import create_starting_list as csl
# from wordle_solver import solver as sv
from nltk.corpus import words

word_list = words.words()


def all_colour_combinations():
    """
    Function to return all potential combinations of Black, Yellow and Green for a 5 letter guess
    :return: list of lists ie. [["Y","Y","Y","Y","Y"],["Y","Y","Y","Y","B"]]
    """
    colours = ["B", "Y", "G"]
    combos = list(itertools.product(colours, repeat=5))
    return combos


def colour_combo_starting_dict(colour_combos):
    """
    Function to create a dictionary containing each potential colour combination of a wordle guess as the key
    and setting the value for each key as 0
    :param colour_combos: list of lists containing colour combinations
    :return: dictionary containing keys of colour combinations and values of 0
    """
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


def product_probs(word_dict, word_corpus):
    new_word_corpus = word_corpus.copy()
    print("product probs new word corpus", len(new_word_corpus))
    total_words = len(new_word_corpus)
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
    print("best_word", word_df.index[0])
    print(word_df.reset_index().iloc[:10])
    return word_df.index[0]


class WordSolver:
    def __init__(self, secret_word, word_corpus, difficulty):
        # self.starter_word = starter_word
        self.secret_word = secret_word
        self.potential_words = word_corpus.copy()
        self.difficulty = difficulty
        self.remaining_words = set()
        self.suggestion_dict = {0: "", 1: "", 2: "", 3: "", 4: ""}
        self.suggestion_colour_dict = {0: "", 1: "", 2: "", 3: "", 4: ""}
        self.suggestion_dict_tuple = {0: tuple(), 1: tuple(), 2: tuple(), 3: tuple(), 4: tuple()}
        self.all_suggestion_colours = np.empty((0, 5), dict)
        self.word_guess = str()
        self.word_guesses = list()
        self.output_df = pd.DataFrame()
        self.alphabet_list = [
            "a", "b", "c", "d", "e", "f", "g", "h", "i", "j",
            "k", "l", "m", "n", "o", "p", "q", "r", "s", "t",
            "u", "v", "w", "x", "y", "z"
        ]
        self.alphabet_dict = dict(zip(self.alphabet_list, []*len(self.alphabet_list)))
        self.green_dict = dict()
        self.yellow_dict = dict()
        self.black_list = list()

        self.colour_combos = all_colour_combinations()
        self.colour_start_dict = colour_combo_starting_dict(self.colour_combos)


    def get_user_input(self):
        guess = input("please enter your 5 letter word")
        #todo: all of the try and exceptions
        self.word_guess = guess
        self.word_guesses.append(guess)
        print(f"your guess is {guess}")

    def return_wordle_colours_dict(self):
        entered_word = self.word_guess
        word_to_guess = self.secret_word
        for i in range(5):
            letter = entered_word[i]
            if letter == word_to_guess[i]:
                colour = "G"
            elif letter in word_to_guess:
                colour = "Y"
            else:
                colour = "B"
            d = {i: letter}
            d2 = {i: colour}
            d3 = (colour, letter)
            self.suggestion_dict.update(d)
            self.suggestion_colour_dict.update(d2)
            self.suggestion_dict_tuple[i] = d3
        # print(self.suggestion_dict_tuple)
        # colours_hist = self.all_suggestion_colours
        # colours_hist = np.append(self.suggestion_colour_dict, colours_hist)
        # print(colours_hist)

    def remove_words_from_corpus(self):
        for key in self.suggestion_dict_tuple.keys():
            index = key
            colour = self.suggestion_dict_tuple[key][0]
            letter = self.suggestion_dict_tuple[key][1]
            # print(index, colour, letter)
            if colour == "B":
                self._remove_words_colour_black(letter)
                #Todo: remove words black
            elif colour == "G":
                self._remove_words_colour_green(index, letter)
                # self._add_green_words(self, index, letter)
            else:
                self._remove_words_colour_yellow(index, letter)
                # self._add_yellow_words(index, letter)
        print(f"There are {len(self.potential_words)} left")
        #print(sorted(self.potential_words))

    def _add_green_words(self, guess_index, guess_letter):
        if len(self.remaining_words) >0:
            for word in self.potential_words:
                if guess_letter == word[guess_index]:
                    self.remaining_words.add(word)

    def _add_yellow_words(self, guess_index, guess_letter):
        for word in self.potential_words:
            if guess_letter == word[guess_index]:
                pass
            elif guess_letter in word:
                self.remaining_words.add(word)
            else:
                pass

    def _remove_words_colour_green(self, guess_index, guess_letter):
        remove_words = set()
        for word in self.potential_words:
            if guess_letter == word[guess_index]:
                pass
            else:
                remove_words.add(word)
        for word in remove_words:
            self.potential_words.remove(word)

    def _remove_words_colour_black(self, guess_letter):
        remove_words = set()
        for word in self.potential_words:
            if guess_letter in word:
                remove_words.add(word)
        for word in remove_words:
            self.potential_words.remove(word)

    def _remove_words_colour_yellow(self, guess_index, guess_letter):
        remove_words = set()
        for word in self.potential_words:
            if guess_letter == word[guess_index]:
                remove_words.add(word)
            elif guess_letter in word:
                pass
            else:
                remove_words.add(word)
        for word in remove_words:
            self.potential_words.remove(word)

    def update_green_alphabet_dict(self):
        entered_word = self.word_guess
        word_to_guess = self.secret_word
        for i in range(len(self.secret_word)):
            entered_letter = entered_word[i]
            secret_letter = word_to_guess[i]
            if entered_letter == secret_letter:
                self.green_dict[i] = secret_letter

    def update_yellow_alphabet_dict(self):
        entered_word = self.word_guess
        word_to_guess = self.secret_word
        for i in range(len(self.secret_word)):
            entered_letter = entered_word[i]
            secret_letter = word_to_guess[i]
            if entered_letter == secret_letter:
                pass
            elif entered_letter in word_to_guess:
                if entered_letter in list(self.yellow_dict.keys()):
                    new_list = list(self.yellow_dict[entered_letter])
                    new_list.append(i)
                    self.yellow_dict[entered_letter] = set(new_list)
                else:
                    self.yellow_dict[entered_letter] = [i]
            else:
                self.black_list.append(entered_letter)

        print(self.yellow_dict)
        print(self.black_list)

    def update_corpus_from_green_dict(self):
        # print(f"There are {len(self.potential_words)} left")
        words_to_remove = set()
        print(self.green_dict)
        if self.green_dict.keys():
            for word in self.potential_words:
                for position in self.green_dict.keys():
                    if self.green_dict[position] == word[position]:
                        pass
                    else:
                        words_to_remove.add(word)
        for i in words_to_remove:
            self.potential_words.remove(i)
        print(f"{len(words_to_remove)} have been be removed")
        print(f"There are {len(self.potential_words)} left")
        print(sorted(self.potential_words))

    def update_corpus_from_yellow_dict(self):
        words_to_remove = set()
        if self.yellow_dict.keys():
            for letter in self.yellow_dict.keys():
                for word in self.potential_words:
                    if letter in word:
                        for position in self.yellow_dict[letter]:
                            if letter == word[position]:
                                words_to_remove.add(word)
                    else:
                        words_to_remove.add(word)

        print(f"There are {len(words_to_remove)} words to remove")
        for word in words_to_remove:
            self.potential_words.remove(word)
        print(sorted(self.potential_words))

    def print_colour_dict(self):
        print(self.suggestion_colour_dict)

    def check_if_correct(self):
        if self.word_guess == self.secret_word:
            print("Well done! You guessed the word")
        else:
            pass

    def all_word_combos(self, starting_corpus):
        word_dict = dict()
        new_starting_corpus = starting_corpus.copy()
        counter = 0
        print(len(self.potential_words))
        print(len(new_starting_corpus))
        for entered_word in new_starting_corpus:
            # print(word_dict)
            counter_dict = self.colour_start_dict.copy()
            for word in self.potential_words:
                colour_output = return_wordle_colours(entered_word, word)
                counter_value = counter_dict[colour_output]
                counter_value += 1
                counter_dict[colour_output] = counter_value
            word_dict[entered_word] = counter_dict
            # word_dict[entered_word[colour_output]] = counter
            counter += 1
            #print(counter)
        print(len(self.potential_words))
        print(len(word_dict))
        return word_dict

    def guess_summary(self, guess_number):
        print_text = f""
        print("Word of the day: ", self.secret_word, "Guess number: ", guess_number, self.word_guess,
              self.suggestion_colour_dict, "There are ", len(self.potential_words), " words left")

    def guess_summary_df(self, guess_number, method, mode):
        str1 = str()
        output_dict = dict()
        output_dict["secret_word"] = [self.secret_word]
        output_dict["guess_no"] = [guess_number]
        output_dict["guess"] = [self.word_guess]
        output_dict["result"] = [str1.join(self.suggestion_colour_dict.values())]
        output_dict["corpus_size"] = [len(self.potential_words)]
        output_dict["method"] = [method]
        output_dict["mode"] = [mode]
        print(output_dict)
        output_df = pd.DataFrame(output_dict)
        self.output_df = self.output_df.append(output_df)
        #print(pd.DataFrame(output_dict))
        #print(pd.DataFrame.from_dict(output_dict,orient = "index"))


if __name__ == "__main__":
    word_list_no_dupes = sw.remove_duplicate_letters(word_list)
    print(len(csl.keep_n_letter_words(word_list_no_dupes, 5)))
    five_letter_words = csl.keep_n_letter_words(word_list_no_dupes, 5)
    print("number of fiver letter words ", len(five_letter_words))

    five_letter_words_no_caps = csl.remove_words_with_capitals(five_letter_words)
    print(len(five_letter_words), len(five_letter_words_no_caps))
    # for word in five_letter_words_no_caps:
    #     if word[0] == word[0].upper():
    #         print(word)

    # for i in range(6):
        # solver = WordSolver("humor", five_letter_words_no_caps)
        # solver.get_user_input()
        # solver.return_wordle_colours_dict()
        # solver.remove_words_from_corpus()


    #establish the solver
    solver = WordSolver("fever", five_letter_words_no_caps, "easy")

    if solver.secret_word in solver.potential_words:
        print("secret word exists")
    else:
        print("error - secret word missing")
    for a in range(6):
        if solver.word_guess == solver.secret_word:
            break
        print(f"This is go number {a}")
        if a == 0:
            test_word_combos = pickle.load(open("file1.pkl", "rb"))
        # elif len(solver.potential_words) == 1:
        #     print("1 word left")
        #     test_word_combos = solver.all_word_combos(solver.potential_words)
        else:
            test_word_combos = solver.all_word_combos(solver.potential_words) #solver.potential_words
        print("test word_combos",len(test_word_combos))
        print("five letter words no caps", len(five_letter_words_no_caps))
        word_average_probs = product_probs(test_word_combos, solver.potential_words)
        best_word = return_best_word(word_average_probs)
        solver.get_user_input()
        solver.return_wordle_colours_dict()
        solver.remove_words_from_corpus()
        solver.guess_summary_df(a, "Probability Matrix", "easy")
    print(solver.output_df)
    #
    #     solver.print_colour_dict()
    #     solver.check_if_correct()
    #     solver.update_green_alphabet_dict()
    #     solver.update_yellow_alphabet_dict()
    #     solver.update_corpus_from_green_dict()
    #     solver.update_corpus_from_yellow_dict()
