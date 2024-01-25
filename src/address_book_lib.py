from collections import UserDict
from src.classes.record import Record


class AddressBook(UserDict):
    def __init__(self):
        # self.list_items = []
        self.list_count = 0
        self.data = {}

    def add_record(self, value):
        self.data[value.name.value] = value

    def find(self, name):
        if name in self.data.keys():
            record = Record(name)
            record.phones = self.data[name]
            return self.data.get(name)
        else:
            return None

    def delete(self, name):
        if name in self.data.keys():
            self.data.pop(name)

    def list_creator(self):
        self.list_items = []
        for item in self.data.values():
            self.list_items.append(item)
        self.list_count = len(self.list_items)

    def iterator(self, from_el=0, to_el=2):
        if self.list_count > 0 and from_el < self.list_count:
            return (x for x in self.list_items[from_el:to_el])

    def search(self, str):
        searched_items = {}
        for val, key in self.data.items():
            if val.find(str) != -1:
                searched_items.update({val: key})
                continue
            for phone in key.phones:
                if phone.value.find(str) != -1:
                    searched_items.update({val: key})
        return searched_items if len(searched_items) > 0 else 0
