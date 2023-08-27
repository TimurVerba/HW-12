from collections import UserDict
import datetime
import pickle

class Field:

    def __init__(self, value) -> None:
        self.__value = None
        self.value = value

    @staticmethod
    def valid_value(value) -> bool:
        if value:
            return True
        return False

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, val):
        if self.valid_value(val):
            self.__value = val


class Phone(Field):
    @staticmethod
    def validate_value(self, value):
        if not value.isdigit():
            raise ValueError("Phone number must consist of digits only.")
        return value


class Name(Field):
   pass


class Birthday(Field):
    @staticmethod
    def validate_value(self, value):
        try:
            parsed_birthday = datetime.datetime.strptime(value, '%Y-%m-%d').date()
        except ValueError:
            raise ValueError("Invalid birthday format. Use 'YYYY-MM-DD'.")
        return parsed_birthday

class Record:
    def __init__(self, name: Name, phone: Phone = None, birthday: Birthday = None) -> None:
        self.name = name
        self.phones = []
        self.birthday = birthday

        if phone:
            self.add_phone(phone)

    def add_phone(self, phone: Phone) -> None:
        self.phones.append(phone)

    def remove_phone(self, phone: Phone) -> None:
        for already_existing_phones in self.phones:
            if phone.value == already_existing_phones:
                self.phones.remove(already_existing_phones)
                break

    def edit_phone(self, old_phone: Phone, new_phone: Phone):
        index = self.phones.index(old_phone)
        self.phones[index] = new_phone

    def days_to_birthday(self):
        if not self.birthday:
            return None

        today = datetime.date.today()
        next_birthday = datetime.date(today.year, self.birthday.value.month, self.birthday.value.day)

        if next_birthday < today:
            next_birthday = datetime.date(today.year + 1, self.birthday.value.month, self.birthday.value.day)

        difference = next_birthday - today
        return difference.days


class AddressBook(UserDict):
    def __init__(self, filename="address_book.pkl"):
        super().__init__()
        self.current_index = 0
        self.filename = filename

    def save(self):
        with open(self.filename, "wb") as file:
            pickle.dump(self.data, file)

    def load(self):
        try:
            with open(self.filename, "rb") as file:
                self.data = pickle.load(file)
        except FileNotFoundError:
            pass

    def search(self, search_str: str):
        result = []
        for record_id, record in self.data.items():
            if search_str in record.name.value:
                result.append(record)
            else:
                for phone in record.phones:
                    if search_str in phone.value:
                        result.append(record)
                        break
        return result

    def add_record(self, record: Record) -> None:
        self.data[record.name.value] = record

    def find_record(self, value):
        for record in self.data.values():
            if value == record.name.value:
                return record
            for phone in record.phones:
                if value == phone.value:
                    return record
        return None

    def __iter__(self):
        return self

    def __next__(self, page_size=10):
        record_values = list(self.data.values())
        if self.current_index >= len(record_values):
            self.current_index = 0
            raise StopIteration

        current_page = record_values[self.current_index: self.current_index + page_size]
        self.current_index += page_size
        return current_page

if __name__ == '__main__':
    ab = AddressBook()
    ab.load()

    name1 = Name('Eva')
    phone1 = Phone('380996602558')
    birthday1 = Birthday(datetime.date(2000, 7, 21))
    rec1 = Record(name1, phone1, birthday1)

    name2 = Name('Hannah')
    phone2 = Phone('380667238934')
    birthday2 = Birthday(datetime.date(1995, 10, 15))
    rec2 = Record(name2, phone2, birthday2)

    ab.add_record(rec1)
    ab.add_record(rec2)

    assert isinstance(ab['Eva'], Record)
    assert isinstance(ab['Eva'].name, Name)
    assert isinstance(ab['Eva'].phones, list)
    assert isinstance(ab['Eva'].phones[0], Phone)
    assert ab['Eva'].phones[0].value == '380996602558'
    found_record = ab.find_record('380996602558')
    assert found_record is rec1

    print("Iterating through the address book:")
    address_book_iterator = iter(ab)
    while True:
        try:
            page = next(address_book_iterator)
            for record in page:
                print(record.name.value)
        except StopIteration:
            break

    print("Days to Eva's birthday:", rec1.days_to_birthday())
    print("Days to Hannah's birthday:", rec2.days_to_birthday())

    ab.save()

    print('Done')
