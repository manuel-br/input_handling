#!/usr/bin/env python3

import sys
import re
import configparser

class InputReader:
    """ This class parses VeloxChem input files (in INI format)
    using the built-in configparser package in python. """
    def __init__(self, filename):
        self.filename = filename
        self.parse_success = True
        """ Calling every method as long as no error occurs. """
        try:
            self.reading_file()
            self.del_comments()
            self.del_emptylines()
            self.del_whitespace()
            self.indent_values()
            self.parsing()
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
    
    def del_comments(self):
        """ Deleting comments (marked by '!' or '#'). """
        self.content = re.sub('!.*|#.*', '', self.content)

    def del_emptylines(self):
        """ Deleting empty lines. """
        self.content = self.content.strip()
        self.content = re.sub('\n\s*\n', '\n', self.content)

    def del_whitespace(self):
        """ Deleting unnecassary whitespace. """
        self.content = re.sub(' +', ' ', self.content)
        self.content = re.sub('\n +', '\n', self.content)
        self.content = re.sub(' +\n', '\n', self.content)

    def indent_values(self):
        """ Handles Indentation of multiline values. """
        lines = self.content.split('\n')
        noindent = re.compile('[:=\[]')
        index = 0
        for i in lines:
            if noindent.findall(i) == []:
                lines[index] = ' ' + lines[index]
            index += 1
        self.content = '\n'.join(lines)
        
    def parsing(self):
        """ Parsing of the selected input file. """
        try: 
            self.config = configparser.ConfigParser()
            self.config.read_string(self.content)
        except:
            print('Something is wrong with the input.')
            raise Exception

if __name__ == '__main__':
    # Reading the filename manually from the command prompt:
    try:
        filename = str(sys.argv[1])
    except IndexError:
        print('Please select an input-file following this scheme:')
        print('python input_conparse.py <input-file>')
        sys.exit()
   
    # Checking for the right extension (.inp):
    if filename.endswith('.inp'):
        pass
    else:
        print('Selected file is either not an input-file or has the wrong extension!')
        sys.exit()

    # Creating an instance of the InputReader class:
    fn = InputReader(filename)
    
    # Printing sections, values and keys in case of successful parsing:
    if fn.parse_success:
        for section in fn.config.sections():
            print(f'\n{section}')
            for k, v in fn.config[section].items():
                print(f' {k} = {v}')
