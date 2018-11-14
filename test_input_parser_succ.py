#!/usr/bin/env python3

#test_input_parser.py

import unittest
from input_parser import InputParser

class TestInputParser(unittest.TestCase):
    """ This is a test class for testing the input_parser module. """
    def test_input_parser(self):
        instance = InputParser('test_succ.inp')
        res = str(instance.grouplist)
        with open('test_succ.out', 'r') as f:
            raw = f.read()
            exp = raw.rstrip('\n')
        self.assertEqual(exp, res)
        self.assertTrue(instance.parse_success)

if __name__ == '__main__':
    unittest.main()
