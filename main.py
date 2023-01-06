from validation import *
from api_fetch import *
from book_list import *
from book import *
from read_list import *
from console import *
from file import *


def main():
    """ Creates any necessary objects and calls functions to execute the program's logic. """
    load_reading_list()

    Console.print_string("Hello friend! This is a program that searches for books using the Google Books API.\n"
                           "It returns a list of matches you can select from to save to a reading list file. Enjoy!")
    select_from_menu()

def load_reading_list():
    """ Creates reading file if none exists. """
    try:
        File().read_file()
    except:
        File().create_file()

def select_from_menu():
    """ Gets user's menu choice and selects menu choice. """
    menu_choice = Console.select_menu_option()
    if not Validation.validate_menu_choice(menu_choice):
        Console.print_string("Oops! This is an invalid menu choice. ")
        select_from_menu()

    if menu_choice == "s":
        search_books()
        select_from_menu()
    if menu_choice == "r":
        File().print_file()
        select_from_menu()
    if menu_choice == "x":
        Console.print_string("Okay. Goodbye!")

def search_books():
    """ Searches books for user's search term. """
    api_search = APIFetch()
    api_search.search()

    if api_search.search_results:
        book_list = create_book_list(api_search.search_results)
        ask_to_add_book_to_reading_list(book_list)
    else:
        ask_to_search_again()

def create_book_list(search_results):
    """ Creates list of books matching user's search term. """
    book_list = BookList(search_results)
    book_dictionary = book_list.create_book_list()
    Console.print_book_list(book_dictionary)
    return book_list


def ask_to_search_again():
    """ Asks user if they would like to search again. """
    search_again = Console.prompt_yn(
        "Would you like to search again?(y/n): ")

    if not Validation.validate_bool(search_again):
        Console.print_string("Sorry! This is an invalid choice. ")
        ask_to_search_again()

    if search_again == "y":
        search_books()

def ask_to_add_book_to_reading_list(book_list, first=True):
    """ Asks user if they would like to add a book to their reading list. """
    a = "a" if first else "another"

    add_book = Console.prompt_yn(
        f"Would you like to add {a} book to your reading list?(y/n): ")

    if not Validation.validate_bool(add_book):
            Console.print_string("Sorry! This is an invalid choice. ")
            ask_to_add_book_to_reading_list(book_list)

    if add_book == "y":
        add_to_reading_list(book_list)

def add_to_reading_list(book_list):
    """ Adds selected book to user's reading list. """
    books = ReadList(book_list)
    books.create_list()
    ask_to_add_book_to_reading_list(book_list, False)

if __name__ == "__main__":
    main()









