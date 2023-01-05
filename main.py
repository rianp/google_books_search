from validation import *
from api_fetch import *
from book_list import *
from book import *
from read_list import *
from console import *
from file import *
from menu import *


def main():
    """ Creates any necessary objects and calls functions to execute the program's logic. """
    try:
        File().read_file()
    except:
        File().create_file()

    Console().print_string("Hello friend! This is a program that searches for books using the Google Books API.\n"
                           "It returns a list of matches you can select from to save to a reading list file. Enjoy!")

    while True:
        menu_choice = Menu().select_menu_option()

        if menu_choice == "s":
            term = Console().get_search_term()
            if term:
                response = APIFetch().fetch_books(term)
                books = Validation().validate_books(response)
                if not books:
                    Console().print_string("There were no matches. ")
                else:
                    book_list = BookList(books)
                    book_dictionary = book_list.create_book_list()
                    Console().print_book_list(book_dictionary)

                    if book_list.get_book_dict():
                        books = ReadList(book_list)
                        answer = Console().prompt_yn(
                            "Would you like to add a book to your reading list?(y/n): ")
                        if answer == "y":
                            books.create_list()

        if menu_choice == "r":
            File().print_file()

        if menu_choice == "x":
            break

    Console().print_string("Okay. Goodbye!")


if __name__ == "__main__":
    main()









