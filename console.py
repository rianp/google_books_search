from validation import *


class Console:
    """ Displays prompts and receives user input. """

    def prompt_yn(self, string):
        """ Prompts user for a yes/no answer. """
        answer = input(string).lower()
        if not Validation().validate_bool(answer):
            self.print_string("This is an invalid choice. ")
            Console().prompt_yn(string)
        return answer

    def prompt_input(self, string):
        """ Prompts user for a string input. """
        answer = input(string).lower()
        return answer

    def get_search_term(self):
        """ Gets the search term from the user. """
        search_term = Console().prompt_input("Enter book to be searched: ")
        if not Validation().validate_string(search_term):
            self.print_string("This is an invalid string. ")
            Console().get_search_term()
        else:
            return search_term

    def print_book_list(self, book_dictionary):
        """ Prints book list. """
        for index, book in book_dictionary.items():
            self.print_string(f"\n----------Book {index + 1}------------\n{book}")

    def print_string(self, string):
        print(string)