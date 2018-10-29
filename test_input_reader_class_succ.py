#!/usr/bin/env python3

#test_input_reader_class.py

import unittest
from input_reader_class import InputReader

class TestInputReader(unittest.TestCase):
    """ This is a test class for testing the input_reader module. """

    def test_input_reader_class(self):
        instance = InputReader('test_succ.inp')
        res = str(instance.grouplist)
        with open('test_succ.out', 'r') as f:
            raw = f.read()
            exp = raw.rstrip('\n')
        self.assertEqual(exp, res)
        self.assertTrue(instance.parse_success)

if __name__ == '__main__':
    unittest.main()
