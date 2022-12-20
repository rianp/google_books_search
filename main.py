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

    def __init__(self):
        self._search_term = ""
        self._response = ""
        self._parsed_books = []
        self._book_list = []

    def get_search_term(self):
        """ Gets search term from user. """
        self._search_term = input("Enter book to be searched: ")

    def fetch_books(self):
        """ Fetches books from API. """
        self._response = requests.get("https://www.googleapis.com/books/v1/volumes?q=" + self._search_term)

    def parse_response(self):
        """ Parses the fetch response. """
        self._parsed_books = self._response.json()

    def set_list(self):
        """ Creates book list. """
        for book in range(5):
            item = self._parsed_books["items"][book]["volumeInfo"]

            if len(item['authors']) > 1:
                author = item['authors']
            else:
                author = item['authors'][0]

            title = item['title']

            if 'publisher' not in item:
                publisher = ''
            else:
                publisher = item['publisher']

            book = {"author": author, "title": title, "publisher": publisher}
            self._book_list.append(book)

    def print_book_list(self):
        """ Prints book list. """

        for item in self._book_list:
            print('----------------------------')
            for key, value in item.items():
                if type(value) is list:
                    print(f'{key}s: {value}')
                else:
                    print(f'{key}: {value}')
        print('----------------------------')

    def get_book_list(self):
        """ Returns book list. """
        return self._book_list

    def search_books(self):
        """ Returns a sorted list of the author, title, and publisher of five books. """
        self.get_search_term()

        if True:
            self.fetch_books()
            self.parse_response()
            self.set_list()
            self.print_book_list()


class ReadList:
    """ Creates reading list. """

    def __init__(self, book_search):
        self._books = book_search
        self._selected_book = ""
        self._read_list = []

    def select_book(self):
        """ Gets book selection. """
        self._selected_book = input("select book title to add to reading list: ").lower()

    def set_read_list(self):
        """ Adds specified book to read list. """

        for book in self._books.get_book_list():
            if book["title"].lower() == self._selected_book:
                self._read_list.append(book)

    def get_read_list(self):
        """ Prints the user's read list. """
        for item in self._read_list:
            print('----------------------------')
            for key, value in item.items():
                if type(value) is list:
                    print(f'{key}s: {value}')
                else:
                    print(f'{key}: {value}')
        print('----------------------------')

    def read_list(self):
        self.select_book()
        self.set_read_list()


class Console:

    def __init__(self):
        self._search_term = ""
        self._selected_book = ""
        self._add_book = ""
        self._try_another = ""
        self._search_another = ""

    def search_prompt(self):
        self._search_term = input("Enter book to be searched: ")

    def add_book_prompt(self):
        self._add_book = input("would you like to add a book to your reading list?(y/n): ").lower()

    def select_book_prompt(self):
        self._selected_book = input("select book title to add to reading list: ")

    def try_another_prompt(self):
        self._try_another = input("would you like to try another book?(y/n): ").lower()

    def print_reading_list_prompt(self):
        self._try_another = input("would you like to print your reading list?(y/n): ").lower()

    def search_another_prompt(self):
        self._search_another = input("Would you like to search another book?(y/n): ").lower()


def main():
    """ Defines an exception """

    while True:
        search = BookSearch()
        search.search_books()

        answer = input("would you like to add a book to your reading list?(y/n): ")
        while answer.lower() == "y":
            books = ReadList(search)
            books.read_list()
            answer = input("would you like to try another book?(y/n): ")

        answer = input("would you like to print your reading list?(y/n): ")
        if answer.lower() == "y":
            books.get_read_list()

        search_update = input("Would you like to search another book?(y/n): ").lower()
        if search_update != "y":
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






