#!/usr/bin/env python3

import sys
import re

class InputParser:
    """ This class stores the content of a selected VeloxChem input file
    as a string and provides some string-manipulation methods. """
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
            self.lowercase_content()
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
        if re.findall('@[\w ]*\n\s*@end(?![\w])', self.content) != []:
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

    def lowercase_content(self):
        """ Lowercasing every alphabetical charakter. Atom labels will be
        uppercased when the dictionary is created. """
        self.content = self.content.lower()

    def groupseperate(self):
        """ Creating a list with every group as an element. """
        self.grouplist = re.findall('@(?!end[\s])\s*\w+[^@]*@end(?![\w])', self.content)

    def groupsplit(self):
        """ Splitting every element(group) into a list with every
        line as an element, while deleting '@' and '@end' tags. """
        i = 0
        for entry in self.grouplist:
            self.grouplist[i] = self.grouplist[i].lstrip('@ \n')
            self.grouplist[i] = self.grouplist[i].rstrip('end\n')
            self.grouplist[i] = self.grouplist[i].rstrip('\n@')
            self.grouplist[i] = self.grouplist[i].split('\n')
            i += 1

    def convert_dict(self):
        """ Converting the list of lists into a dictionary with groupnames as keys
        and group content as a dictionary itself. The geometry definition of the
        molecule group is stored in a different dictionary. """
        self.groupdict = {}
        self.moldict = {}
        l = 1
        for j in self.grouplist:
            inner_dic = {}
            for k in j[1:]:
                if ':' in k and 'xyz' not in k:
                    inner_dic[k.split(':')[0].strip()] = k.split(':')[1].strip()
                elif j[0] != 'molecule':
                    inner_dic[k.strip()] = None
                elif 'xyz' in k:
                    pass
                else:
                    self.moldict[l] = k.strip().upper()
                    l += 1
            self.groupdict[j[0]] = inner_dic
            self.moldict['atoms'] = l-1


if __name__ == '__main__':
    # Reading the filename manually from the command prompt:    
    try:
        filename = str(sys.argv[1])
    except IndexError:
        print('Please select an input-file following this scheme:')
        print('python input_parser.py <input-file>')
        sys.exit()
    
    # Checking for the right extension (.inp):
    if filename.endswith('.inp'):
        pass
    else:
        print('Selected file is either not an input-file or has the wrong extension!')
        sys.exit()

    # Creating an instance of the InputParser class:
    fn = InputParser(filename)
    
    if fn.parse_success:
        print('Groups and keywords with values: ', fn.groupdict)
        print('\nNumber of atoms, type and xyz coordinates: ', fn.moldict)

