from validation import *


class Console:
    """ Displays prompts and receives user input. """

    @staticmethod
    def prompt_yn(string):
        """ Prompts user for a yes/no answer. """
        answer = input(string).lower()
        if not Validation.validate_bool(answer):
            Console.print_string("This is an invalid choice. ")
            Console.prompt_yn(string)
        return answer

    @staticmethod
    def prompt_input(string):
        """ Prompts user for a string input. """
        answer = input(string).lower()
        return answer

    @staticmethod
    def get_search_term():
        """ Gets the search term from the user. """
        search_term = Console.prompt_input("Enter book to be searched: ")
        if not Validation.validate_string(search_term):
            Console.print_string("This is an invalid string. ")
            Console.get_search_term()
        else:
            return search_term

    @staticmethod
    def print_book_list(book_dictionary):
        """ Prints book list. """
        for index, book in book_dictionary.items():
            Console.print_string(f"\n----------Book {index + 1}------------\n{book}")

    @staticmethod
    def print_string(string):
        print(string)