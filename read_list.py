from console import *
from file import *


class ReadList:
    """ Creates reading list. """

    def __init__(self, book_search):
        self._books = book_search
        self._selected_book = None

    def _select_book(self):
        """ Gets book selection from user. """
        list_length = min(len(self._books.get_book_dict()), 5)

        selected_book = int(Console().prompt_input(
            f"Select book number(1-{list_length}) to add to reading list: "))

        if not Validation.validate_selection(selected_book, list_length):
            Console().print_string("Book number not found.")
            self._select_book()

        return selected_book

    def _add_another_book(self):
        """ Handles searches that fail to return results. """
        add_another = Console().prompt_yn("Would you like to add another book?(y/n): ")
        if add_another == "y":
            return True
        else:
            return False

    def _check_book_is_new(self):
        """ Checks if book has already been added to reading list. """
        read_list = File().read_file()
        for book in read_list["books"]:
            book_id = book["_book_id"]
            if book_id in str(self._selected_book):
                return False
            return True

    def _set_read_list(self):
        """ Adds specified book to reading list. """
        key = self._selected_book - 1
        book = self._books.get_book_dict()[key]
        File().write_file(book)

    def create_list(self):
        """ Creates a reading list. """
        self._selected_book = self._select_book()

        if self._check_book_is_new():
            self._set_read_list()
        else:
            self._select_book()

        if self._add_another_book():
            self.create_list()
        else:
            return