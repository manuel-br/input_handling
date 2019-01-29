#!/usr/bin/env python3


import sys
import re


class InputParser:
    """ Provides functions for parsing VeloxChem input files into a format,
    which passes the needed information to the rest of the program """

    def __init__(self, filename):
        """ Initializes parsing process by setting monitor value to TRUE """

        self.success_monitor = True

        self.filename = filename

    # defining main functions

    def parse(self):
        """ Calls every function needed for the parsing process depending on
        the success of the parsing in different stages """

        try:

            # reading selected file

            self.reading_file()

            # checking for syntax correctness of the input file

            self.incomp_group_check()
            self.empty_group_check()

        except FileNotFoundError:
            print('Selected file was not found!')
            self.success_monitor = False

        except SyntaxError:
            print(
            'Selected input file has bad syntax! You may check for incomplete or empty groups.')
            self.success_monitor = False

        if self.success_monitor:

            # manipulation of input string

            self.del_comments()
            self.clear_interspace()
            self.del_whitespace()
            self.lowercase_content()

            # processing the data into lists and dictionaries

            self.groupsplit()
            self.convert_dict()
            self.convert_moldict()

            if self.input_dict['molecule']['units'] == 'angs':

                # converting angstroms to atomic units

                self.convert_units()

            return self.input_dict

    def parse_success(self):
        """ Performing the parsing process and returning monitor value. """

        self.parse()
        return self.success_monitor

    # defining subordinated functions

    def reading_file(self):
        """ Storing content of selected file as a string type """

        with open(self.filename, 'r') as f:
            self.content = f.read()

    def incomp_group_check(self):
        """ Checking for any incomplete groups. """

        if re.findall(r'@(?!end[\s])[^@]*@(?!end(?![\w]))|@end\s[^@]*@end(?![\w])', self.content) != []:
            raise SyntaxError

    def empty_group_check(self):
        """ Checking for any empty groups. """

        if re.findall(r'@[\w ]*\n\s*@end(?![\w])', self.content) != []:
            raise SyntaxError

    def del_comments(self):
        """ Deleting comments (marked by '!'). """

        self.content = re.sub('!.*', '', self.content)

    def clear_interspace(self):
        """ Deleting content, that's not within a group. """

        self.content = re.sub(r'@end\s[^@]*@', '@end\n@', self.content)

    def del_whitespace(self):
        """ Deleting unnecassary whitespace. """

        self.content = self.content.strip()
        self.content = re.sub(r'\n\s*\n', '\n', self.content)
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

        self.grouplist = re.findall(r'@(?!end[\s])\s*\w+[^@]*@end(?![\w])', self.content)
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

        self.input_dict = {}
        self.moldict = {}
        q = 1
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
                    self.moldict[q] = k.strip().upper()
                    q += 1
            self.input_dict[j[0]] = inner_dic

    def convert_moldict(self):
        """ Converting the molecular structure into the format required for calculations. """

        self.input_dict['molecule']['atom_labels'] = []
        self.input_dict['molecule']['x_coords'] = []
        self.input_dict['molecule']['y_coords'] = []
        self.input_dict['molecule']['z_coords'] = []
        for m in self.moldict.keys():
            self.input_dict['molecule']['atom_labels'].append(self.moldict[m].split()[0])
            self.input_dict['molecule']['x_coords'].append(float(self.moldict[m].split()[1]))
            self.input_dict['molecule']['y_coords'].append(float(self.moldict[m].split()[2]))
            self.input_dict['molecule']['z_coords'].append(float(self.moldict[m].split()[3]))

    def convert_units(self):
        """ Converting molecule coordinates form angstroms to atomic units. """

        coords = ['x_coords', 'y_coords', 'z_coords']

        for n in coords:
            for p in range(len(self.input_dict['molecule'][n])):
                self.input_dict['molecule'][n][p] = self.input_dict['molecule'][n][p] / 0.52917721092


if __name__ == '__main__':
    try:

        # Reading the filename manually from the command prompt:

        filename = str(sys.argv[1])

        # Calling the .parse method of the InputParser class:

        input_dict = InputParser(filename).parse()

        if input_dict is not None:
            print('Groups and keywords with values: ', input_dict)

    except IndexError:
        print('Please select an input-file following this scheme:')
        print('python3 input_parser.py <input-file>')
        sys.exit()
