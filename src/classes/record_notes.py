class RecordNotes():
    def __init__(self, title, description, tags=None):
        self._tags = tags.split(" ") if (tags is not None and tags != "") else None
        self._title = None
        self._description = None
        self.title = title
        self.description = description
        self.tags = title + " " + description

    @property
    def title(self):
        return self._title

    @property
    def description(self):
        return self._description

    @property
    def tags(self):
        return self._tags

    @title.setter
    def title(self, title):
        self._title = title.replace("#", "")

    @description.setter
    def description(self, description):
        self._description = description.replace("#", "")

    @tags.setter
    def tags(self, tags):
        # tags_from_text = []
        tags_from_text = self._tags or []
        # tags_from_text = set()
        substring = '#'
        substrings = tags.split(substring)

        if len(tags) > 0:
            for item in substrings[1:]:
                temp_arr = item.split(" ")
                tag = temp_arr[0].removesuffix('.').removesuffix(',').lower().strip()
                if not tag in tags_from_text:
                    tags_from_text.append(tag)
                # tags_from_text.add(temp_arr[0].removesuffix('.').removesuffix(',').lower().strip())
                # tags_from_text.discard("some tag") # For delete from unic collection
                continue
        self._tags = tags_from_text

    def __str__(self):
        return f" Title: {self.title}\n Tags:{self.tags}\n Description: {self.description}\n{'-'*50}"
