#!/usr/bin/env python3

import sys
from input_parser import InputParser

class MoleculeReader:

    def __init__(self,filename):
        self.parser = InputParser(filename)
        self.xyz_success = True

        #_______________________________________________________________
        self.periodic_table = ['H', 'He', 'Li', 'Be', 'B', 'C', 'N', 'O', 'F', 'Ne', 'Na', 'Mg', 'Al', 'Si', 'P', 'S', 'Cl', 'Ar']
        #_______________________________________________________________

        self.check_xyz_keyword()
        if self.direct_parsing:
            print(self.parser.moldict)
            self.check_moldict()
            self.convert_moldict()

    def check_xyz_keyword(self):
        if self.parser.moldict != {}:
            self.direct_parsing = True
        else:
            self.direct_parsing = False

    def check_moldict(self):
        for i in self.parser.moldict.keys():
            atom = self.parser.moldict[i].split()
            if len(atom) != 4:
                print('The following atom is not properly defined:')
                print(i)
                raise Exception
            if atom[0] not in self.periodic_table:
                print('There is at least one unknown type of elements!')
                raise Exception
            try:
                float(atom[1])
                float(atom[2])
                float(atom[3])
            except TypeError:
                print('There is at least one incorrect coordinate!')
                raise Exception

    def convert_moldict(self):
        self.atom_labels = []
        self.x_coords = []
        self.y_coords = []
        self.z_coords = []
        for j in self.parser.moldict.keys():
            self.atom_labels.append(self.parser.moldict[j].split()[0])
            self.x_coords.append(self.parser.moldict[j].split()[1])
            self.y_coords.append(self.parser.moldict[j].split()[2])
            self.z_coords.append(self.parser.moldict[j].split()[3])
        print(self.atom_labels, self.x_coords, self.y_coords, self.z_coords)
            



if __name__ == '__main__':
    # Reading the filename manually from the command prompt:
    try:
        filename = str(sys.argv[1])
    except IndexError:
        print('Please select an input-file following this scheme:')
        print('python molecule_reader.py <input-file>')
        sys.exit()

    # Creating an instance of the MoleculeReader class:
    molecule = MoleculeReader(filename)

    if molecule.xyz_success:
        print('molecule_reader succeeded!')
    else:
        print('molecule_reader failed!')
            
        

