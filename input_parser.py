#!/usr/bin/env python3

import sys
import re

class InputReader:
    """ This class stores the content of a selected file as a
    string and provides some string-manipulation methods. """
    def __init__(self, filename):
        self.filename = filename
        self.parse_success = True
        """ Calling every method as long as no error occurs. """
        try:
            self.reading_file()
            self.incomp_group_check()
            self.del_comments()
            self.empty_group_check()
            self.clear_interspace()
            self.del_emptylines()
            self.del_whitespace()
            self.groupseperate()
            self.groupsplit()
            self.convert_dict()
        except Exception:
            self.parse_success = False


    def reading_file(self):
        """ Storing content of selected file in an attribute of the instance. """
        try:
            with open(self.filename, 'r') as f:
                self.content = f.read()
        except FileNotFoundError:
            print('Selected file was not found!')
            raise Exception

    def incomp_group_check(self):
        """ Checking for any incomplete groups. """
        if re.findall('@(?!end[\s])[^@]*@(?!end(?![\w]))|@end\s[^@]*@end(?![\w])', self.content) != []:
            print('There is at least one incomplete group in the input-file!')
            raise Exception

    def empty_group_check(self):
        """ Checking for any empty groups. """
        if re.findall('@\s*\w*\s*@end(?![\w])', self.content) != []:
            print('There is at least one empty group in the input-file!')
            raise Exception

    def del_comments(self):
        """ Deleting comments (marked by '!'). """
        self.content = re.sub('!.*', '', self.content)

    def clear_interspace(self):
        """ Deleting content, that's not within a group. """
        self.content = re.sub('@end\s[^@]*@', '@end\n@', self.content)

    def del_emptylines(self):
        """ Deleting empty lines. """
        self.content = self.content.strip()
        self.content = re.sub('\n\s*\n', '\n', self.content)

    def del_whitespace(self):
        """ Deleting unnecassary whitespace. """
        self.content = re.sub(' +', ' ', self.content)
        self.content = re.sub('\n +', '\n', self.content)
        self.content = re.sub(' +\n', '\n', self.content)

    def groupseperate(self):
        """ Creating a list with every group as an element. """
        self.grouplist = re.findall('@(?!end[\s])\s*\w+[^@]*@end(?![\w])', self.content)

    def groupsplit(self):
        """ Splitting every element(group) into a list with every
        line as an element, while deleting '@' and '@end' tags. """
        j = 0
        for m in self.grouplist:
            self.grouplist[j] = self.grouplist[j].lstrip('@ \n')
            self.grouplist[j] = self.grouplist[j].rstrip('end\n')
            self.grouplist[j] = self.grouplist[j].rstrip('\n@')
            self.grouplist[j] = self.grouplist[j].split('\n')
            j += 1

    def convert_dict(self):
        """ Converting the list of lists into a dictionary with groupnames as keys. """
        self.groupdict = {}
        for n in self.grouplist:
            self.groupdict[n[0]] = (n[1:])

if __name__ == '__main__':
    # Reading the filename manually from the command prompt:    
    try:
        filename = str(sys.argv[1])
    except IndexError:
        print('Please select an input-file following this scheme:')
        print('python input_reader_class.py <input-file>')
        sys.exit()
    
    # Checking for the right extension (.inp):
    if filename.endswith('.inp'):
        pass
    else:
        print('Selected file is either not an input-file or has the wrong extension!')
        sys.exit()

    # Creating an instance of the InputReader class:
    fn = InputReader(filename)
    
    if fn.parse_success:
        print(fn.groupdict)

