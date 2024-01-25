import re
from src.classes.field import Field


class Email(Field):
    def __init__(self, email):
        self._value = None
        self.value = email
        super().__init__(self._value)

    @property
    def value(self):
        return self._value

    @Field.value.setter
    def value(self, email):
        if self.validate(email):
            self._value = email
        else:
            raise ValueError("Invalid email format")

    def validate(self, email):
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(email_regex, email) is not None
