from validation import *
from console import *

class Menu:
    """ Main menu for command options for program. """

    @staticmethod
    def select_menu_option():
        """ Display menu options and return user's choice. """
        menu_choice = Console.prompt_input(
            "\n++++++++++++++++Main Menu++++++++++++++++\nPress (s) to search books.\n"
            "Press (r) to view reading list.\nPress (x) to exit\n: ")
        if not Validation.validate_menu_choice(menu_choice):
            Console.print_string("This is an invalid  menu choice. ")
            Menu.select_menu_option()
        else:
            return menu_choice