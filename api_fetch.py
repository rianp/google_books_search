import requests
from console import *

class APIFetch:

    @staticmethod
    def fetch_books(search_term):
        """ Fetches books from API. """
        try:
            response = requests.get("https://www.googleapis.com/books/v1/volumes?q=" + search_term)
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

        return response.json()