import requests

class APIFetch:

    def fetch_books(self, search_term):
        """ Fetches books from API. """
        try:
            response = requests.get("https://www.googleapis.com/books/v1/volumes?q=" + search_term)
            response.raise_for_status()
        except requests.exceptions.HTTPError as errh:
            return "An Http Error occurred:" + repr(errh)
        except requests.exceptions.ConnectionError as errc:
            return "An Error Connecting to the API occurred:" + repr(errc)
        except requests.exceptions.Timeout as errt:
            return "A Timeout Error occurred:" + repr(errt)
        except requests.exceptions.RequestException as err:
            return "An Unknown Error occurred" + repr(err)

        return response.json()