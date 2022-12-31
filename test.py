import unittest
from unittest.mock import patch
import mock
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

    def test_valid_menu_choice_returns_true(self):
        self.assertTrue(self.validation.validate_menu_choice("s"))
        self.assertTrue(self.validation.validate_menu_choice("r"))
        self.assertTrue(self.validation.validate_menu_choice("x"))

    def test_invalid_menu_choice_returns_false(self):
        self.assertFalse(self.validation.validate_menu_choice("f"))

    def test_valid_selection_returns_true(self):
        self.assertTrue(self.validation.validate_selection(1, 5))

    def test_invalid_selection_returns_false(self):
        self.assertFalse(self.validation.validate_selection(6, 5))

    def test_valid_response_returns_true(self):
        ok_response = {'kind': 'books#volumes', 'totalItems': 2, 'items': [{}, {}]}
        self.assertTrue(self.validation.validate_response(ok_response))

    def test_invalid_response_returns_false(self):
        bad_response = {'kind': 'books#volumes', 'totalItems': 0, 'items': []}
        self.assertFalse(self.validation.validate_response(bad_response))


class TestBookSearch(unittest.TestCase):
    @patch('main.BookSearch')
    def test_blog_posts(self, MockSearch):
        book_search = MockSearch()

        book_search.get_search_term().return_value = [
            {
                "Authors": "Author Name",
                "Title": "My Book Title",
                "Publisher": "Publishing Co."
            }
        ]

        response = book_search.get_search_term()
        print(response[0])
        self.assertIsNotNone(response)
        print(response[0])
        # self.assertIsInstance(response[0], dict)


class TestBook(unittest.TestCase):
    test_book = Book(["Author Name"], "My Book Title", "Publishing Co.")
    test_empty_info_book = Book([], "My Book Title", "")

    def test_book_str(self):
        self.assertEqual(str(self.test_book),
                         "Authors: Author Name\nTitle: My Book Title\nPublisher: Publishing Co.")

    def test_book_repr(self):
        self.assertEqual(str(self.test_book),
                         "Authors: Author Name\nTitle: My Book Title\nPublisher: Publishing Co.")


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