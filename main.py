import json
import requests

class Error(Exception):
    """user-defined exception for duplicate pet error"""
    pass

class BookSearch:
    """ Reads and makes searchable Google Book Search API. """

    def __init__(self, book_title):
        response = requests.get("https://www.googleapis.com/books/v1/volumes?q=" + book_title)
        self._books = response.json()
        self._book_list = []
        self._read_list = []

    def search_books(self):
        """ Returns a sorted list of the author, title, and publisher of five books. """

        for book in range(5):
            item = self._books["items"][book]["volumeInfo"]

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

        for item in self._book_list:
            print('----------------------------')
            for key, value in item.items():
                if type(value) is list:
                    print(f'{key}s: {value}')
                else:
                    print(f'{key}: {value}')
        print('----------------------------')


    def add_to_read_list(self, selected_book):
        """ Adds specified book to read list. """

        for book in self._book_list:
            if book["title"] == selected_book:
                self._read_list.append(book)

    def get_read_list(self):
        """ Prints the user's read list. """
        for item in self._read_list:
            for key, value in item.items():
                print(f'{key}: {value}')

def main():
    """ Defines an exception """

    while True:
        book_title = input("enter book title: ")
        search = BookSearch(book_title)

        try:
            search.search_books()
        except Error:
            print('error')

        answer = input("would you like to add a book to your reading list?(y/n): ")
        if answer.lower() == "y":
            selected_book = input("select book title to add to reading list: ")
            try:
                search.add_to_read_list(selected_book)
            except Error:
                print("This book isn't in the list.")

        answer = input("would you like to print your reading list?(y/n): ")
        if answer.lower() == "y":
            print(search.get_read_list())

        search_update = input("Would you like to search another book?(y/n): ").lower()
        if search_update != "y":
            print("Okay. Goodbye!")
            break

if __name__ == "__main__":
    main()






