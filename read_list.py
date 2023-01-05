from console import *
from file import *


class ReadList:
    """ Creates reading list. """

    def __init__(self, book_search):
        self._books = book_search
        self._selected_book_key = None

    def _select_book(self):
        """ Gets book selection from user. """
        list_length = min(len(self._books.get_book_dict()), 5)

        selected_book = int(Console.prompt_input(
            f"Select book number(1-{list_length}) to add to reading list: "))

        if not Validation.validate_selection(selected_book, list_length):
            Console.print_string("Sorry, book number not found. ")
            self._select_book()

        return selected_book

    def _add_another_book(self):
        """ Handles searches that fail to return results. """
        add_another = Console.prompt_yn("Would you like to add another book?(y/n): ")
        if add_another == "y":
            return True
        else:
            return False

    def _check_book_is_new(self, selected_book):
        """ Checks if book has already been added to reading list. """
        selected_book_id = selected_book.get_book_id()
        read_list = File().read_file()
        for book in read_list["books"]:
            if book["_book_id"] == selected_book_id:
                return False
        return True

    def _fetch_selected_book(self):
        """ Takes selected book number and returns selected book. """
        index = self._selected_book_key - 1
        selected_book = self._books.get_book_dict()[index]
        return selected_book

    def create_list(self):
        """ Creates a reading list. """
        self._selected_book_key = self._select_book()
        selected_book = self._fetch_selected_book()

        if not self._check_book_is_new(selected_book):
            Console.print_string("This book is already in your reading list :) ")
        else:
            File().write_file(selected_book)

        if self._add_another_book():
            self.create_list()
        else:
            return