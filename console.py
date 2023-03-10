class Console:
    """ Displays prompts and receives user input. """

    @staticmethod
    def prompt_yn(string):
        """ Prompts user for a yes/no answer. """
        return input(string).lower()

    @staticmethod
    def prompt_input(string):
        """ Prompts user for a string input. """
        return input(string).lower()

    @staticmethod
    def print_book_list(book_dictionary):
        """ Prints book list. """
        for index, book in book_dictionary.items():
            Console.print_string(f"\n----------Book {index + 1}------------\n{book}")

    @staticmethod
    def select_menu_option():
        """ Display menu options and return user's choice. """
        menu_choice = Console.prompt_input(
            "\n++++++++++++++++Main Menu++++++++++++++++\nPress (s) to search books.\n"
            "Press (r) to view reading list.\nPress (x) to exit\n: ")
        return menu_choice

    @staticmethod
    def print_string(string):
        """ Prints string. """
        print(string)