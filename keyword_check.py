#!/usr/bin/env python3

import sys
from input_parser import InputParser

class KeywordCheck:
    """ This class provides functions for evaluating the content correctness of
    VeloxChem input files. """
    def __init__(self,filename):
        self.inst = InputParser(filename)
        self.check_success = True

#___________________________________________________________________________
        # Defining mandatory and optional groups. For future reference this
        # information might be stored externally in some library:
        self.m_groups = ['jobtype', 'method settings', 'molecule']
        self.o_groups = ['specifications', 'testgroup']
        # Defining mandatory and optional keywords. For future reference this
        # information might be stored externally in some library:
        self.jobtype_m_keywords = ['task', 'method']
        self.jobtype_o_keywords = ['correlation']
        self.method_settings_m_keywords = []
        self.method_settings_o_keywords = ['functional']
        self.molecule_m_keywords = ['charge', 'multiplicity', 'basis']
        self.molecule_o_keywords = []
        self.specifications_m_keywords = ['kind']
        self.specifications_o_keywords = ['stepsize', 'print']
        # Defining possible string type values for every keyword:
        self.values = {'task': ['geometry', 'geometry optimization', 'single point'], 'method': ['hartree-fock', 'hf', 'adc(1)', 'adc(2)', 'dft'], 'functional': ['b3lyp', 'pbe'], 'basis': ['def-pvdz'], 'kind': ['kind1', 'kind2'], 'stepsize': range(1000), 'print': range(10), 'charge': range(20), 'multiplicity': range(10)}
        # Defining keywords which require values (no default set):
        self.keywords_m_values = ['task', 'method', 'functional', 'charge', 'multiplicity', 'basis']
#___________________________________________________________________________

        try:
            # Checking if there are any unknown ...
            
            # ... groupnames:
            self.unknown_routine(self.inst.groupdict.keys(), self.m_groups, self.o_groups, 'There is at least one unknown group!')
            # ... keywords in the jobtype group: 
            self.unknown_routine(self.inst.groupdict['jobtype'].keys(), self.jobtype_m_keywords, self.jobtype_o_keywords, 'There is at least one unknown keyword in the jobtype group!')
            # ... keywords in the method settings group:
            self.unknown_routine(self.inst.groupdict['method settings'].keys(), self.method_settings_m_keywords, self.method_settings_o_keywords, 'There is at least one unknown keyword in the method settings group!')
            # ... keywords in the molecule group:
            self.unknown_routine(self.inst.groupdict['molecule'].keys(), self.molecule_m_keywords, self.molecule_o_keywords, 'There is at least one unknown keyword in the molecule group!')
            # ... keywords in the specifications group:
            if 'specifications' in self.inst.groupdict.keys():
                self.unknown_routine(self.inst.groupdict['specifications'].keys(), self.specifications_m_keywords, self.specifications_o_keywords, 'There is at least one unknown keywords in the specifications group!')

            # Checking if there are any mandatory ...

            # ... groups missing:
            self.mandatory_routine(self.inst.groupdict.keys(), self.m_groups, 'At least one mandatory group is not defined!')
            # ... keywords in the jobtype group missing:
            self.mandatory_routine(self.inst.groupdict['jobtype'].keys(), self.jobtype_m_keywords, 'At least one mandatory keyword is not defined in the jobtype group!')
            # ... keywords in the method settings group missing:
            self.mandatory_routine(self.inst.groupdict['method settings'].keys(), self.method_settings_m_keywords, 'At least one mandatory keyword is not defined in the method settings group!')
            # ... keywords in the molecule group missing:
            self.mandatory_routine(self.inst.groupdict['molecule'].keys(), self.molecule_m_keywords, 'At least one mandatory keyword is not defined in the molecule group!')
            # ... keywords in the specifications group missing:
            if 'specifications' in self.inst.groupdict.keys():
                self.mandatory_routine(self.inst.groupdict['specifications'].keys(), self.specifications_m_keywords, 'At least one mandatory keyword is not defined in the specifications group!')

            # Checking if there is a value set for every keyword that requires one:
            self.required_values(self.inst.groupdict, self.keywords_m_values, 'There is at least one keyword without required value!')

            # Checking if the values are set properly:
            self.unvalid_values()

        except Exception:
            self.check_success = False

    def unknown_routine(self, keywords, m_list, o_list, error_message):
        for i in keywords:
            if i not in m_list and i not in o_list:
                print(error_message)
                raise Exception

    def mandatory_routine(self, keywords, m_list, error_message):
        for j in m_list:
            if j not in keywords:
                print(error_message)
                raise Exception

    def required_values(self, dictionary, values, error_message):
        for k in dictionary.keys():
            for l in dictionary[k].keys():
                if l in values and dictionary[k][l] == None:
                    print(error_message)
                    raise Exception

    def unvalid_values(self):
        for m in self.inst.groupdict.keys():
            for n in self.inst.groupdict[m].keys():
                if self.inst.groupdict[m][n] not in self.values[n] and self.inst.groupdict[m][n] != None:
                    try:
                        if int(self.inst.groupdict[m][n]) not in self.values[n]:
                            raise Exception
                    except:
                        print('The value set for the <', n, '> keyword is unvalid!')
                        raise Exception

if __name__ == '__main__':
    # Reading the filename manually from the command prompt:
    try:
        filename = str(sys.argv[1])
    except IndexError:
        print('Please select an input-file following this scheme:')
        print('python keyword_check.py <input-file>')
        sys.exit()

    # Checking for the right extension (.inp):
    if filename.endswith('.inp'):
        pass
    else:
        print('Selected file is either not an input-file or has the wrong extension!')
        sys.exit()

    # Creating an instance of the KeywordCheck class:
    check = KeywordCheck(filename)
    
    if check.check_success:
        print('keyword_check succeeded!')
    else:
        print('keyword_check failed!')
