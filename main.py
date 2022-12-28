import json
import requests


class Validation:
    """ Validates user inputs and search results. """

    def validate_string(self, string):
        """ Validates user's string. """
        if string == "":
            print("This is an invalid choice. ")
            return False
        return True

    def validate_bool(self, choice):
        """ Validates y/n selection. """
        if choice not in ("y", "n"):
            print("This is an invalid choice. ")
            return False
        return True

    def validate_menu_choice(self, choice):
        """ Validates y/n selection. """
        if choice not in ("s", "r", "m", "x"):
            print("This is an invalid choice. ")
            return False
        return True

    def validate_selection(self, selection):
        """ Validates user's book selection. """
        if selection not in range(1, 6):
            print("Book number not found.")
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
        self._book_dict = {}

    def get_search_term(self):
        """ Gets the search term from the user. """
        search_term = Console().prompt_input("Enter book to be searched: ")
        self.fetch_books(search_term)

    def fetch_books(self, search_term):
        """ Fetches books from API. """
        response = requests.get("https://www.googleapis.com/books/v1/volumes?q=" + search_term)
        response.raise_for_status()

        parsed_books = response.json()
        if Validation().validate_response(parsed_books):
            self.create_book_list(parsed_books)
            self.print_book_list()
        else:
            self.search_failed()


    def search_failed(self):
        """ Handles searches that fail to return results. """
        print("There were no matches. ")
        retry = Console().prompt_yn("Would you like to search again?(y/n): ")
        if retry == "y":
            self.get_search_term()
        else:
            print("Okay! Thank you so much and goodbye!")

    def create_book_list(self, parsed_books):
        """ Creates book list. """
        print(parsed_books)
        list_length = min(parsed_books["totalItems"], 5)
        for book in range(list_length):
            book_object = self.create_book_object(book, parsed_books)
            self._book_dict[book] = book_object

    def create_book_object(self, book, parsed_books):
        """ Creates book object. """
        item = parsed_books["items"][book]["volumeInfo"]

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
            print("")
            print(f"----------Book {index + 1}------------")

            if isinstance(book.get_author(), list):
                stripped = ", ".join(book.get_author())
                print(f"Authors: {stripped}")
            else:
                print(f"Author: {book.get_author()}")

            print(f"Title: {book.get_title()}")
            print(f"Publisher: {book.get_publisher()}")

        print("")

    def get_book_dict(self):
        """ Returns book list. """
        return self._book_dict


class Book:
    """ Creates book object. """

    def __init__(self, authors, title, publisher):
        self._author = authors
        self._title = title
        self._publisher = publisher

    def get_author(self):
        """ Returns book's author. """
        return self._author

    def get_title(self):
        """ Returns book's title. """
        return self._title

    def get_publisher(self):
        """ Returns book's publisher. """
        return self._publisher


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
            self._selected_book = Console().prompt_selection(
                f"Select book number(1-{list_length}) to add to reading list: ")
            if not Validation().validate_selection(self._selected_book):
                self._selected_book = None

    def set_read_list(self):
        """ Adds specified book to reading list. """
        key = self._selected_book - 1
        if key in self._books.get_book_dict():
            book = self._books.get_book_dict()[key]
            File().write_file(book)
            self._read_list.append(book)
        else:
            print("Book not found.")

    def print_read_list(self):
        """ Prints the user's reading list. """
        books = File().read_file()
        if books["books"]:
            for book in books["books"]:
                print('----------------------------')
                if isinstance(book["_author"], list):
                    stripped = ", ".join(book["_author"])
                    print(f"Authors: {stripped}")
                else:
                    print(f"Author: {book['_author']}")

                print(f"Title: {book['_title']}")
                print(f"Publisher: {book['_publisher']}")
            print("----------------------------")
        else:
            print("Reading list is empty. ")

    def get_list(self):
        """ Returns reading list. """
        return self._read_list

    def add_to_list(self):
        """ Creates a reading list. """
        self.select_book()
        self.set_read_list()


class File:
    """ Creates and adds to JSON file. """

    def create_file(self):
        """ Creates a reading list file. """
        books_dict = {}
        books_dict["books"] = []
        json_object = json.dumps(books_dict)
        with open("read_list.json", "w") as outfile:
            outfile.write(json_object)

    def write_file(self, book):
        """ Writes to a reading list file. """
        file_data = self.read_file()
        file_data["books"].append(book.__dict__)
        with open("read_list.json", "w") as outfile:
            json.dump(file_data, outfile, indent=4)

    def read_file(self):
        """ Reads a reading list file. """
        with open("read_list.json", "r") as openfile:
            json_object = json.load(openfile)
        return json_object


class Console:
    """ Displays prompts and receives user input. """

    def prompt_yn(self, string):
        """ Prompts user for a yes/no answer. """
        answer = input(string).lower()
        if not Validation().validate_bool(answer):
            Console().prompt_yn(string)
        return answer

    def prompt_menu_choice(self, string):
        """ Prompts user for a yes/no answer. """
        answer = input(string).lower()
        if not Validation().validate_menu_choice(answer):
            Console().prompt_menu_choice(string)
        return answer

    def prompt_input(self, string):
        """ Prompts user for a string input. """
        answer = input(string).lower()
        if not Validation().validate_string(answer):
            Console().prompt_input(string)
        return answer

    def prompt_selection(self, string):
        """ Prompts user for a selection between 1-5. """
        answer = int(input(string))
        if not Validation().validate_selection(answer):
            Console().prompt_selection(string)
        return answer


class Menu:
    """ Main menu for command options for program. """

    def get_menu(self):
        """ Display menu options and return user's choice. """
        print("++++++++++++++Main Menu++++++++++++++")
        answer = Console().prompt_menu_choice(
            "Press (s) to search books.\nPress (r) to view reading list.\n"
            "Press (m) to view menu\nPress (x) to exit\n: ")
        return answer


def main():
    """ Creates any necessary objects and calls functions to execute the program's logic. """
    try:
        File().read_file()
    except:
        File().create_file()

    print("Hello friend! This is a program that searches for books using the Google Books API.\n"
          "It returns a list of matches you can select from to save to a reading list file. Enjoy!")

    answer = Menu().get_menu()

    while answer != "x":
        search = BookSearch()
        books = ReadList(search)

        if answer == "s":
            search.get_search_term()
            if search.get_book_dict():
                answer = Console().prompt_yn(
                    "Would you like to add a book to your reading list?(y/n): ")
                while answer == "y":
                    books.add_to_list()
                    answer = Console().prompt_yn(
                        "Would you like to add another book to your reading list?(y/n): ")
        elif answer == "r":
            books.print_read_list()
        elif answer == "m":
            answer = Menu().get_menu()
        elif answer == "x":
            print("Okay goodbye!")
            break

        answer = Console().prompt_menu_choice(
            "Press (m) to display menu or (x) to exit: ")

    print("Okay. Goodbye!")



if __name__ == "__main__":
    main()









