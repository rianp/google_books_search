class Validation:
    """ Validates user inputs and search results. """

    @staticmethod
    def validate_string(string):
        """ Validates user's string. """
        if string.strip() == "":
            return False
        return True

    @staticmethod
    def validate_bool(choice):
        """ Validates y/n selection. """
        if choice not in ("y", "n"):
            return False
        return True

    @staticmethod
    def validate_menu_choice(choice):
        """ Validates y/n selection. """
        if choice not in ("s", "r", "x"):
            return False
        return True

    @staticmethod
    def validate_selection(selection, list_length):
        """ Validates user's book selection. """
        if selection not in range(1, list_length + 1):
            return False
        return True

    @staticmethod
    def validate_response(json_response):
        """ Validate response returns list of books. """
        if not json_response["totalItems"]:
            return False
        return True
