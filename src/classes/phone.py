from src.classes.field import Field
import src.classes.exceptions as ex


class Phone(Field):
    def __init__(self, value):
        self._value = None
        self.value = value
        super().__init__(self._value)

    @property
    def value(self):
        return self._value

    @Field.value.setter
    def value(self, phone):
        numeric_phone = ''.join(filter(str.isdigit, phone))
        if numeric_phone.isdigit():
            if len(numeric_phone) == 9:
                self._value = f"+380{numeric_phone}"
            elif len(numeric_phone) == 10:
                self._value = f"+38{numeric_phone}"
            elif 10 < len(numeric_phone) <= 13:
                self._value = f"+{numeric_phone}"
            else:
                raise ex.NotCorrectPhoneIsTwoShortOrLong
        else:
            raise ex.NotCorrectPhoneIsNotANumber

    def validate(self, phone):
        numeric_phone = ''.join(filter(str.isdigit, phone))
        if numeric_phone.isdigit():
            if len(numeric_phone) == 13:
                return True
            elif len(numeric_phone) == 9 or 10 <= len(numeric_phone) <= 13:
                return True
        return False
