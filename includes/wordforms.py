# -*- coding: utf-8 -*-

# Copyright 2016 Sergey Lebedev
# Licensed under the Apache License, Version 2.0


import re

class wordFormsDict:
    
    WORD_FORMS_DATA_DIVIDER = ','
    WORD_FORMS_FILE = "dictonaries/odict.csv"
    
    wordForms = {}
    wordMainForms = {}    
    
    def __init__(self):
        self.__loadDict(self.WORD_FORMS_FILE)

    def findWordForm(self, wordForm):    
        if wordForm in self.wordForms:
            return self.wordForms[wordForm]
        return None
    
    def __loadDict(self, filename):                
        with open(filename, 'r', encoding='cp1251') as f:        
            count = 0
            while True:
                line = f.readline()
                line = line.strip()
                if not line:
                    break            
                data = re.split(self.WORD_FORMS_DATA_DIVIDER, line)
                self.wordMainForms[count] = data[0]            
                mainForm = self.wordMainForms[count]
                count = count + 1
                self.wordForms[data[0]] = mainForm

                if len(data) <= 2:
                    continue

                for i in range(2, len(data)):
                    self.wordForms[data[i]] = mainForm