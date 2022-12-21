import unittest
from main import *


class TestValidation(unittest.TestCase):
    validation = Validation()

    def test_valid_string_returns_true(self):
        self.assertTrue(self.validation.validate_string("test string"))

    def test_invalid_string_returns_false(self):
        self.assertFalse(self.validation.validate_string(""))

    def test_valid_bool_returns_true(self):
        self.assertTrue(self.validation.validate_bool("y"))
        self.assertTrue(self.validation.validate_bool("n"))

    def test_invalid_bool_returns_false(self):
        self.assertFalse(self.validation.validate_bool("x"))

    def test_valid_selection_returns_true(self):
        self.assertTrue(self.validation.validate_selection(1))

    def test_invalid_selection_returns_false(self):
        self.assertFalse(self.validation.validate_selection(6))

    def test_valid_response_returns_true(self):
        ok_response = {'kind': 'books#volumes', 'totalItems': 2, 'items': [{}, {}]}
        self.assertTrue(self.validation.validate_response(ok_response))

    def test_invalid_response_returns_false(self):
        bad_response = {'kind': 'books#volumes', 'totalItems': 0, 'items': []}
        self.assertFalse(self.validation.validate_response(bad_response))


class TestBook(unittest.TestCase):
    test_book = Book(["Author Name"], "My Book Title", "Publishing Co.")
    test_empty_info_book = Book([], "My Book Title", "")

    def test_get_author_returns_book_author(self):
        fetched_author = self.test_book.get_author()
        self.assertEqual(["Author Name"], fetched_author)

    def test_get_author_returns_empty_string_if_none(self):
        fetched_author = self.test_empty_info_book.get_author()
        self.assertEqual([], fetched_author)

    def test_get_title_returns_book_title(self):
        fetched_title = self.test_book.get_title()
        self.assertEqual("My Book Title", fetched_title)

    def test_get_publisher_returns_book_publisher(self):
        fetched_publisher = self.test_book.get_publisher()
        self.assertEqual("Publishing Co.", fetched_publisher)

    def test_get_publisher_returns_empty_string_if_none(self):
        fetched_publisher = self.test_empty_info_book.get_publisher()
        self.assertEqual("", fetched_publisher)


class TestReadList(unittest.TestCase):
    test_book_search = BookSearch()
    read_list = ReadList(test_book_search)

    def test_get_list_returns_reading_list(self):
        reading_list = [Book(["Author Name"], "My Book Title", "Publishing Co.")]
        self.read_list._read_list = reading_list
        fetched_list = self.read_list.get_list()

        self.assertEqual(reading_list, fetched_list)


if __name__ == '__main__':
    unittest.main()