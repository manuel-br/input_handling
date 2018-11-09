#!/usr/bin/env python3

#test_input_conparse.py

import unittest
from input_conparse import InputReader

class TestInputReader(unittest.TestCase):
    """ This is a test class for testing the input_conparse module. """

    def test_input_reader_class(self):
        instance = InputReader('test_pars_succ.inp')
        res = str(instance.content)
        with open('test_pars_succ.out', 'r') as f:
            raw = f.read()
            exp = raw.rstrip('\n')
        self.assertEqual(exp, res)
        self.assertTrue(instance.parse_success)

if __name__ == '__main__':
    unittest.main()
