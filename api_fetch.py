from validation import *
from console import *
import requests


class APIFetch:
    def __init__(self):
        self._search_term = ''
        self.search_results = []

    def search(self):
        self._get_search_term()
        self._fetch_books()

    def _get_search_term(self):
        search_term = Console.prompt_input("Enter book to be searched: ")
        if not Validation.validate_string(search_term):
            Console.print_string("This is an invalid string. ")
            self._get_search_term()
        else:
            self._search_term = search_term

    def _fetch_books(self):
        """ Fetches books from API. """
        try:
            response = requests.get("https://www.googleapis.com/books/v1/volumes?q=" + self._search_term)
            response.raise_for_status()
        except requests.exceptions.HTTPError as errh:
            Console.print_string(f"An Http Error occurred: {repr(errh)}")
            return
        except requests.exceptions.ConnectionError as errc:
            Console.print_string(f"An Error Connecting to the API occurred: {repr(errc)}")
            return
        except requests.exceptions.Timeout as errt:
            Console.print_string(f"A Timeout Error occurred: {repr(errt)}")
            return
        except requests.exceptions.RequestException as err:
            Console.print_string(f"An Unknown Error occurred {repr(err)}")
            return

        if not Validation.validate_response(response.json()):
            Console.print_string("There were no matches. ")
        else:
            self.search_results = response.json()