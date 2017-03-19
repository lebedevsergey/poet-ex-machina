# -*- coding: utf-8 -*-

# Copyright 2016 Sergey Lebedev
# Licensed under the Apache License, Version 2.0

import os, sys, struct, re, pickle

import includes.keyboard_work as keyboard
import includes.wordforms as wordforms
import includes.utils as utils

class AccentsAndSyllables:

    OLD_BASE_FORMAT_FILE_EXT = '.BSY'	
    NEW_BASE_FORMAT_FILE_EXT = '.syll'

    ACCENTS_DICT_INFO_DIVIDER = ' '
    ACCENTS_DICT_MULTIPLE_ACCENTS_DIVIDER = ","	
    ACCENTS_DICT_FILENAME = "dictonaries/zalizniak.txt"
	
    syllablesAccentsBase = {}
    accentsDict = None
    wordFormsDictObj = None	
	

    def setAccentsAndSyllablesDict_N(self, words):
        """ Automatically sets Accents And Syllables in words base with dictionary"""
        """ changes syllablesAccentsBase according to new accents statistics """		
        if not self.accentsDict:
            self.accentsDict = self.__loadAccentsDict(self.ACCENTS_DICT_FILENAME)
        if not self.wordFormsDictObj:
            self.wordFormsDictObj = wordforms.wordFormsDict()

        for key, word in words.items():			
            word = self.setAccentsAndSyllablesDict(word)

        return words
	
    def setAccentsAndSyllablesAuto_N(self, words):
        """ Automatically sets Accents And Syllables in words base"""
        """ changes syllablesAccentsBase according to new accents statistics """	
        for key, word in words.items():			
            word = self.setAccentsAndSyllablesAuto(word)	
        return words

    def setAccentsAndSyllablesManual_N(self, words):
        """ Allows user to manually set Accents And Syllables in words base """
        """ changes syllablesAccentsBase according to new accents statistics """	
        for key, word in words.items():
            if not self.setAccentsAndSyllablesManual(word):	# Esc was pressed
                return words
        return words

    def setAccentsAndSyllablesDict(self, wordInfo):
        """ sets Accents And Syllables in one word with dictionary"""
        """ changes wordInfo and syllablesAccentsBase according to new accents statistics"""
        if wordInfo['manualAccent']:  # ;а проставлено ли там уже ударение?
            return 

        syllables = utils.Utils.getWordSyllables(wordInfo['word'])
        wordInfo['sylNum'] = len(syllables)		
        if wordInfo['sylNum'] < 1:
            wordInfo['sylNum'] = 1
        if wordInfo['sylNum'] < 2:
            wordInfo['accentSylNum'] = 1  # in one-syllable word accent falls on that unique syllable	 
            return wordInfo

        wordForm = self.wordFormsDictObj.findWordForm(wordInfo['word'])
        if not wordForm:
            return self.setAccentsAndSyllablesAuto(wordInfo)

        accentedLetterNum = self.__getAccentFromDict(wordForm)
        if not accentedLetterNum:
            return self.setAccentsAndSyllablesAuto(wordInfo)

        accentedSyllNum = AccentsAndSyllables.getSyllableNumFromLetterNum(wordForm, accentedLetterNum)
        if wordInfo['sylNum'] >= accentedSyllNum:  # вдруг в словоформе больше слогов, чем в слове
            wordInfo['accentSylNum'] = accentedSyllNum
        else:
            return self.setAccentsAndSyllablesAuto(wordInfo)

        return wordInfo


    def setAccentsAndSyllablesManual(self, wordInfo):
        if wordInfo['manualAccent']:	#;а проставлено ли там уже ударение?
            return True

        if wordInfo['sylNum'] == 0 or wordInfo['accentSylNum'] == 0:
            self.setAccentsAndSyllablesAuto(wordInfo)

        if wordInfo['sylNum'] < 2:
            wordInfo['manualAccent'] = True
            return True

        syllables = utils.Utils.getWordSyllables(wordInfo['word'])		

        curAccentedSylNum = wordInfo['accentSylNum']
        while True:			
            for i, syllable in enumerate(syllables):
                if i == curAccentedSylNum-1:
                    print("|", end="")
                print(syllable, end="")
            sys.stdout.flush()						

            key = keyboard.KeyboardWork.getch()                        
            if keyboard.KeyboardWork.isArrowRightPressed(key):
                curAccentedSylNum = curAccentedSylNum + 1
                if curAccentedSylNum > wordInfo['sylNum']:
                    curAccentedSylNum = wordInfo['sylNum']
            if keyboard.KeyboardWork.isArrowLeftPressed(key):
                curAccentedSylNum = curAccentedSylNum - 1
                if curAccentedSylNum < 1:
                    curAccentedSylNum = 1                                
            if keyboard.KeyboardWork.isBreakKeyPressed(key):
                self.__clearInputLine(len(wordInfo['word']))
                return False
            if keyboard.KeyboardWork.isEnterPressed(key):
                wordInfo['accentSylNum'] = curAccentedSylNum
                wordInfo['manualAccent'] = True
                self.__saveSyllablesAccentStat(syllables, curAccentedSylNum)
                self.__clearInputLine(len(wordInfo['word']))
                return True

            print("\r", end="")
        
    def setAccentsAndSyllablesAuto(self, wordInfo):
        """ sets Accents And Syllables in one word """
        """ changes wordInfo and syllablesAccentsBase according to new accents statistics"""	

        if wordInfo['manualAccent']:	#;а проставлено ли там уже ударение?
            return 

        syllables = self.__addDashes(utils.Utils.getWordSyllables(wordInfo['word']))	

        wordInfo['sylNum'] = len(syllables)
        if wordInfo['sylNum'] < 1:
            wordInfo['sylNum'] = 1
        if wordInfo['sylNum'] < 2:
            wordInfo['accentSylNum'] = 1 		# in one-syllable word accent falls on that unique syllable 	
            return wordInfo

        udar_slog = self.__setAccentAuto(syllables)

        wordInfo['accentSylNum'] = udar_slog
        return wordInfo	

    def loadSyllablesBase(self, fileName):
        filename, file_extension = os.path.splitext(fileName)		
        if file_extension == AccentsAndSyllables.OLD_BASE_FORMAT_FILE_EXT:			
            self.syllablesAccentsBase = AccentsAndSyllables.__loadBaseOldFormat(fileName)
        else:
            self.syllablesAccentsBase = AccentsAndSyllables.__loadBaseNewFormat(fileName)		

    def saveSyllablesBase(self, fileName):		
        file_name, file_extension = os.path.splitext(fileName)        
        if file_extension == AccentsAndSyllables.OLD_BASE_FORMAT_FILE_EXT:			
            file_extension = AccentsAndSyllables.NEW_BASE_FORMAT_FILE_EXT
            fileName = file_name + file_extension 		
        AccentsAndSyllables.__saveBaseNewFormat(self.syllablesAccentsBase, fileName)
        print('База ударений и слогов сохранена в файле ' + fileName)

    @staticmethod
    def getSyllableNumFromLetterNum(word, letterNum):
        if len(word) < letterNum:
            return None

        syllables = utils.Utils.getWordSyllables(word)		
        count = 0
        i = 1
        for syllable in syllables:			
            count = count + len(syllable)
            if letterNum <= count:
                return i
            i = i + 1
        return None

    @staticmethod
    def __loadBaseOldFormat(fileName):
        firstRussianLetterInAscii866 = 0xA0
        lastRussianLetterInAscii866 = 0xFF
        dashAsciiCode = 0x2D

        with open(fileName, mode='rb') as file:
            fileContent = file.read()

        startRecordLen = struct.unpack(str(1) + "B", fileContent[0: 1])[0]
        i = startRecordLen

        syllablesAccentsBase = {}
        k = 0
        while True:
            if i >= len(fileContent):
                break

            recordLen = struct.unpack(str(1) + "B", fileContent[i: i + 1])[0]		
            if recordLen == 0:
                break  # base format error

            s = ''		
            for i2 in range(i, i + recordLen - 3):
                if i2 >= len(fileContent):
                    break									
                if (fileContent[i2] >= firstRussianLetterInAscii866 and fileContent[i2] <= lastRussianLetterInAscii866) or fileContent[i2] == dashAsciiCode:
                    tmp = struct.unpack(str(1) + "s", fileContent[i2: i2 + 1])[0]
                    s = s + tmp.decode('866')

            i = i2 + 1
            accentedSylNum = struct.unpack("B", fileContent[i: i + 1])[0]		
            notAccentedSylNum = struct.unpack("B", fileContent[i + 2: i + 3])[0]		

            syllablesAccentsBase[k] = {
                'slog': s,
                'accStat': [accentedSylNum, notAccentedSylNum]
                }
            i = i + 4		
            k = k + 1

        return syllablesAccentsBase

    @staticmethod
    def __loadBaseNewFormat(fileName):
        with open(fileName, 'rb') as f:
            result = pickle.load(f)
        return result

    @staticmethod
    def __saveBaseNewFormat(syllablesAccentsBase, fileName):		
        with open(fileName, 'wb') as f:
            pickle.dump(syllablesAccentsBase, f)         

    def __setAccentAuto(self, syllables):	
        prognose_STRING = []
        for syllable in syllables:		
            syllable = self.__findSyllable(syllable)
            if syllable:
                accented = float(syllable['accStat'][0])
                unaccented = float(syllable['accStat'][1])
            else:
                accented = 0
                unaccented = 0

            if (unaccented == accented) or (accented + unaccented == 0):
                probability = 0.0
                continue
            else:
                probability = accented / (accented + unaccented)		

            prognose_STRING.append(probability)

        best_prognose = 0.0
        udar_slog = 1
        slogCount = 1
        for prognose in prognose_STRING:
            if best_prognose < prognose:
                best_prognose = prognose
                udar_slog = slogCount
            slogCount = slogCount + 1	

        return udar_slog

    def __saveSyllablesAccentStat(self, syllables, accentedSylNum):		
        tmpSyllables = self.__addDashes(syllables)
        for i,syllable in enumerate(tmpSyllables):
            
            syllableStatRecord = self.__findSyllable(syllable)
            if not syllableStatRecord:
                syllableStatRecord = self.__addSyllableToBase(syllable)

            if i == accentedSylNum-1:
                syllableStatRecord['accStat'][0] = syllableStatRecord['accStat'][0] + 1  
            else:
                syllableStatRecord['accStat'][1] = syllableStatRecord['accStat'][1] + 1

    def __clearInputLine(self, lenToClear):
        print("\r", end='')
        print(' ' * (lenToClear + 1) + "\r", end='')

    def __findSyllable(self, syllableToFind):		
        for key, syllable in self.syllablesAccentsBase.items():				
            if syllable['slog'] == syllableToFind:
                return syllable
        return None

    def __addSyllableToBase(self, syllable):
        newItemIndex = len(self.syllablesAccentsBase) 
        self.syllablesAccentsBase[newItemIndex] = ({'slog': syllable,
                                                   'accStat': [0, 0]})
        return self.syllablesAccentsBase[newItemIndex] 		

    # добавляет дефисы к слогам, что дает указание на их раположение в слове - в начале/конце/середине
    def __addDashes(self, syllables):		
        resultSyllables = []
        tmpSyllable = {}		
        for i in range(0, len(syllables)):
            if i == 0:
                tmpSyllable = syllables[i] + '-'
            elif i == len(syllables)-1:
                tmpSyllable = '-' + syllables[i]
            else:
                tmpSyllable = '-' + syllables[i] + '-'
            resultSyllables.append(tmpSyllable)

        return resultSyllables

    def __getAccentFromDict(self, word):	
        if word in self.accentDict:
            return self.accentDict[word]
        return None

    def __loadAccentsDict(self, filename):
        with open(filename, 'r', encoding='cp1251') as f:
            s = f.read()	

        lines = re.split("\n", s)			   
        self.accentDict = {}	
        for i, s1 in enumerate(lines):
            s1 = s1.strip()
            if not s1:
                continue
            wordDictInfo = re.split(self.ACCENTS_DICT_INFO_DIVIDER, s1)
            wordDictInfo = list(filter(None, wordDictInfo))
            if wordDictInfo[1].find(".") != -1:
                mainAccent = re.split("\.", wordDictInfo[1])[0]
            elif wordDictInfo[1].find(self.ACCENTS_DICT_MULTIPLE_ACCENTS_DIVIDER) != -1:
                mainAccent = re.split(self.ACCENTS_DICT_MULTIPLE_ACCENTS_DIVIDER, wordDictInfo[1])[0]
            else:
                mainAccent = wordDictInfo[1] 

            self.accentDict[wordDictInfo[0]] = int(mainAccent)
