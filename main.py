import json
import requests


class Validation:
    """ Validates user inputs and search results. """

    def validate_string(self, string):
        """ Validates user's string. """
        if string.strip() == "":
            Console().print_string("This is an invalid string. ")
            return False
        return True

    def validate_bool(self, choice):
        """ Validates y/n selection. """
        if choice not in ("y", "n"):
            Console().print_string("This is an invalid choice. ")
            return False
        return True

    def validate_menu_choice(self, choice):
        """ Validates y/n selection. """
        if choice not in ("s", "r", "x"):
            Console().print_string("This is an invalid  menu choice. ")
            return False
        return True

    def validate_selection(self, selection, list_length):
        """ Validates user's book selection. """
        if selection not in range(1, list_length + 1):
            Console().print_string("Book number not found.")
            return False
        return True

    def validate_response(self, json_response):
        """ Validate response returns list of books. """
        if not json_response["totalItems"]:
            return False
        return True


class BookSearch:
    """ Reads and makes searchable Google Book Search API. """

    def __init__(self):
        self._parsed_books = {}

    def get_search_term(self):
        """ Gets the search term from the user. """
        search_term = Console().prompt_input("Enter book to be searched: ")
        if Validation().validate_string(search_term):
            self.fetch_books(search_term)
        else:
            self.get_search_term()

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

        parsed_books = response.json()
        if Validation().validate_response(parsed_books):
            self._parsed_books = parsed_books
        else:
            Console().print_string("There were no matches. ")
            return False

    def get_parsed_books(self):
        """ Returns parsed books dictionary. """
        return self._parsed_books


class BookList:
    """ Creates a book list object. """

    def __init__(self, search):
        self._book_dict = {}
        self._parsed_books = search.get_parsed_books()

    def create_book_list(self):
        """ Creates book list. """
        list_length = min(self._parsed_books["totalItems"], 5)
        for book in range(list_length):
            book_object = self.create_book_object(book)
            self._book_dict[book] = book_object

    def create_book_object(self, book):
        """ Creates book object. """
        item = self._parsed_books["items"][book]["volumeInfo"]

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

        return Book(author, title, publisher)

    def print_book_list(self):
        """ Prints book list. """
        for index, book in self._book_dict.items():
            Console().print_string(f"\n----------Book {index + 1}------------\n{book}")

    def get_book_dict(self):
        """ Returns book list. """
        return self._book_dict


class Book:
    """ Creates book object. """

    def __init__(self, authors, title, publisher):
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
        self._read_list = []

    def select_book(self):
        """ Gets book selection from user. """
        list_length = min(len(self._books.get_book_dict()), 5)
        self._selected_book = None
        while self._selected_book is None:
            self._selected_book = int(Console().prompt_input(
                f"Select book number(1-{list_length}) to add to reading list: "))
            if not Validation().validate_selection(self._selected_book, list_length):
                self._selected_book = None

    def add_another_book(self):
        """ Handles searches that fail to return results. """
        add_another = Console().prompt_yn("Would you like to add another book?(y/n): ")
        if add_another == "y":
            self.add_to_list()
        else:
            return

    def check_book(self, selected_book):
        """ Checks if book has already been added to reading list. """
        read_list = File().read_file()
        for book in read_list["books"]:
            if isinstance(book["_author"], list):
                author = ", ".join(book["_author"])
            else:
                author = book["_author"]
            if author in str(selected_book):
                if book["_title"] in str(selected_book):
                    Console().print_string("This book is already in your reading list. ")
                    self.add_another_book()
            else:
                pass

    def set_read_list(self):
        """ Adds specified book to reading list. """
        key = self._selected_book - 1
        if key in self._books.get_book_dict():
            book = self._books.get_book_dict()[key]
            self.check_book(book)
            File().write_file(book)
            self._read_list.append(book)
        else:
            Console().print_string("Book not found.")

    def add_to_list(self):
        """ Creates a reading list. """
        self.select_book()
        self.set_read_list()
        self.add_another_book()


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
            Console().prompt_yn(string)
        return answer

    def prompt_input(self, string):
        """ Prompts user for a string input. """
        answer = input(string).lower()
        return answer

    def print_string(self, string):
        print(string)


class Menu:
    """ Main menu for command options for program. """

    def select_menu_option(self):
        """ Display menu options and return user's choice. """
        menu_choice = Console().prompt_input(
            "\n++++++++++++++++Main Menu++++++++++++++++\nPress (s) to search books.\n"
            "Press (r) to view reading list.\nPress (x) to exit\n: ")
        if Validation().validate_menu_choice(menu_choice):
            return menu_choice
        else:
            return


def main():
    """ Creates any necessary objects and calls functions to execute the program's logic. """
    try:
        File().read_file()
    except:
        File().create_file()

    Console().print_string("Hello friend! This is a program that searches for books using the Google Books API.\n"
                           "It returns a list of matches you can select from to save to a reading list file. Enjoy!")

    while True:
        search = BookSearch()

        menu_choice = Menu().select_menu_option()

        if menu_choice == "s":
            term = search.get_search_term()
            if term:
                book_list = BookList(search)
                book_list.create_book_list()
                book_list.print_book_list()
                books = ReadList(book_list)
                if book_list.get_book_dict():
                    answer = Console().prompt_yn(
                        "Would you like to add a book to your reading list?(y/n): ")
                    if answer == "y":
                        books.add_to_list()

        if menu_choice == "r":
            File().print_file()

        if menu_choice == "x":
            break

    Console().print_string("Okay. Goodbye!")


if __name__ == "__main__":
    main()









