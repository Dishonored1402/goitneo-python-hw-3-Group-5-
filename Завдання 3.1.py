from datetime import datetime, timedelta

class Birthday:
    def __init__(self, date_str):
        self.date = self._parse_date(date_str)

    def _parse_date(self, date_str):
        try:
            return datetime.strptime(date_str, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Invalid date format. Please use DD.MM.YYYY.")

    def __str__(self):
        return self.date.strftime("%d.%m.%Y")

class Record:
    def __init__(self, name, phone, birthday=None):
        self.name = name
        self.phone = self._validate_phone(phone)
        self.birthday = birthday

    def _validate_phone(self, phone):
        if not phone.isdigit() or len(phone) != 10:
            raise ValueError("Invalid phone number. Please use 10 digits.")
        return phone

class AddressBook:
    def __init__(self):
        self.contacts = {}

    def add_contact(self, name, phone, birthday=None):
        if name in self.contacts:
            raise KeyError(f"Contact {name} already exists.")
        
        contact = Record(name, phone, birthday)
        self.contacts[name] = contact

    def change_phone(self, name, new_phone):
        contact = self._get_contact(name)
        contact.phone = contact._validate_phone(new_phone)

    def get_phone(self, name):
        contact = self._get_contact(name)
        return contact.phone

    def show_all_contacts(self):
        return "\n".join(f"{contact.name}: {contact.phone}" for contact in self.contacts.values())

    def add_birthday(self, name, birthday_str):
        contact = self._get_contact(name)
        contact.birthday = Birthday(birthday_str)

    def show_birthday(self, name):
        contact = self._get_contact(name)
        return f"{contact.name}'s birthday: {contact.birthday}"

    def get_birthdays_per_week(self):
        today = datetime.now().date()
        next_week = today + timedelta(days=7)
        upcoming_birthdays = [
            f"{contact.name}: {contact.birthday}"
            for contact in self.contacts.values()
            if contact.birthday and today < contact.birthday.date <= next_week
        ]
        return upcoming_birthdays

    def _get_contact(self, name):
        contact = self.contacts.get(name)
        if not contact:
            raise KeyError(f"Contact {name} not found.")
        return contact

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as ve:
            return str(ve)
        except KeyError as ke:
            return str(ke)
        except Exception as e:
            return f"An error occurred: {e}"

    return inner

book = AddressBook()

@input_error
def handle_add(args):
    name, phone = args
    book.add_contact(name, phone)
    return "Contact added."

@input_error
def handle_change(args):
    name, new_phone = args
    book.change_phone(name, new_phone)
    return "Phone number changed."

@input_error
def handle_phone(args):
    name = args[0]
    return book.get_phone(name)

@input_error
def handle_all(args):
    return book.show_all_contacts()

@input_error
def handle_add_birthday(args):
    name, birthday_str = args
    book.add_birthday(name, birthday_str)
    return "Birthday added."

@input_error
def handle_show_birthday(args):
    name = args[0]
    return book.show_birthday(name)

@input_error
def handle_birthdays(args):
    return "\n".join(book.get_birthdays_per_week())

while True:
    command = input("Enter command: ").lower().split()
    
    if command[0] in ["close", "exit"]:
        break

    if command[0] == "add":
        result = handle_add(command[1:])
    elif command[0] == "change":
        result = handle_change(command[1:])
    elif command[0] == "phone":
        result = handle_phone(command[1:])
    elif command[0] == "all":
        result = handle_all(command[1:])
    elif command[0] == "add-birthday":
        result = handle_add_birthday(command[1:])
    elif command[0] == "show-birthday":
        result = handle_show_birthday(command[1:])
    elif command[0] == "birthdays":
        result = handle_birthdays(command[1:])
    else:
        result = "Invalid command. Please enter a valid command."

    print(result)
