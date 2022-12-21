import json
import requests


class Validation:
    """exception for no book error"""

    def validate_string(self, string):
        """ Validates user's string. """
        if string == "":
            self.invalid_choice()
            return False
        else:
            return True

    def validate_bool(self, input):
        """ Validates user's string. """
        if input != "y" and input != "n":
            self.invalid_choice()
            return False
        else:
            return True

    def validate_selection(self, selection):
        """ Validates user's string. """
        if selection not in range(1, 5):
            print("book number not found.")
            return False
        else:
            return True

    def invalid_choice(self):
        """ Prints error message for an invalid choice. """
        print("This is an invalid choice. ")


class BookSearch:
    """ Reads and makes searchable Google Book Search API. """

    def __init__(self):
        self._search_term = ""
        self._response = ""
        self._parsed_books = []
        self._book_dict = {}

    def set_search_term(self):
        """ Gets the search term from the user. """
        while self._search_term == "":
            self._search_term = str(input("Enter book to be searched: "))
            if not Validation().validate_string(self._search_term):
                self._search_term = ""

    def fetch_books(self):
        """ Fetches books from API. """
        self._response = requests.get("https://www.googleapis.com/books/v1/volumes?q=" + self._search_term)

    def parse_response(self):
        """ Parses the fetch response. """
        if self._response:
            self._parsed_books = self._response.json()
        else:
            print("There were no matches. ")

    def set_list(self):
        """ Creates book list. """
        for book in range(5):
            book_object = self.create_book(book)
            self._book_dict[book] = book_object

    def create_book(self, book):
        """ Creates book object. """

        item = self._parsed_books["items"][book]["volumeInfo"]

        if 'authors' not in item:
            author = []
        elif len(item['authors']) > 1:
            author = item['authors']
        else:
            author = item['authors'][0]

        title = item['title']

        if 'publisher' not in item:
            publisher = ''
        else:
            publisher = item['publisher']

        book = Book(author, title, publisher)
        return book

    def print_book_list(self):
        """ Prints book list. """

        for key in self._book_dict:
            item = self._book_dict[key]
            print('')
            print(f"----------Book {key + 1}------------")

            if type(self._book_dict[key].get_author()) is list:
                stripped = str(item.get_author())[1:-1]
                print(f"Authors: {stripped}")
            else:
                print(f"Author: {item.get_author()}")

            print(f"Title: {item.get_title()}")
            print(f"Publisher: {item.get_publisher()}")

        print('')

    def get_book_dict(self):
        """ Returns book list. """
        return self._book_dict

    def search_books(self):
        """ Returns a sorted list of the author, title, and publisher of five books. """

        if True:
            self.set_search_term()
            self.fetch_books()
            self.parse_response()
            self.set_list()
            self.print_book_list()


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
        while self._selected_book is None:
            self._selected_book = int(input("Select book number(1-5) to add to reading list: "))
            if not Validation().validate_selection(self._selected_book):
                self._selected_book = None

    def set_read_list(self):
        """ Adds specified book to read list. """
        key = self._selected_book - 1
        if key in self._books.get_book_dict():
            book = self._books.get_book_dict()[key]
            self._read_list.append(book)
        else:
            return "book not found."

    def get_read_list(self):
        """ Prints the user's read list. """
        if self._read_list:
            for item in self._read_list:
                print('----------------------------')

                if type(item.get_author()) is list:
                    stripped = str(item.get_author())[1:-1]
                    print(f"Authors: {stripped}")
                else:
                    print(f"Author: {item.get_author()}")

                print(f"Title: {item.get_title()}")
                print(f"Publisher: {item.get_publisher()}")

            print('----------------------------')
        else:
            print("Reading list is empty. ")

    def get_list(self):
        """ Returns reading list. """
        return self._read_list

    def read_list(self):
        self.select_book()
        self.set_read_list()


class File:
    """ Creates and adds to JSON file. """

    def create_file(self):
        """ Creates read list file. """
        books_dict = {}
        books_dict["books"] = []
        json_object = json.dumps(books_dict)
        with open('read_list.json', 'w') as outfile:
            outfile.write(json_object)

    def write_file(self, books):
        """ Writes to read list file. """
        file_data = self.read_file()
        for book in books:
            file_data["books"].append(book.__dict__)
        with open('read_list.json', 'w') as outfile:
            json.dump(file_data, outfile)

    def read_file(self):
        """ Reads read list file. """
        with open('read_list.json', 'r') as openfile:
            json_object = json.load(openfile)
        return json_object


class Console:
    """ Prompts user and returns answer. """

    def prompt(self, string):
        answer = ""
        while answer == "":
            answer = input(string).lower()
            if not Validation().validate_bool(answer):
                answer = ""
        return answer


def main():
    """ Defines an exception """
    try:
        File().read_file()
    except:
        File().create_file()

    print("Hello friend! This is a search and save programming for books using Google Book Search API. Enjoy!")

    while True:
        search = BookSearch()
        search.search_books()
        books = ReadList(search)

        answer = Console().prompt("Would you like to add a book to your reading list?(y/n): ")

        while answer == "y":
            books.read_list()
            answer = Console().prompt("Would you like to add another book?(y/n): ")

        answer = Console().prompt("Would you like to print your reading list?(y/n): ")
        if answer == "y":
            books.get_read_list()

        answer = Console().prompt("Would you like to save list to file?(y/n): ")
        if answer == "y":
            File().write_file(books.get_list())

        answer = Console().prompt("Would you like read file?(y/n): ")
        if answer == "y":
            print(File().read_file())

        answer = Console().prompt("Would you like to search another book?(y/n): ")
        if answer == "n":
            print("Okay. Goodbye!")
            break


if __name__ == "__main__":
    main()








