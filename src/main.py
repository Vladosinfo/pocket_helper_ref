import src.address_book_lib as abl
import src.notes_book_lib as nbl
from src.classes.record_notes import RecordNotes
import src.messages_settings as message
import src.classes.exceptions as ex
import src.helpers.general_helpers as helpeer
import src.helpers.serialization as serialize
from src import clean_lib
from src.messages_settings import (MESSAGES, EXIT_COMMANDS, WARNING_MESSAGES, COMMAND_HANDLER_DESCRIPTION,)
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit import prompt

contacts_book = abl.AddressBook()
notes_book = nbl.NotesBook()

RED = "\033[91m"
GREEN = "\033[92m"
BOLD = "\033[1m"
RESET = "\033[0m"


def message_notice(notice, color=None):
    color = color or GREEN
    return f"{color}{notice} {RESET}"


def message_warging(warning):
    return f"{RED} {warning} {RESET}"


def output_message(message):
    print(message)


def input_error(func):
    def wrapper(user_input):
        try:
            return func(user_input)
        except KeyError as err:
            return message_warging(f"Error: {err}")
        except ValueError as err:
            return message_warging(f"Error: {err}")
        except IndexError as err:
            return message_warging(f"Error: {err}")
        except ex.NotCorrectData as err:
            return message_warging(f"Error: {WARNING_MESSAGES['not_correct_data']}")
        except ex.NotCorrectPhoneIsNotANumber as err:
            return message_warging(f"Error: {WARNING_MESSAGES['not_correct_phone_is_not_a_number']}")
        except ex.NotCorrectPhoneIsTwoShortOrLong as err:
            return message_warging(f"Error: {WARNING_MESSAGES['not_correct_phone_short_long']}")
    return wrapper


def message(mes):
    return message_notice(MESSAGES[mes[0]])


def exit(mes):
    return message_notice(mes)


@input_error
def error(err):
    raise ValueError(WARNING_MESSAGES["correct_command"])


@input_error
def add(com):
    count = len(com)
    if count < 3:
        raise ValueError(WARNING_MESSAGES["name_phone"])
    record_is = contacts_book.find(com[1])
    if record_is is None:
        if count > 3:
            record = abl.Record(com[1], com[2])
            record.add_phone(com[3])
        else:
            record = abl.Record(com[1])
            record.add_phone(com[2])
        contacts_book.add_record(record)
        return message_notice(MESSAGES[com[0]])
    else:
        record_is.add_phone(com[2])
        contacts_book.add_record(record_is)
        return message_notice(MESSAGES[com[0] + "_more"])


def contacts_book_fullness():
    if len(contacts_book) == 0:
        return message_warging(WARNING_MESSAGES["contacts_book_empty"])
    else:
        return 1


def presence_name(com):
    contact = contacts_book.find(com[1])
    if contact is None:
        raise ValueError(WARNING_MESSAGES["missing_name"])
    else:
        return contact


def show_all(com, search=None):
    if search is not None:
        iter_Item = search
        message = "show_found"
    else:
        cont = contacts_book_fullness()
        if cont != 1:
            return cont
        iter_Item = contacts_book
        message = com
    contacts = message_notice(MESSAGES[message])
    for val in iter_Item.values():
        contacts += "\n" + message_notice(f"{val}", BOLD)
    return contacts


@input_error
def phone(com):
    cont = contacts_book_fullness()
    if cont != 1:
        return cont
    if len(com) < 2:
        raise ValueError(WARNING_MESSAGES["find"])
    name_is = presence_name(com)
    if name_is is not None:
        return message_notice(f"{MESSAGES[com[0]]}{contacts_book[com[1]]}", BOLD)


@input_error
def change(com):
    if len(com) < 4:
        raise ValueError(WARNING_MESSAGES["change_phone"])
    name_is = presence_name(com)
    if name_is is not None:
        name_is.edit_phone(com[2], com[3])
        return message_notice(MESSAGES[com[0]])


@input_error
def change_birth(com):
    if len(com) < 3:
        raise ValueError(WARNING_MESSAGES["name_birth"])
    birth_is = presence_name(com)
    if birth_is:
        birth_is.edit_birthday(com[2])
        return message_notice(MESSAGES[com[0]])
    else:
        raise ValueError(WARNING_MESSAGES["missing_name"])


