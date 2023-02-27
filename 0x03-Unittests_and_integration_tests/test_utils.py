#!/usr/bin/env python3
"""
Test class for utils.py
"""
import unittest
from unittest.mock import patch, MagicMock
from parameterized import parameterized
access_nested_map = __import__("utils").access_nested_map
get_json = __import__("utils").get_json
requests = __import__("utils").requests
memoize = __import__("utils").memoize


class TestAccessNestedMap(unittest.TestCase):
    """
    Test class for utils.py
    """
    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {'b': 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2)
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """ Test for the test_access_nested_map method """
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b"))
    ])
    def test_access_nested_map_exception(self, nested_map, path):
        """
        Test if key error is raised for the test_access_nested_map method
        """
        with self.assertRaises(KeyError):
            access_nested_map(nested_map, path)


class TestGetJson(unittest.TestCase):
    """
    Test the get json method of utils
    """
    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False})
    ])
    def test_get_json(self, test_url, test_payload):
        """test_get_json"""
        with patch('requests.get') as mock_get:
            # Mock response object.
            # Mocking an instance of the Response class
            mock_response = MagicMock()
            mock_response.json.return_value = test_payload

            # requests.get returns an instance of the response
            # class, we assign the mocked response object
            mock_get.return_value = mock_response
            payload = get_json(test_url)
        self.assertEqual(payload, test_payload)


class TestMemoize(unittest.TestCase):
    """
    Test the memoize method of utils
    """
    def test_memoize(self):
        """
        method that tests memoize
        """

        class TestClass:
            """
            Class for testing purpose
            """
            def a_method(self):
                """a_method"""
                return 42

            @memoize
            def a_property(self):
                """a_property"""
                return self.a_method()

        prop_inst = TestClass()
        with patch.object(TestClass, 'a_method') as mock_get:
            mock_get.return_value = 32
            value = prop_inst.a_property
            value = prop_inst.a_property
            self.assertEqual(value, 32)
            mock_get.assert_called_once()
