#!/usr/bin/env python3

# This module provides an input reader for input-files.

# imports:
import sys
import re

# Reading filename to a variable, if selected:
try:
    filename = str(sys.argv[1])
except IndexError:
    print('Please select an input-file following this scheme:')
    print('python input_reader.py <input-file>')
    exit()

# Checking if input-file is actually an input-file:
if filename.endswith('.inp'):
    pass
else:
    print('Selected file is either not an input-file or has the wrong extension!')
    exit()

# Reading the input-file and store it as a string:
print('Reading input-file...')
try:
    with open(filename, 'r') as f:
        content = f.read()
except FileNotFoundError:
    print('Selected file was not found.')
    exit()

# Checking if there are any incomplete groups:
incom_group = re.compile('@(?!end)[\w\s:.-/!]*@(?!end)')
if incom_group.findall(content) != []:
    print('There is at least one incomplete group in the input-file!')
    exit()

# Checking if there are any empty groups:
empty_group = re.compile('@\s*@end')
if empty_group.findall(content) != []:
    print('There is at least one empty group in the input-file!')
    exit()

#i = 0
#newgroup = True
#for j in content:
#    if j == '@':
#        i += 1
#        if newgroup == True:
#            for k in content[(i):-1]:
#                if k == '\n' or k == ' ':
#                    continue
#                elif k != '@':
#                    newgroup = False
#                    break
#                else:
#                    print('There is at least one empty group in the input-file!')
#                    exit()
#        else:
#            newgroup = True
#    else:
#        i += 1
#        continue

# General formatting of the input-string:
# Getting rid of comments:
comment = re.compile('![ \w:.-/]*\n')
content = comment.sub('\n',content)
# Getting rid of content between groups:
cleargroupspace = re.compile('@end[\s\w:.-/]*@')
content = cleargroupspace.sub('@end\n@',content)
# Getting rid of empty lines:
content = content.strip()
delemptylines = re.compile('\n\s*\n')
content = delemptylines.sub('\n',content)
# Getting rid of unnecassary whitespace:
delwhitespace = re.compile(' +')
content = delwhitespace.sub(' ',content)
delwhitespace_bol = re.compile('\n +')
content = delwhitespace_bol.sub('\n',content)
delwhitespace_eol = re.compile(' +\n')
content = delwhitespace_eol.sub('\n',content)

# Splitting string into a list of groups using a regular expression:
groupsplit = re.compile('@[\s\w:.\-\/]*\w+[\s\w:.\-\/]*@end')
grouplist = groupsplit.findall(content) 

# Formatting and splitting every element of the list of groups into lists themselves:
j = 0
for m in grouplist:
    grouplist[j] = grouplist[j].lstrip('@')
    grouplist[j] = grouplist[j].rstrip('\n@end')
    grouplist[j] = grouplist[j].split('\n')
    j += 1

print(grouplist)

