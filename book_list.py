from book import *


class BookList:
    """ Creates a book list object. """

    def __init__(self, search):
        self._book_dict = {}
        self._parsed_books = search

    def create_book_list(self):
        """ Creates book list. """
        list_length = min(self._parsed_books["totalItems"], 5)
        for book in range(list_length):
            book_object = self._create_book_object(book)
            self._book_dict[book] = book_object
        return self._book_dict

    def get_book_dict(self):
        """ Returns book list. """
        return self._book_dict

    def _create_book_object(self, book):
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
