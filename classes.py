import pickle
from datetime import datetime
from collections import UserDict

class Field:
    def __init__(self, value) -> None:
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value


class Name(Field):
    def __init__(self, name: str):
        self.value = name

    @Field.value.setter
    def value(self, name):
        if not name.isalpha():
            raise ValueError
        Field.value.fset(self, name)

    def __repr__(self) -> str:
        return f"Name({self.value})"


class Phone(Field):
    def __init__(self, value) -> None:
        super().__init__(value)

    def is_valid_phone(self):
        return len(self.value) == 10 and self.value.isdigit()
    
    def __repr__(self) -> str:
        return f"Phone({self.value})"


class Email(Field):
    def __init__(self, value) -> None:
        super().__init__(value)

    def __repr__(self) -> str:
        return f"Email({self.value})"


class Birthday(Field):
    def __init__(self, birthday):
        self.value = birthday

    @Field.value.setter
    def value(self, birthday):
        try:
            dt = datetime.strptime(birthday, '%d.%m.%Y')
        except (ValueError, TypeError):
            raise ValueError
        Field.value.fset(self, dt.date())

    def __repr__(self) -> str:
        return f"Birthday({self.value})"


class Record:
    def __init__(
        self,
        name: Name,
        phone: Phone | str | None = None,
        email: Email | str | None = None,
        birthday: Birthday | None = None
    ):
        self.name = name
        self.birthday = birthday

        self.phones = []
        if phone is not None:
            self.add_phone(phone)

        self.emails = []
        if email is not None:
            self.add_email(email)

    def add_phone(self, phone: Phone | str):
        if isinstance(phone, str):
            phone = self.create_phone(phone)
        self.phones.append(phone)

    def add_email(self, email: Email | str):
        if isinstance(email, str):
            email = self.create_email(email)
        self.emails.append(email)

    def add_birthday(self, birthday: Birthday | str):
        if isinstance(birthday, str):
            birthday = self.create_birthday(birthday)
        self.birthday = birthday

    def create_phone(self, phone: str):
        return Phone(phone)

    def create_email(self, email: str):
        return Email(email)

    def create_birthday(self, birthday: str):
        return Birthday(birthday)

    def edit_phone(self, old_phone, new_phone):
        for p in self.phones:
            if p.value == old_phone:
                p.value = new_phone
                return p

    def edit_email(self, old_email, new_email):
        for e in self.emails:
            if e.value == old_email:
                e.value = new_email
                return e

    def show(self):
        for inx, p in enumerate(self.phones):
            print(f'{inx}: {p.value}') 

    def get_phone(self, inx):
        if self.phones:
            return self.phones[inx]
        else:
            return None

    def get_name(self):
        return self.name.value

    def get_email(self, indx):
        if self.emails and indx < len(self.emails):
            return self.emails[indx]
        else:
            return None

    def get_birthday(self):
        return self.birthday

    def days_to_birthday(self):
        if self.birthday:
            today = datetime.today().date()
            next_birthday = datetime(today.year, self.birthday.value.month, self.birthday.value.day).date()
            if today > next_birthday:
                next_birthday = datetime(today.year + 1, self.birthday.value.month, self.birthday.value.day).date()
            days_left = (next_birthday - today).days
            return days_left
        else:
            return "No birthday set"

    def __str__(self) -> str:
        return f"name: {self.name}: phones: {self.phones} emails: {self.emails} birthday: {self.birthday}"

    def __repr__(self) -> str:
        return f"Record({self.name!r}: {self.phones!r}, {self.emails!r}, {self.birthday!r})"


class AddressBook(UserDict):
    def __init__(self, record: Record | None = None) -> None:
        self.data = {}
        if record is not None:
            self.add_record(record)

    def add_record(self, record: Record):
        self.data[record.get_name()] = record

    def show(self):
        for name, record in self.data.items():
            print(f'{name}:')
            record.show()

    def get_records(self, name: str) -> Record:
        try:
            return self.data[name]
        except KeyError:
            return None

    def save_to_file(self, filename):
        with open(filename, 'wb') as file:
            pickle.dump(self.data, file)

    def load_from_file(self, filename):
        try:
            with open(filename, 'rb') as file:
                self.data = pickle.load(file)
        except FileNotFoundError:
            pass

    def __iter__(self):
        return iter(self.data.values())

    def __next__(self):
        if self._iter_index < len(self.data):
            record = list(self.data.values())[self._iter_index]
            self._iter_index += 1
            return record
        else:
            raise StopIteration