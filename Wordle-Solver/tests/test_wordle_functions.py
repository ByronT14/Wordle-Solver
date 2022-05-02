import pytest
from wordle_solver import wordle_functions as wf


def test_return_wordle_colours_list():
    assert(wf.return_wordle_colours_list("raise", "apoop") == ["B", "Y", "B", "B", "B"])
    assert(wf.return_wordle_colours_list("raise", "raise") == ["G", "G", "G", "G", "G"])
    assert(wf.return_wordle_colours_list("fever", "saver") == ["B", "Y", "G", "G", "G"])
    assert(wf.return_wordle_colours_list("teale", "fever") == ["B", "G", "B", "B", "Y"])
    assert(wf.return_wordle_colours_list('metes', "inert") == ["B", "Y", "Y", "Y", "B"])


def test_return_wordle_colours_str():
    assert(wf.return_wordle_colours_str("raise", "apoop") == "BYBBB") #["B", "Y", "B", "B", "B"])
    # assert(wf.return_wordle_colours_list("raise", "raise") == ["G", "G", "G", "G", "G"])
    # assert(wf.return_wordle_colours_list("fever", "saver") == ["B", "Y", "G", "G", "G"])
    # assert(wf.return_wordle_colours_list("teale", "fever") == ["B", "G", "B", "B", "Y"])
    # assert(wf.return_wordle_colours_list('metes', "inert") == ["B", "Y", "Y", "Y", "B"])


def test_identify_duplicate_letters():
    assert(wf.identify_duplicate_letters("metes") == ["e"])
    assert(wf.identify_duplicate_letters("memes") == ["m", "e"] or ["e", "m"])
    assert(wf.identify_duplicate_letters("teeth") == ["t", "e"] or ["e", "t"])


def test_get_position_of_multiple_letters():
    assert(wf.get_position_of_multiple_letters("metes", ["e"]) == {"e": [1, 3]})
    assert (wf.get_position_of_multiple_letters("memes", ["e", "m"]) == {"e": [1, 3], "m": [0, 2]})


def test_get_position_of_multiple_letters_opt():
    assert(wf.get_position_of_multiple_letters_opt("metes", ["e"]) == {"e": [1, 3]})
    assert (wf.get_position_of_multiple_letters_opt("memes", ["e", "m"]) == {"e": [1, 3], "m": [0, 2]})


def test_return_world_clue():
    assert(wf.return_corrected_wordle_clue("fever", "saver") == "BBGGG") #["B", "B", "G", "G", "G"])
    # assert(wf.return_corrected_wordle_clue("raise", "apoop") == ["B", "Y", "B", "B", "B"])
    # assert(wf.return_corrected_wordle_clue("raise", "raise") == ["G", "G", "G", "G", "G"])
    # assert(wf.return_corrected_wordle_clue("fever", "saver") == ["B", "B", "G", "G", "G"])
    # assert(wf.return_corrected_wordle_clue("teale", "fever") == ["B", "G", "B", "B", "Y"])
    # assert(wf.return_corrected_wordle_clue("teale", "saver") == ["B", "Y", "Y", "B", "B"])
    # assert(wf.return_corrected_wordle_clue('metes', "inert") == ["B", "Y", "Y", "B", "B"])
    # assert (wf.return_corrected_wordle_clue('memes', "inert") == ["B", "Y", "B", "B", "B"])


def test_return_corrected_wordle_colours_list():
    assert (wf.return_corrected_wordle_colours_list("fever", "saver", {"e": [1, 3]}) == "BBGGG") #["B", "B", "G", "G", "G"])
    # assert(wf.return_corrected_wordle_colours_list("raise", "apoop", None) == ["B", "Y", "B", "B", "B"])
    # assert(wf.return_corrected_wordle_colours_list("raise", "raise", None) == ["G", "G", "G", "G", "G"])
    # assert(wf.return_corrected_wordle_colours_list("fever", "saver", {"e": [1, 3]}) == ["B", "B", "G", "G", "G"])
    # assert(wf.return_corrected_wordle_colours_list("teale", "fever", {"e": [1, 4]}) == ["B", "G", "B", "B", "Y"])
    # assert(wf.return_corrected_wordle_colours_list("teale", "saver", {"e": [1, 4]}) == ["B", "Y", "Y", "B", "B"])
    # assert(wf.return_corrected_wordle_colours_list('metes', "inert", {"e": [1, 3]}) == ["B", "Y", "Y", "B", "B"])
    # assert (wf.return_corrected_wordle_colours_list('memes', "inert", {"e": [1, 3], "m": [0, 2]}) == ["B", "Y", "B", "B", "B"])


def test_compute_wordle_colours_for_one_word():
    test_list = ["raise", "arise", "swoon", "memes"]
    test_output = wf.compute_wordle_colours_for_one_word("memes", test_list)
    # expected_output = {"raise": ["B", "Y", "B", "B", "Y"],
    #                    "arise": ["B", "Y", "B", "B", "Y"],
    #                    "swoon": ["B", "B", "B", "B", "Y"],
    #                    "memes": ["G", "G", "G", "G", "G"]}
    expected_output = {"raise": "BYBBY", # ["B", "Y", "B", "B", "Y"],
                       "arise": "BYBBY", #["B", "Y", "B", "B", "Y"],
                       "swoon": "BBBBY",  #["B", "B", "B", "B", "Y"],
                       "memes": "GGGGG"} #["G", "G", "G", "G", "G"]}
    assert(test_output == expected_output)


def test_sum_groups_of_hints():
    # test_dict = {"raise": ["G", "G", "G", "G", "G"],
    #              "arise": ["Y", "Y", "G", "G", "G"],
    #              "swoon": ["B", "B", "B", "Y", "B"],
    #              "swoop": ["B", "B", "B", "Y", "B"]}
    #
    # expected_output = {"['G', 'G', 'G', 'G', 'G']": 1,
    #                    "['Y', 'Y', 'G', 'G', 'G']": 1,
    #                    "['B', 'B', 'B', 'Y', 'B']": 2}

    test_dict = {"raise": "GGGGG",
                 "arise": "YYGGG",  #["Y", "Y", "G", "G", "G"],
                 "swoon": "BBBYB", #["B", "B", "B", "Y", "B"],
                 "swoop": "BBBYB"} #["B", "B", "B", "Y", "B"]}

    expected_output = {"GGGGG": 1,
                       "YYGGG": 1,
                       "BBBYB": 2}

    test_output = wf.sum_groups_of_hints(test_dict)
    print(test_output)
    assert(test_output == expected_output)


def test_average_solutions_left_after_guess():
    test_dict = {"BYBBB": 528,
                 "BBBBB": 532,
                 "BBBYB": 234
                 }
    sum_of_words = sum([528, 532, 234])
    average_number_of_words = (528/sum_of_words) * 528 + (532/sum_of_words) * 532 + (234/sum_of_words) * 234
    test_output = wf.average_solutions_left_after_guess(test_dict)
    assert(test_output == average_number_of_words)


if __name__ == "__main__":
    test_sum_groups_of_hints()