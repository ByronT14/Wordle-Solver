import json
from definitions import ROOT_DIR
import os

test_path = os.path.join(ROOT_DIR, "word_lists", "five_letter_words_no_caps.json")


def import_json_to_list(file_path):
    fileObject = open(file_path, "r")
    jsonContent = fileObject.read()
    aList = json.loads(jsonContent)
    return aList


if __name__ == "__main__":
    five_letter_words = import_json_to_list(test_path)
    print(five_letter_words)
