from collections import UserDict


class NotesBook(UserDict):
    def __init__(self):
        self.data = {}

    def add_record(self, value):
        self.data[value.title] = value
        return value

    def search(self, search_str):
        search_str = search_str.lower()
        search_notes = {}
        for key, val in self.data.items():
            if val.title.lower().find(search_str) != -1:
                search_notes.update({key: val})
            elif val.description.lower().find(search_str) != -1:
                search_notes.update({key: val})
        return search_notes

    def search_by_tag(self, search_tag):
        search_notes = {}
        for key, val in self.data.items():
            if search_tag in val.tags:
                search_notes.update({key: val})
        return search_notes

    def change_note(self, note):
        for key, val in self.data.items():
            if key.lower() == note.lower():
                return {key: val}
        return False

    def delete(self, del_title):
        for title in self.data.keys():
            if title == del_title:
                self.data.pop(title)
                return True
        return False

    def __str__(self):
        return f" Title: {self.title}\n Tags:{self.tags}\n Description: {self.description}"
