import json
import requests


class Validation:
    """ Validates user inputs. """

    def validate_string(self, string):
        """ Validates user's string. """
        if string == "":
            print("This is an invalid choice. ")
            return False
        else:
            return True

    def validate_bool(self, input):
        """ Validates y/n selection """
        if input != "y" and input != "n":
            print("This is an invalid choice. ")
            return False
        else:
            return True

    def validate_selection(self, selection):
        """ Validates user's book selection. """
        if selection not in range(1, 6):
            print("Book number not found.")
            return False
        else:
            return True

    def validate_response(self, json_response):
        if not json_response['totalItems']:
            print("There were no matches. ")
            return False
        else:
            return True


class BookSearch:
    """ Reads and makes searchable Google Book Search API. """

    def __init__(self):
        self._book_dict = {}

    def get_search_term(self):
        """ Gets the search term from the user. """
        search_term = input("Enter book to be searched: ")
        if Validation().validate_string(search_term):
            self.fetch_books(search_term)
        else:
            self.get_search_term()

    def fetch_books(self, search_term):
        """ Fetches books from API. """
        response = requests.get("https://www.googleapis.com/books/v1/volumes?q=" + search_term)

        if response:
            parsed_books = response.json()
            if Validation().validate_response(parsed_books):
                self.set_list(parsed_books)
                self.print_book_list()
            else:
                retry = Console().prompt("Would you like to search again?(y/n): ")
                if retry == "y":
                    self.get_search_term()
                else:
                    print("Okay! Thank you so much and goodbye!")

    def set_list(self, parsed_books):
        """ Creates book list. """
        for book in range(5):
            book_object = self.create_book(book, parsed_books)
            self._book_dict[book] = book_object

    def create_book(self, book, parsed_books):
        """ Creates book object. """

        item = parsed_books["items"][book]["volumeInfo"]

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
                stripped = ', '.join(item.get_author())
                print(f"Authors: {stripped}")
            else:
                print(f"Author: {item.get_author()}")

            print(f"Title: {item.get_title()}")
            print(f"Publisher: {item.get_publisher()}")

        print('')


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
        self._selected_book = None
        while self._selected_book is None:
            self._selected_book = int(input("Select book number(1-5) to add to reading list: "))
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
            return "Book not found."

    def print_read_list(self):
        """ Prints the user's reading list. """
        books = File().read_file()
        if books["books"]:
            for book in books["books"]:
                print('----------------------------')
                if type(book["_author"]) is list:
                    stripped = ', '.join(book["_author"])
                    print(f"Authors: {stripped}")
                else:
                    print(f"Author: {book['_author']}")

                print(f"Title: {book['_title']}")
                print(f"Publisher: {book['_publisher']}")
            print('----------------------------')
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
        with open('read_list.json', 'w') as outfile:
            outfile.write(json_object)

    def write_file(self, book):
        """ Writes to a reading list file. """
        file_data = self.read_file()
        file_data["books"].append(book.__dict__)
        with open('read_list.json', 'w') as outfile:
            json.dump(file_data, outfile, indent=4)

    def read_file(self):
        """ Reads a reading list file. """
        with open('read_list.json', 'r') as openfile:
            json_object = json.load(openfile)
        return json_object


class Console:
    """ Prompts user and returns answer. """

    def prompt(self, string):
        answer = input(string).lower()
        if not Validation().validate_bool(answer):
            Console().prompt(string)

        return answer

def main():
    """ Defines an exception """
    try:
        File().read_file()
    except:
        File().create_file()

    print("Hello friend! This is a program that searches books using Google's Book Search API.\n"
          "It will then return a list of matches you can select from to save to a reading list file. Enjoy!")

    while True:
        search = BookSearch()
        search.get_search_term()
        books = ReadList(search)

        answer = Console().prompt("Would you like to add a book to your reading list?(y/n): ")
        while answer == "y":
            books.add_to_list()
            answer = Console().prompt("Would you like to add another book to your reading list?(y/n): ")

        answer = Console().prompt("Would you like to print your reading list?(y/n): ")
        if answer == "y":
            books.print_read_list()

        answer = Console().prompt("Would you like to search for another book?(y/n): ")
        if answer == "n":
            print("Okay. Goodbye!")
            break


if __name__ == "__main__":
    main()








