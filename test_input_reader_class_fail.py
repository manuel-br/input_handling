#!/usr/bin/env python3

#test_input_reader_class.py

import unittest
from input_reader_class import InputReader

class TestInputReader(unittest.TestCase):
    """ This is a test class for testing the input_reader module. """
    def test_input_reader_class(self):
        instance = InputReader('test_fail.inp')
        self.assertFalse(instance.parse_success)

if __name__ == '__main__':
    unittest.main()