@input_error
def iter(com):
    contacts_book.list_creator()
    count = len(com)
    if count == 3:
        items = contacts_book.iterator(int(com[1]), int(com[2]))
    else:
        items = contacts_book.iterator()
    if items is not None:
        contacts = ""
        contacts += message_notice(MESSAGES[com[0]])
        for item in items:
            contacts += "\n" + message_notice(f"{item}", BOLD)
        return contacts
    else:
        return message_warging(WARNING_MESSAGES["iter_no_result"])


@input_error
def delete(com):
    res = contacts_book.find(com[1])
    if res is None:
        return message_warging(WARNING_MESSAGES["missing_name"])
    else:
        contacts_book.delete(com[1])
        return message_notice(MESSAGES["delete_contact"], GREEN)


@input_error
def search(com):
    if len(com) < 2:
        raise ValueError(WARNING_MESSAGES["search_cont"])
    res = contacts_book.search(com[1])
    if res != 0:
        return show_all("show_all", res)
    else:
        return message_warging(WARNING_MESSAGES["show_found_empty"])


@input_error
def daysbir(com):
    contact = contacts_book.find(com[1])
    if contact is None:
        return message_warging(WARNING_MESSAGES["missing_name"])
    else:
        res = contact.days_to_birthday()
        return message_notice(f"{res}", BOLD)


@input_error
def add_address(com):
    if len(com) < 2:
        raise ValueError(WARNING_MESSAGES["name_address"])
    record_is = presence_name(com)
    if record_is is not None and isinstance(record_is, abl.Record):

        address = input("\tInput address >>> ")
        address = address.strip()

        record_is.set_address(address)
        contacts_book.add_record(record_is)
        return message_notice(MESSAGES["added_address"])
    else:
        return message_warging(WARNING_MESSAGES["missing_address"])


@input_error
def add_email(com):
    if len(com) < 3:
        raise ValueError(WARNING_MESSAGES["name_email"])

    record_is = presence_name(com)
    if record_is is not None and isinstance(record_is, abl.Record):
        record_is.set_email(com[2])
        contacts_book.add_record(record_is)
        return message_notice(MESSAGES["add_email"])
    else:
        return message_warging(WARNING_MESSAGES["missing_name"])


def birthdays(com, days=7):
    search_days = int(com[1]) if len(com) > 1 else days
    res = ""
    for item in contacts_book.values():
        if item.date.value is not None:
            days_count = helpeer.list_days_to_birthday(item.date.value)
            if days_count <= search_days:
                res += message_notice(f"{item.name.value.title()} after {days_count} day(s)\n", BOLD)
    if res != "":
        return message_notice(MESSAGES["list_days_to_birthday"] + "\n", GREEN) + res
    else:
        return message_warging(WARNING_MESSAGES["no_list_days_to_birthday"])


@input_error
def add_note(com):
    title = input("\tInput title note >>> ")
    desc = input("\tInput description note >>> ")
    note_title = title.strip()
    note_desc = desc.strip()
    note_record = RecordNotes(note_title, note_desc)
    res = notes_book.add_record(note_record)
    return res


@input_error
def show_all_notes(can):
    notes = message_notice(f"{MESSAGES['list_notes']}", GREEN)
    for val in notes_book.values():
        notes += "\n" + message_notice(f"{val}", BOLD)
    return notes


@input_error
def search_note(com):
    if len(com) < 2:
        raise ValueError(WARNING_MESSAGES["search_note"])
    search_notes = notes_book.search(com[1])
    if len(search_notes) > 0:
        notes = message_notice(f"{MESSAGES['list_notes_by_string']} - '{com[1]}':", GREEN)
        for val in search_notes.values():
            notes += "\n" + message_notice(f"{val}", BOLD)
    else:
        notes = message_notice(f"{MESSAGES['list_notes_by_string']} - '{com[1]}': is empty.", GREEN)
    return notes


@input_error
def search_notes_by_tag(com):
    if len(com) < 2:
        return message_warging(WARNING_MESSAGES["search_note_by_tag_id_empty"])

    search_notes = notes_book.search_by_tag(com[1])
    if len(search_notes) > 0:
        notes = message_notice(f"{MESSAGES['list_notes_by_tag']} - '{com[1]}':", GREEN)
        for val in search_notes.values():
            notes += "\n" + message_notice(f"{val}", BOLD)
    else:
        notes = message_notice(f"{MESSAGES['list_notes_by_tag']} - '{com[1]}': is empty.", GREEN)
    return notes


