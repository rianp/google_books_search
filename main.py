import json
import requests

class Validation:
    """exception for no book error"""

    def __init__(self, string):
        self._string = string

    def validate_string(self):
        """ Validates user's string. """
        if self._string is None:
            return self.invalid_string()
        # elif self._string not in Books():
        #     return self.invalid_choice()
        else:
            return

    def invalid_choice(self):
        """ Prints error message for an invalid choice. """
        print("This is an invalid choice. ")

    def invalid_string(self):
        """ Prints error message for an invalid choice. """
        print("This is an invalid string. ")

class BookSearch:
    """ Reads and makes searchable Google Book Search API. """

    def __init__(self, term):
        self._search_term = term.get_term()
        self._response = ""
        self._parsed_books = []
        self._book_list = []

    def fetch_books(self):
        """ Fetches books from API. """
        self._response = requests.get("https://www.googleapis.com/books/v1/volumes?q=" + self._search_term)

    def parse_response(self):
        """ Parses the fetch response. """
        self._parsed_books = self._response.json()

    def set_list(self):
        """ Creates book list. """
        for book in range(5):
            book = self.create_book(book)
            self._book_list.append(book)

    def create_book(self, book):
        """ Creates book object. """

        item = self._parsed_books["items"][book]["volumeInfo"]

        if len(item['authors']) > 1:
            author = item['authors']
        elif 'authors' not in item:
            author = []
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

        for item in self._book_list:
            print('----------------------------')

            if type(item.get_author()) is list:
                stripped = str(item.get_author())[1:-1]
                print(f"Authors: {stripped}")
            else:
                print(f"Author: {item.get_author()}")

            print(f"Title: {item.get_title()}")
            print(f"Publisher: {item.get_publisher()}")

        print('----------------------------')

    def get_book_list(self):
        """ Returns book list. """
        return self._book_list

    def search_books(self):
        """ Returns a sorted list of the author, title, and publisher of five books. """

        if True:
            self.fetch_books()
            self.parse_response()
            self.set_list()
            self.print_book_list()

class Book():
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

    def __init__(self, book_search, console):
        self._books = book_search
        self._selected_book = console.get_selected_book()
        self._read_list = []

    def set_read_list(self):
        """ Adds specified book to read list. """

        for book in self._books.get_book_list():
            if book.get_title().lower() == self._selected_book:
                self._read_list.append(book)

    def get_read_list(self):
        """ Prints the user's read list. """

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

    def read_list(self):
        self.set_read_list()


class Console:

    def __init__(self):
        self._search_term = ""
        self._selected_book = ""
        self._add_book = ""
        self._print_list = ""
        self._search_another = ""

    def search_term(self):
        self._search_term = input("Enter book to be searched: ")

    def add_book_prompt(self):
        self._add_book = input("would you like to add a book to your reading list?(y/n): ").lower()

    def select_book_prompt(self):
        self._selected_book = input("select book title to add to reading list: ").lower()

    def try_another_prompt(self):
        self._add_book = input("would you like to try another book?(y/n): ").lower()

    def reading_list_prompt(self):
        self._print_list = input("would you like to print your reading list?(y/n): ").lower()

    def search_another_prompt(self):
        self._search_another = input("Would you like to search another book?(y/n): ").lower()

    def get_add_book(self):
        return self._add_book

    def get_list(self):
        return self._print_list

    def get_search_another(self):
        return self._search_another

    def get_term(self):
        return self._search_term

    def get_selected_book(self):
        return self._selected_book


def main():
    """ Defines an exception """

    while True:
        console = Console()
        console.search_term()

        search = BookSearch(console)
        search.search_books()

        console.add_book_prompt()
        while console.get_add_book().lower() == "y":
            console.select_book_prompt()
            books = ReadList(search, console)
            books.read_list()
            console.try_another_prompt()

        console.reading_list_prompt()
        if console.get_list() == "y":
            books.get_read_list()

        console.search_another_prompt()
        if console.get_search_another() != "y":
            print("Okay. Goodbye!")
            break

if __name__ == "__main__":
    main()



   # def add_to_read_list(self, selected_book):
   #      """ Adds specified book to read JSON file. """
   #
   #      # for book in self._book_list:
   #          # if selected_book in book.values():
   #      with open('read_list.json', 'a') as outfile:
   #          for book in self._book_list:
   #              if book["title"] == selected_book:
   #                  json.dump(book, outfile)
   #          # outfile.write('\n')
   #              # print("true")
   #          # else:
   #          #     raise NoBookError
   #
   #  def get_read_list(self):
   #      """ Prints the user's read list. """
   #
   #      with open("read_list.json", 'r') as infile:
   #          self._read_list = json.load(infile)
   #
   #          print(self._read_list)
   #
   #      # for item in self._read_list:
   #      #     for key, value in item.items():
   #      #         print(f'{key}: {value}')






