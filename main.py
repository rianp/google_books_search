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
    while True:
        select_from_menu()

    Console.print_string("Okay. Goodbye!")

def load_reading_list():
    try:
        File().read_file()
    except:
        File().create_file()

def select_from_menu():

    menu_choice = Console.select_menu_option()
    if menu_choice == "s":
        search_books()
    if menu_choice == "r":
        File().print_file()
    if menu_choice == "x":
        return False

def search_books():
    search_results = get_search_results()
    if not Validation.validate_response(search_results):
        Console.print_string("There were no matches. ")
    else:
        book_list = create_book_list(search_results)
        ask_to_add_book_to_reading_list(book_list)

def get_search_results():
    term = Console.get_search_term()
    if term:
        return APIFetch.fetch_books(term)

def create_book_list(search_results):
    book_list = BookList(search_results)
    book_dictionary = book_list.create_book_list()
    Console.print_book_list(book_dictionary)
    return book_list

def ask_to_add_book_to_reading_list(book_list):
    add_book = Console.prompt_yn(
        "Would you like to add a book to your reading list?(y/n): ")
    if add_book == "y":
        add_to_reading_list(book_list)

def add_to_reading_list(book_list):
    books = ReadList(book_list)
    books.create_list()

if __name__ == "__main__":
    main()









