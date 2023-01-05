from console import *
from file import *


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