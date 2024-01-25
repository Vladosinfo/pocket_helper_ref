from src.classes.field import Field
import src.classes.exceptions as ex
from time import strptime


class Birthday(Field):
    def __init__(self, value):
        self._value = None
        self.value = value
        super().__init__(self._value)

    @property
    def value(self):
        return self._value

    @Field.value.setter
    def value(self, value):
        if value is None:
            self._value = None
        else:
            try:
                strptime(value, '%d-%m-%Y')
                self._value = value
            except ValueError:
                raise ex.NotCorrectData
