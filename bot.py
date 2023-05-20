from classes import Record, AddressBook, Name, Email, Birthday, Phone

phonebook = AddressBook()


def input_error(func):
    def inner(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except KeyError:
            return "There is no such name"
        except ValueError:
            return "Give me name and phone/email/birthday please"
        except IndexError:
            return "Enter user name"
        except TypeError:
            return "Incorrect values"
    return inner


@input_error
def greeting():
    return "How can I help you?"


def unknown_command():
    return "Unknown command"


@input_error
def exit():
    return None


@input_error
def add_user(name, contact_details):
    record = phonebook.get_records(name)
    if record:
        return update_user(record, contact_details)
    else:
        if '@' in contact_details:
            record = Record(Name(name), email=Email(contact_details))
        elif '.' in contact_details:
            record = Record(Name(name), birthday=Birthday(contact_details))
        else:
            phone = Phone(contact_details)
            if phone.is_valid_phone():
                record = Record(Name(name), phone=phone)
                phonebook.add_record(record)
                return "Contact successfully added"
            else:
                return "Invalid phone number format"
        phonebook.add_record(record)
        return "Contact successfully added"
        

def update_user(record, contact_details):
    if '@' in contact_details:
        record.add_email(Email(contact_details))
    elif '.' in contact_details:
        record.add_birthday(Birthday(contact_details))
    else:
        phone = Phone(contact_details)
        if phone.is_valid_phone():
            record.add_phone(phone)
        else:
            return "Invalid phone number format"
    return "Contact details added successfully"  


@input_error
def change_phone(name, new_phone, index=0):
    record = phonebook.get_records(name)
    if record:
        if record.phones and '0' <= str(index) < str(len(record.phones)):
            record.edit_phone(old_phone=record.phones[int(index)].value, new_phone=new_phone)
            return "Phone number updated successfully"
        else:
            return "Invalid phone number index"
    else:
        return "There is no such name"


@input_error
def show_all():
    if not phonebook.data:
        return "The phonebook is empty"
    result = ''
    for name, record in phonebook.data.items():
        result += f'{name}:'
        if record.phones:
            phones = ', '.join([phone.value for phone in record.phones])
            result += f' phones: {phones}'
        if record.emails:
            emails = ', '.join([email.value for email in record.emails])
            result += f' emails: {emails}'
        if record.birthday:
            result += f' birthday: {record.birthday.value}'
            days_left = record.days_to_birthday()
            result += f' days to birthday: {days_left}'
        result += '\n'
    return result.rstrip()


@input_error
def get_birthday(name):
    record = phonebook.get_records(name)
    if record:
        if record.birthday:
            return f"{record.name.value}: {record.birthday.value}, Days to birthday: {record.days_to_birthday()}"
        else:
            return "No birthday found for that name"
    else:
        return "There is no such name"


def get_phone_number(name):
    record = phonebook.get_records(name)
    if record:
        phones = [f"{record.get_name()}: {phone}" for phone in record.phones]
        result = "\n".join(phones)
        return result
    else:
        return "There is no such name"


@input_error
def get_email(name):
    record = phonebook.get_records(name)
    if record:
        result = f"{record.get_name()}: {record.get_email(0)}"
        return result
    else:
        return "There is no such name"


@input_error
def search_by_criteria(criteria):
    if criteria:
        result = []
        for record in phonebook.data.values():
            if criteria in record.get_name():
                result.append(record)
            elif record.get_email(0) and criteria in record.get_email(0).value:
                result.append(record)
            elif any(criteria in phone.value for phone in record.phones):
                result.append(record)
            
        if result:
            result_strings = []
            for record in result:
                contact_info = f"{record.get_name()}"
                if record.phones:
                    phones = ", ".join([phone.value for phone in record.phones])
                    contact_info += f": {phones}"
                if record.get_email(0):
                    contact_info += f", Email: {record.get_email(0).value}"
                if record.get_birthday():
                    contact_info += f", Birthday: {str(record.get_birthday().value)}"
                    days_left = record.days_to_birthday()
                    contact_info += f", Days to birthday: {days_left}"
                result_strings.append(contact_info)
            return "\n".join(result_strings)

    return "No records found for that criteria"


@input_error
def iteration(page=1, page_size=3):
    if not phonebook.data:
        return "The phonebook is empty"

    page = int(page)
    page_size = int(page_size)
    start_index = (page - 1) * page_size
    end_index = start_index + page_size

    records = list(phonebook)
    total_pages = (len(records) + page_size - 1) // page_size

    if page < 1 or page > total_pages:
        return f"Invalid page number. Please enter a page number between 1 and {total_pages}"

    result = ""
    for record in records[start_index:end_index]:
        result += f"{record}\n"

    result += f"Page {page}/{total_pages}"

    return result.rstrip()


commands = {
    'hello': greeting,
    'add': add_user,
    'change': change_phone,
    'show all': show_all,
    "phone": get_phone_number,
    'exit': exit,
    'good bye': exit,
    'close': exit,
    "email": get_email,
    "birthday": get_birthday,
    'search': search_by_criteria,
    "page": iteration,
}

filename = "address_book.txt"

def main():
    phonebook.load_from_file(filename)
    while True:
        command, *args = input(">>> ").strip().lower().split(' ')
        if commands.get(command):
            handler = commands.get(command)
            if args:
                result = handler(*args)
            else:
                result = handler()
        elif args and commands.get(command + ' ' + args[0]):
            command = command + ' ' + args[0]
            args = args[1:]
            handler = commands.get(command)
            result = handler(*args)
        else:
            result = unknown_command()
        if not result:
            print('Goodbye!')
            phonebook.save_to_file(filename)
            break
        print(result)


if __name__ == "__main__":
    main()