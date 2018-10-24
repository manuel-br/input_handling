#!/usr/bin/env python3

import sys
import re

class InputReader:
    """ This class stores the content of a selected file as a string initially and provides some string-manipulation methods. """

    def __init__(self, filename):
        self.filename = filename
        try:
            with open(self.filename, 'r') as input:
                self.content = input.read()
        except FileNotFoundError:
            print('Selected file was not found!')

    def incomp_group_check(self):
        incomp_group = re.compile('@(?!end)[\w\s:.-/!]*@(?!end)')
        if incomp_group.findall(self.content) != []:
            print('There is at least one incomplete group in the input-file!')
            exit()

    def empty_group_check(self):
        empty_group = re.compile('@\s*@end')
        if empty_group.findall(self.content) != []:
            print('There is at least one empty group in the input-file!')
            exit()

    def del_comments(self):
        comment = re.compile('![ \w:.-/]*\n')
        self.content = comment.sub('\n',self.content)

    def clear_interspace(self):
        interspace = re.compile('@end[\s\w:.-/]*@')
        self.content = interspace.sub('@end\n@',self.content)

    def del_emptylines(self):
        self.content = self.content.strip()
        emptyline = re.compile('\n\s*\n')
        self.content = emptyline.sub('\n',self.content)

    def del_whitespace(self):
        whitespace = re.compile(' +')
        self.content = whitespace.sub(' ',self.content)
        whitespace_bol = re.compile('\n +')
        self.content = whitespace_bol.sub('\n',self.content)
        whitespace_eol = re.compile(' +\n')
        self.content = whitespace_eol.sub('\n',self.content)

    def groupseperate(self):
        group = re.compile('@[\s\w:.\-\/]*\w+[\s\w:.\-\/]*@end')
        self.grouplist = group.findall(self.content)

    def groupsplit(self):
        j = 0
        for m in self.grouplist:
            self.grouplist[j] = self.grouplist[j].lstrip('@')
            self.grouplist[j] = self.grouplist[j].rstrip('\n@end')
            self.grouplist[j] = self.grouplist[j].split('\n')
            j += 1



if __name__ == '__main__':
    
    check = True
    try:
        filename = str(sys.argv[1])
    except IndexError:
        print('Please select an input-file following this scheme:')
        print('python input_reader_class.py <input-file>')
        exit()

    if filename.endswith('.inp'):
        pass
    else:
        print('Selected file is either not an input-file or has the wrong extension!')
        exit()

    fn = InputReader(filename)

    fn.incomp_group_check()

    fn.empty_group_check()

    fn.del_comments()

    fn.clear_interspace()

    fn.del_emptylines()

    fn.del_whitespace()

    fn.groupseperate()

    fn.groupsplit()

    print(fn.grouplist)

