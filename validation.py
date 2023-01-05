class Validation:
    """ Validates user inputs and search results. """

    def validate_string(self, string):
        """ Validates user's string. """
        if string.strip() == "":
            return False
        return True

    def validate_bool(self, choice):
        """ Validates y/n selection. """
        if choice not in ("y", "n"):
            return False
        return True

    def validate_menu_choice(self, choice):
        """ Validates y/n selection. """
        if choice not in ("s", "r", "x"):
            return False
        return True

    def validate_selection(self, selection, list_length):
        """ Validates user's book selection. """
        if selection not in range(1, list_length + 1):
            return False
        return True

    def validate_response(self, json_response):
        """ Validate response returns list of books. """
        if not json_response["totalItems"]:
            return False
        return True

    def validate_books(self, parsed_books):
        """ Validates parsed books. """
        if not Validation().validate_response(parsed_books):
            return False
        else:
            return parsed_books