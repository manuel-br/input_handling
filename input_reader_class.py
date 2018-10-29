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
        self.reading_file()
        if self.parse_success == True:
            self.incomp_group_check()
            if self.parse_success == True:
                self.empty_group_check()
                if self.parse_success == True:
                    self.del_comments()
                    self.clear_interspace()
                    self.del_emptylines()
                    self.del_whitespace()
                    self.groupseperate()
                    self.groupsplit()

    def reading_file(self):
        """ Storing content of selected file in an attribute of the instance: """
        try:
            with open(self.filename, 'r') as f:
                self.content = f.read()
        except FileNotFoundError:
            print('Selected file was not found!')
            self.parse_success = False

    def incomp_group_check(self):
        """ Checking for any incomplete groups: """
        if re.findall('@(?!end)[^@]*@(?!end)|@end[^@]*@end', self.content) != []:
            print('There is at least one incomplete group in the input-file!')
            self.parse_success = False

    def empty_group_check(self):
        """ Checking for any empty groups: """
        if re.findall('@\s*@end', self.content) != []:
            print('There is at least one empty group in the input-file!')
            self.parse_success = False

    def del_comments(self):
        """ Deleting all comments: """
        self.content = re.sub('!.*', '\n', self.content)

    def clear_interspace(self):
        """ Deleting content, that's not within a group: """
        self.content = re.sub('@end[^@]*@', '@end\n@', self.content)

    def del_emptylines(self):
        """ Deleting empty lines: """
        self.content = self.content.strip()
        self.content = re.sub('\n\s*\n', '\n', self.content)

    def del_whitespace(self):
        """ Deleting unnecassary whitespace: """
        self.content = re.sub(' +', ' ', self.content)
        self.content = re.sub('\n +', '\n', self.content)
        self.content = re.sub(' +\n', '\n', self.content)

    def groupseperate(self):
        """ Creating a list with every group as an element: """
        self.grouplist = re.findall('@(?!end)\s*\w+[^@]*@end', self.content)

    def groupsplit(self):
        """ Splitting every element(group) into a list with every
        line as an element, while deleting '@' and '@end' tags: """
        j = 0
        for m in self.grouplist:
            self.grouplist[j] = self.grouplist[j].lstrip('@')
            self.grouplist[j] = self.grouplist[j].rstrip('end')
            self.grouplist[j] = self.grouplist[j].rstrip('\n@')
            self.grouplist[j] = self.grouplist[j].split('\n')
            j += 1

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
    
    if fn.parse_success == True:
        print(fn.grouplist)

