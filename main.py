import json
import requests
from validation import *


class APIFetch:

    def fetch_books(self, search_term):
        """ Fetches books from API. """
        try:
            response = requests.get("https://www.googleapis.com/books/v1/volumes?q=" + search_term)
            response.raise_for_status()
        except requests.exceptions.HTTPError as errh:
            return "An Http Error occurred:" + repr(errh)
        except requests.exceptions.ConnectionError as errc:
            return "An Error Connecting to the API occurred:" + repr(errc)
        except requests.exceptions.Timeout as errt:
            return "A Timeout Error occurred:" + repr(errt)
        except requests.exceptions.RequestException as err:
            return "An Unknown Error occurred" + repr(err)

        return response.json()


class BookList:
    """ Creates a book list object. """

    def __init__(self, search):
        self._book_dict = {}
        self._parsed_books = search

    def create_book_list(self):
        """ Creates book list. """
        list_length = min(self._parsed_books["totalItems"], 5)
        for book in range(list_length):
            book_object = self.create_book_object(book)
            self._book_dict[book] = book_object
        return self._book_dict

    def create_book_object(self, book):
        """ Creates book object. """
        item = self._parsed_books["items"][book]["volumeInfo"]
        book_id = self._parsed_books["items"][book]["id"]
        if "authors" not in item:
            author = []
        elif len(item["authors"]) > 1:
            author = item["authors"]
        else:
            author = item["authors"][0]

        title = item["title"]

        if "publisher" not in item:
            publisher = ""
        else:
            publisher = item["publisher"]

        return Book(book_id, author, title, publisher)

    def get_book_dict(self):
        """ Returns book list. """
        return self._book_dict


class Book:
    """ Creates book object. """

    def __init__(self, book_id, authors, title, publisher):
        self._book_id = book_id
        self._author = authors
        self._title = title
        self._publisher = publisher

    def __str__(self):
        """ Returns a formatted string version of a book object instance. """
        if isinstance(self._author, list):
            stripped = ", ".join(self._author)
            author = f"Authors: {stripped}"
        else:
            author = f"Author: {self._author}"

        return f"{author}\nTitle: {self._title}\nPublisher: {self._publisher}"

    def __repr__(self):
        """ Returns an unformatted string of a book object instance. """
        return f"Author: {self._author}, Title: {self._title}, Publisher: {self._publisher}"


class ReadList:
    """ Creates reading list. """

    def __init__(self, book_search):
        self._books = book_search
        self._selected_book = None

    def select_book(self):
        """ Gets book selection from user. """
        list_length = min(len(self._books.get_book_dict()), 5)

        selected_book = int(Console().prompt_input(
            f"Select book number(1-{list_length}) to add to reading list: "))

        if not Validation().validate_selection(selected_book, list_length):
            Console().print_string("Book number not found.")
            self.select_book()

        return selected_book

    def add_another_book(self):
        """ Handles searches that fail to return results. """
        add_another = Console().prompt_yn("Would you like to add another book?(y/n): ")
        if add_another == "y":
            return True
        else:
            return False

    def check_book_is_new(self):
        """ Checks if book has already been added to reading list. """
        read_list = File().read_file()
        for book in read_list["books"]:
            book_id = book["_book_id"]
            if book_id in str(self._selected_book):
                return False
            return True

    def set_read_list(self):
        """ Adds specified book to reading list. """
        key = self._selected_book - 1
        book = self._books.get_book_dict()[key]
        File().write_file(book)

    def create_list(self):
        """ Creates a reading list. """
        self._selected_book = self.select_book()

        if self.check_book_is_new():
            self.set_read_list()
        else:
            self.select_book()

        if self.add_another_book():
            self.create_list()
        else:
            return


class File:
    """ Creates and adds to JSON file. """
    def __init__(self):
        self._filename = "read_list.json"

    def create_file(self):
        """ Creates a reading list file. """
        books_dict = {}
        books_dict["books"] = []
        json_object = json.dumps(books_dict)
        with open(self._filename, "w") as outfile:
            outfile.write(json_object)

    def write_file(self, book):
        """ Writes to a reading list file. """
        file_data = self.read_file()
        file_data["books"].append(book.__dict__)
        try:
            with open(self._filename, "w") as outfile:
                json.dump(file_data, outfile, indent=4)
        except FileNotFoundError:
            Console().print_string(f"Sorry, the file {self._filename} does not exist.")

    def print_file(self):
        """ Prints the user's reading list file. """
        books = File().read_file()
        if books["books"]:
            for book in books["books"]:
                if isinstance(book["_author"], list):
                    stripped = ", ".join(book["_author"])
                    author = f"Authors: {stripped}"
                else:
                    author = f"Author: {book['_author']}"

                Console().print_string(f"\n----------------------------\n{author}\nTitle: {book['_title']}"
                                       f"\nPublisher: {book['_publisher']}\n----------------------------")
        else:
            Console().print_string("Reading list is empty. ")

    def read_file(self):
        """ Reads a reading list file. """
        try:
            with open(self._filename, "r") as openfile:
                json_object = json.load(openfile)
        except FileNotFoundError:
            Console().print_string(f"Sorry, the file {self._filename} does not exist.")
        return json_object


class Console:
    """ Displays prompts and receives user input. """

    def prompt_yn(self, string):
        """ Prompts user for a yes/no answer. """
        answer = input(string).lower()
        if not Validation().validate_bool(answer):
            self.print_string("This is an invalid choice. ")
            Console().prompt_yn(string)
        return answer

    def prompt_input(self, string):
        """ Prompts user for a string input. """
        answer = input(string).lower()
        return answer

    def get_search_term(self):
        """ Gets the search term from the user. """
        search_term = Console().prompt_input("Enter book to be searched: ")
        if not Validation().validate_string(search_term):
            self.print_string("This is an invalid string. ")
            Console().get_search_term()
        else:
            return search_term

    def print_book_list(self, book_dictionary):
        """ Prints book list. """
        for index, book in book_dictionary.items():
            self.print_string(f"\n----------Book {index + 1}------------\n{book}")

    def print_string(self, string):
        print(string)


class Menu:
    """ Main menu for command options for program. """

    def select_menu_option(self):
        """ Display menu options and return user's choice. """
        menu_choice = Console().prompt_input(
            "\n++++++++++++++++Main Menu++++++++++++++++\nPress (s) to search books.\n"
            "Press (r) to view reading list.\nPress (x) to exit\n: ")
        if not Validation().validate_menu_choice(menu_choice):
            Console().print_string("This is an invalid  menu choice. ")
            self.select_menu_option()
        else:
            return menu_choice


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









