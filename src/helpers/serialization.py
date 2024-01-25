from collections import UserDict
import pickle
from pathlib import Path
import os


class Serialization(UserDict):
    def __init__(self):
        self.__abook_file = "book_file.bin"
        self.data = {}

    def serialization(self, contacts_book, notes_book):
        self.data = dict(full_content=dict(contacts=contacts_book, notes=notes_book))
        with open(self.__abook_file, "wb") as fh:
            pickle.dump(self.data, fh)

    def check_file_exist(self):
        return Path(self.__abook_file).exists()

    def unserialization(self):
        if self.check_file_exist():
            if os.stat(self.__abook_file).st_size != 0:
                with open(self.__abook_file, "rb") as fh:
                    self.data = pickle.load(fh)
        return self.data
