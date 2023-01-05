class Book:
    """ Creates book object. """

    def __init__(self, book_id, authors, title, publisher):
        self._book_id = book_id
        self._author = authors
        self._title = title
        self._publisher = publisher

    def __str__(self):
        """ Returns a formatted string version of a book object instance. """
        if isinstance(self._author, list):
            stripped = ", ".join(self._author)
            author = f"Authors: {stripped}"
        else:
            author = f"Author: {self._author}"

        return f"{author}\nTitle: {self._title}\nPublisher: {self._publisher}"

    def __repr__(self):
        """ Returns an unformatted string of a book object instance. """
        return f"Author: {self._author}, Title: {self._title}, Publisher: {self._publisher}"

    def get_book_id(self):
        """ Returns the book id. """
        return self._book_id