@input_error
def change_note(com):
    note_for_change = input('\tEnter note that you want to change: >>> ')
    search_res = notes_book.change_note(note_for_change)
    if search_res is False:
        return f"Note: '{note_for_change}', was not found."
    else:
        current_key = ""
        current_title = ""
        current_description = ""
        current_tags = ""
        for key, val in search_res.items():
            current_key = key
            current_title = val.title
            current_description = val.description
            current_tags = val.tags
        output_message(message_notice(f"{MESSAGES['change_notes_note_add_tag1']}", GREEN))
        output_message(message_notice(f"{MESSAGES['change_note_current_title']} {current_title}"))
        title_note_for_change = input("\tEnter new title for change: >>> ")

        output_message(message_notice(f"{MESSAGES['change_notes_note_add_tag2']}", GREEN))
        output_message(message_notice(f"{MESSAGES['change_note_current_description']} {current_description}"))
        description_note_for_change = input("\tEnter new description for change: >>> ")

        output_message(message_notice(f"{MESSAGES['change_notes_note_add_tag3']}", GREEN))
        output_message(message_notice(f"{MESSAGES['change_note_current_tags']} {current_tags}"))
        tags_note_for_change = input(f"\t{MESSAGES['change_note_input_tags']} >>> ")
        notes_book.delete(current_key)
        note_record = RecordNotes(title_note_for_change, description_note_for_change, tags_note_for_change)
        output_message(message_notice(f"{MESSAGES['changed_note']}", GREEN))
        res = notes_book.add_record(note_record)
    return res


@input_error
def delete_note(com):
    title = input("\tInput title that you want to delete: >>> ")
    res = False
    if title != "":
        res = notes_book.delete(title)
    return f"Notes: '{title}', has been successfully removed." if res else f"Notes: '{title}', was not found."


@input_error
def help(com):
    res = ""
    for command in COMMAND_HANDLER.keys():
        res += message_notice(f"Command: {command}", GREEN)
        res += message_notice(f"- description: {COMMAND_HANDLER_DESCRIPTION[command]}\n", BOLD)
    return res


def clean_dir(com):
    res = ""
    clean_lib.sort_files(False)
    return res


COMMAND_HANDLER = {
    "hello": message,
    "add_contact": add,
    "add_note": add_note,
    "add_email": add_email,
    "add_address": add_address,
    "change_phone": change,
    "change_birth": change_birth,
    "change_email": add_email,
    "change_address": add_address,
    "clean_dir": clean_dir,
    "find_contact": phone,
    "show all": show_all,
    "show_all_notes": show_all_notes,
    "iter_contacts": iter,
    "search_contact": search,
    "search_note": search_note,
    "search_notes_by_tag": search_notes_by_tag,
    "change_note": change_note,
    "delete_note": delete_note,
    "delete_contact": delete,
    "daysbir": daysbir,
    "birthdays": birthdays,
    "help": help,
    "exit": message,
    "close": message,
    "good bye": message
}


def command_handler(com):
    handler = COMMAND_HANDLER.get(com[0], error)
    return handler(com)


@input_error
def parsing(user_input):
    if user_input.startswith("show all"):
        return show_all("show_all")
    elif user_input.startswith("add_email"):
        return add_email(user_input.split(" "))
    elif user_input.startswith("add_note"):
        return add_note("add_note")
    elif user_input.startswith("show_all_notes"):
        return show_all_notes(user_input.split(" "))
    elif user_input.startswith("search_notes_by_tag"):
        return search_notes_by_tag(user_input.split(" "))
    elif user_input.startswith("search_note"):
        return search_note(user_input.split(" "))
    elif user_input.startswith("change_note"):
        return change_note(user_input.split(" "))
    elif user_input.startswith("delete_note"):
        return delete_note(user_input.split(" "))
    elif user_input.startswith("add_address"):
        return add_address(user_input.split(" "))
    else:
        return command_handler(user_input.split(" "))


# Completer for commands
command_completer = WordCompleter(COMMAND_HANDLER.keys(), ignore_case=True)


def main():
    serialization_full_data = serialize.Serialization().unserialization()
    full_content = serialization_full_data.get('full_content')
    if full_content is not None:
        contacts_book.data = full_content.get("contacts")
        notes_book.data = full_content.get("notes")

    print(message_notice(MESSAGES["text_before_start"], GREEN))
    while True:
        # user_input = input("Input command >>> ")
        user_input = prompt(">>> ", completer=command_completer)
        user_input = user_input.strip().lower()
        if user_input in EXIT_COMMANDS:
            print(exit(MESSAGES[user_input]))
            ob_serialize = serialize.Serialization()
            ob_serialize.serialization(contacts_book.data, notes_book)
            break
        res = parsing(user_input)
        print(res)


if __name__ == "__main__":
    main()
