import json
from console import *

class File:
    """ Creates and adds to JSON file. """
    def __init__(self):
        self._filename = "read_list.json"

    def create_file(self):
        """ Creates a reading list file. """
        books_dict = {}
        books_dict["books"] = []
        json_object = json.dumps(books_dict)
        with open(self._filename, "w") as outfile:
            outfile.write(json_object)

    def write_file(self, book):
        """ Writes to a reading list file. """
        file_data = self.read_file()
        file_data["books"].append(book.__dict__)
        try:
            with open(self._filename, "w") as outfile:
                json.dump(file_data, outfile, indent=4)
        except FileNotFoundError:
            Console().print_string(f"Sorry, the file {self._filename} does not exist.")

    def print_file(self):
        """ Prints the user's reading list file. """
        books = File().read_file()
        if books["books"]:
            for book in books["books"]:
                if isinstance(book["_author"], list):
                    stripped = ", ".join(book["_author"])
                    author = f"Authors: {stripped}"
                else:
                    author = f"Author: {book['_author']}"

                Console().print_string(f"\n----------------------------\n{author}\nTitle: {book['_title']}"
                                       f"\nPublisher: {book['_publisher']}\n----------------------------")
        else:
            Console().print_string("Reading list is empty. ")

    def read_file(self):
        """ Reads a reading list file. """
        try:
            with open(self._filename, "r") as openfile:
                json_object = json.load(openfile)
        except FileNotFoundError:
            Console().print_string(f"Sorry, the file {self._filename} does not exist.")
        return json_object