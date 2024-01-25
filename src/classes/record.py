from datetime import date, datetime
from src.classes.name import Name
from src.classes.phone import Phone
from src.classes.birthday import Birthday
from src.classes.exceptions import NotCorrectData
from src.classes.address import Address
from src.classes.email import Email


class Record():
    def __init__(self, name, date=None, email=None, address=None):
        self.name = Name(name)  # Mandatory
        self.phones = []
        self.date = Birthday(date)
        self.email = Email(email) if email is not None else None
        self.address = Address(address)

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def days_to_birthday(self):
        if self.date.value is not None:
            today = date.today()
            bdat = datetime.strptime(self.date.value, '%d-%m-%Y')
            birthday = datetime(
                year=today.year, month=bdat.month, day=bdat.day)
            curdat = datetime(
                year=today.year, month=today.month, day=today.day)
            count = (curdat - birthday).days
            count = count if count > 0 else abs(count)
            return f"{count} days left to birthday."
        else:
            return "Birthday data is misssing."

    def edit_phone(self, phone, phone_new):
        # phone_obj = self.find_phone(phone)
        phone_obj: Phone = self.find_phone(phone)
        if phone_obj and phone_obj.validate(phone_new):
            phone_obj.value = phone_new
        else:
            raise ValueError("Not correct phone number. Check by command 'show all'")

    def edit_birthday(self, new_birth):
        try:
            self.date.value = new_birth
        except NotCorrectData:
            raise ValueError("Not correct data. Example: 21-12-2021")

    def remove_phone(self, phone_r):
        p_obj = self.find_phone(phone_r)
        if p_obj:
            self.phones.remove(p_obj)

    def set_email(self, email):
        self.email = Email(email)

    def find_phone(self, phone_f):
        for phone in self.phones:
            if phone.value == phone_f:
                return phone

    def set_address(self, address):
        self.address.value = address

    def __str__(self):
        str_dat = f"; birthday: {self.date.value}" if self.date.value is not None else ""
        str_email = f"; email: {self.email.value}" if self.email is not None and self.email.value is not None else ""
        str_address = f"; address: {self.address.value}" if self.address.value is not None else ""
        return f"Name: {self.name.value.title()}; phones: {'; '.join(p.value for p in self.phones)}{str_dat}{str_email}{str_address}"
