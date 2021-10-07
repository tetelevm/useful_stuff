"""
Pseudoword generator using books/text.
Requires prefetched data.

The algorithm is as follows:
  1) collect the entire text array
  2) move the cursor to a random place
  3) memorize the next two letters and write them into the resulting text
  4) move the cursor to a random place
  5) move the cursor forward to the first occurrence of these letters
     in the text
  6) if the resulting text is still insufficient, return to step 3)
"""

import re
from random import randint
from pathlib import Path


PATH_TO_TEXT = '/home/t/folder_with_text/'
CHARS_LEN = 1
WORD_COUNT = 500


class Generator:
    def __init__(self, path=PATH_TO_TEXT):
        self.text = self.find_text(path)
        self.len_text = len(self.text)
        self.max_index = self.len_text - CHARS_LEN
        self.resulting_text = ''

    @staticmethod
    def find_text(path):
        paths_to_text = Path(path)

        if paths_to_text.is_file():
            paths_to_text = [paths_to_text]
        elif paths_to_text.is_dir():
            paths_to_text = paths_to_text.iterdir()
        else:
            raise ValueError(f'{path} is not file or dir!')

        text = '\n'.join(
            open(file, encoding="utf8").read()
            for file in paths_to_text
        )
        text = text.replace('\n', ' ')

        # removing unnecessary characters
        text = re.sub(r'[^А-Яа-я\s,.]', '', text)
        text = re.sub(r'\s+', ' ', text)
        text = text.lower().rstrip().lstrip()

        return text

    def generate(self) -> str:
        cursor = randint(0, self.max_index)
        current_chars = self.set_new_chars(cursor)

        while len(self.resulting_text.split(' ')) < WORD_COUNT:
            while True:
                cursor = randint(0, self.max_index)
                find_index = self.text[cursor : self.max_index].find(current_chars)
                if find_index != -1:
                    current_chars = self.set_new_chars(cursor + find_index + CHARS_LEN)
                    break

        return self.resulting_text

    def set_new_chars(self, index: int) -> str:
        """
        Takes the new characters and adds them to the result
        
        :index: cursor index
        :return: new current_chars
        """
        current_chars = self.text[index : index + CHARS_LEN]
        self.resulting_text += current_chars
        self.resulting_text = re.sub(r'\s+', ' ', self.resulting_text)
        return current_chars

if __name__ == '__main__':
    generated_text = Generator().generate()
    print(generated_text)
