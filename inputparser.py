#!/usr/bin/env python3

import sys
import re

class InputParser:
    """ Docstring here """
    def __init__(self, filename):
        self.filename = filename
        self.parse_success = True

        try:

            # reading selected file

            self.reading_file()

            # checking for syntax correctness of the input file

            self.incomp_group_check()
            self.empty_group_check()

        except FileNotFoundError:
            print('Selected file was not found!')
            self.parse_success = False

        except SyntaxError:
            print('Selected input file has bad syntax! You may check for incomplete or empty groups.')
            self.parse_success =  False

        if self.parse_success:

            # manipulation of input string

            self.del_comments()
            self.clear_interspace()
            self.del_whitespace()
            self.lowercase_content()

            # processing the data into lists and dictionaries

            self.groupsplit()
            self.convert_dict()
            #self.check_moldict()
            self.convert_moldict()

    # Definition of functions

    def reading_file(self):
        """ Storing content of selected file as a string type """

        with open(self.filename, 'r') as f:
            self.content = f.read()

    def incomp_group_check(self):
        """ Checking for any incomplete groups. """

        if re.findall('@(?!end[\s])[^@]*@(?!end(?![\w]))|@end\s[^@]*@end(?![\w])', self.content) != []:
            raise SyntaxError

    def empty_group_check(self):
        """ Checking for any empty groups. """

        if re.findall('@[\w ]*\n\s*@end(?![\w])', self.content) != []:
            raise SyntaxError

    def del_comments(self):
        """ Deleting comments (marked by '!'). """

        self.content = re.sub('!.*', '', self.content)

    def clear_interspace(self):
        """ Deleting content, that's not within a group. """

        self.content = re.sub('@end\s[^@]*@', '@end\n@', self.content)

    def del_whitespace(self):
        """ Deleting unnecassary whitespace. """

        self.content = self.content.strip()      
        self.content = re.sub('\n\s*\n', '\n', self.content)
        self.content = re.sub(' +', ' ', self.content)
        self.content = re.sub('\n +', '\n', self.content)
        self.content = re.sub(' +\n', '\n', self.content)

    def lowercase_content(self):
        """ Lowercasing every alphabetical character. Atom labels will be
        uppercased when the dictionary is created. """

        self.content = self.content.lower()

    def groupsplit(self):
        """ Creating a list in which every element is a list itself containing every line
        of a group, while deleting '@' and '@end' tags. """

        self.grouplist = re.findall('@(?!end[\s])\s*\w+[^@]*@end(?![\w])', self.content)
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

    def check_moldict(self):
        """ Checking if there are any information about the strucutre in the
        moldict dictionary. """

        if self.moldict != {}:
            self.direct_parsing = True
        else:
            self.direct_parsing = False

    def convert_moldict(self):
        """ Converting the molecular structure into the format required for calculations. """

        self.atom_labels = []
        self.x_coords = []
        self.y_coords = []
        self.z_coords = []
        for j in self.moldict.keys():
            self.atom_labels.append(self.moldict[j].split()[0])
            self.x_coords.append(self.moldict[j].split()[1])
            self.y_coords.append(self.moldict[j].split()[2])
            self.z_coords.append(self.moldict[j].split()[3])
        print(self.atom_labels, self.x_coords, self.y_coords, self.z_coords)



if __name__ == '__main__':

    # Reading the filename manually from the command prompt:
    
    try:
        filename = str(sys.argv[1])
    except IndexError:
        print('Please select an input-file following this scheme:')
        print('python3 input_parser.py <input-file>')
        sys.exit()
 
 # Creating an instance of the InputParser class:
    fn = InputParser(filename)

    if fn.parse_success:
        print('Groups and keywords with values: ', fn.groupdict)
        print('\nNumber of atoms, type and xyz coordinates: ', fn.moldict)


