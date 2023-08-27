from address_book import AddressBook, Name, Phone, Birthday, Record
import datetime

if __name__ == '__main__':
    ab = AddressBook()
    ab.load()

    for record in ab.data.values():
        print("Name:", record.name.value)
        print("Phones:", [phone.value for phone in record.phones])
        if record.birthday:
            print("Birthday:", record.birthday.value)
        print()

    print('Done')

