# -*- coding: utf-8 -*-

# Copyright 2016 Sergey Lebedev
# Licensed under the Apache License, Version 2.0

import includes.utils as utils
import os, struct, pickle

class WordBaseWork:
    OLD_BASE_FORMAT_FILE_EXT = '.BSY'	
    NEW_BASE_FORMAT_FILE_EXT = '.words'
	
    allText = ''
    curTextSymPtr = 0
    last_ASSO = None
    new_ASSO = False
    words = {}	

    @staticmethod
    def loadWordBase(fileName):
        filename, file_extension = os.path.splitext(fileName)		
        if file_extension == WordBaseWork.OLD_BASE_FORMAT_FILE_EXT:			
            return WordBaseWork.__loadBaseOldFormat(fileName)
        return WordBaseWork.__loadBaseNewFormat(fileName)
	
    @staticmethod
    def saveWordBase(fileName, words):		
        file_name, file_extension = os.path.splitext(fileName)        
        if file_extension == WordBaseWork.OLD_BASE_FORMAT_FILE_EXT:			
            file_extension = WordBaseWork.NEW_BASE_FORMAT_FILE_EXT
            fileName = file_name + file_extension 		
        WordBaseWork.__saveBaseNewFormat(fileName, words)
        print('База слов сохранена в файле ' + fileName)

    def refillBase(self, text):
        self.allText = self.__removeNewLines(text)
        self.curTextSymNum = 0
        self.last_ASSO = None				
			
        while True:
            self.new_ASSO = False		#;не убивать появившихся ассоциаций
            word = self.__getNextWord().lower()
            if not word:
                break
            if len(word) == 1 and not utils.Utils.isOneLetterWord(word[0]):
                self.new_ASSO = True
                continue
				
            curWordIndex = self.__findWord(word)			
            if curWordIndex == None:	
                curWordIndex = self.__addNewWord(word, self.last_ASSO)				
            else:				
                if self.last_ASSO:	
                    self.__addNewAsoc(curWordIndex, self.last_ASSO)
					
            if not self.new_ASSO:
                self.last_ASSO = curWordIndex
            else:
                self.last_ASSO = None
				

        WordBaseWork.__filterRecursiveAssociation(self.words)
        WordBaseWork.__filterInexistingAssociation(self.words)

        return self.words		
	
    @staticmethod
    def getAssoc(word, words):
        result = []		
        tmpList = enumerate(word['assoc'])
        for i, assocWordIndex in tmpList:
            result.append(words[assocWordIndex])
        return result	
	
    @staticmethod
    def findWordByValue(findWord, words):	
        for i, word in words.items():
            if word['word'] == findWord:			
                return i, word
        return False
		
    def __findWord(self, findWord):		
        for i, word in self.words.items():
            if word['word'] == findWord:
                return i
        return None
	
    @staticmethod
    def __filterInexistingAssociation(words):					
        for key, word in words.items():
            for i, assoc in enumerate(word['assoc']):
                if word['assoc'][i] not in words:					
                    words[key]['assoc'].pop(i)					
					
    @staticmethod
    def __filterRecursiveAssociation(words):					
        for key, word in words.items():
            for i, assoc in enumerate(word['assoc']):
                if word['assoc'][i] == key:								
                    raise NameError('Something has gone wrong - recursive association detected', key, word)                                
										
	
    def __addNewAsoc(self, wordIndex, assocIndex):
        if assocIndex  == None:
            return
        if assocIndex == wordIndex:			
            return						#;запретить саму на себя
        if assocIndex in self.words[wordIndex]['assoc']:
            return
				
        self.words[wordIndex]['assoc'].append(assocIndex)		
	
    def __addNewWord(self, word, assoc):
        wordInfo = {
            'word': word, 
            'sylNum': 0,	#not initialized value
            'accentSylNum': 0,	#not initialized value
            'manualAccent':  False,
            'index':  len(self.words),	
            }
        if assoc == None:
            wordInfo['assoc'] = []
        else:
            wordInfo['assoc'] = [assoc]			

        newItemIndex = len(self.words)			
        self.words[len(self.words)] = wordInfo
        return newItemIndex		
	
    def __getNextSym(self):		
        if self.curTextSymPtr > len(self.allText)-1:
            return False
        sym = self.allText[self.curTextSymPtr] 
        self.curTextSymPtr = self.curTextSymPtr + 1
        return sym

    def __getNextWord(self):		
        new_WORD = ''
        while True:
            sym = self.__getNextSym()
            if not sym:
                return ''
            if utils.Utils.isAssocStopSym(sym):
                self.last_ASSO = None
            if utils.Utils.isCyrillicLetter(sym):
                break
		
        while True:
            new_WORD = new_WORD + sym
            sym = self.__getNextSym()	
            if not sym:
                return new_WORD
            if utils.Utils.isAssocStopSym(sym):
                self.new_ASSO = True
            if not utils.Utils.isCyrillicLetter(sym):
                break
				
        return new_WORD
	
    def __removeNewLines(self, text):
        result = text
        self.result = text.replace('-\r\n', '')
        self.result = result.replace('-\r', '')
        self.result = result.replace('-\n', '')
        return result
	
    @staticmethod
    def __loadBaseNewFormat(fileName):
        f = open(fileName, 'rb') 
        return pickle.load(f) 
        f.close()
	
    @staticmethod
    def __saveBaseNewFormat(fileName, words):
        f = open(fileName, 'wb') 
        pickle.dump(words, f) 
        f.close()		
	
    @staticmethod
    def __loadBaseOldFormat(fileName):
        WORDINFO_POINTER_SIZE = 3
	
        with open(fileName, mode='rb') as file:
            fileContent = file.read()
			
        itemsNum = struct.unpack("i", fileContent[:4])[0] & 0xFFFFFF	
		
        pointersTableEndIndex = (itemsNum + 1) * WORDINFO_POINTER_SIZE
        wordPointers = []
        count = 0
        for i in range(3, pointersTableEndIndex, WORDINFO_POINTER_SIZE):
            wordOffset = struct.unpack("i", fileContent[i: (i + 4)])[0] & 0xFFFFFF			
            wordPointers.insert(count, wordOffset)
            count = count + 1  
				
        words = {}
		
        wordsTableStart = pointersTableEndIndex + WORDINFO_POINTER_SIZE
        i = wordsTableStart
			
        count = 0
        while True:				
            wordAddress = i - wordsTableStart
			
            if struct.unpack("B", fileContent[i: i + 1])[0] == 0:
                isManualAccented = False
            else:
                isManualAccented = True
			
            i = i + 1
            assocNum = struct.unpack("B", fileContent[i: i + 1])[0]
            i = i + 1
            sylNum = struct.unpack("B", fileContent[i: i + 1])[0]
            i = i + 1
            accentSylNum = struct.unpack("B", fileContent[i: i + 1])[0]
            i = i + 1
            lettersNum = struct.unpack("B", fileContent[i: i + 1])[0]
            i = i + 1
			
            word = struct.unpack(str(lettersNum) + "s", fileContent[i: i + lettersNum])[0]		
            i = i + lettersNum		
            assoc = []
			
            for j in range(0, assocNum):
                indexAssoc = struct.unpack("<H", fileContent[i + j * 2: i + j * 2 + 2])[0]
                assoc.append(indexAssoc-1)
				
            i = i + assocNum * 2
						
            wordInfo = {'word': word.decode('866'),
                'manualAccent': isManualAccented,
                'sylNum': sylNum, 
                'accentSylNum': accentSylNum,	
                'assoc': assoc,	
                }			
            words[count] = wordInfo
            count = count + 1			
					
            empiricalValue1 = 35
            if i >= len(fileContent) - empiricalValue1: 
                break
										        
        WordBaseWork.__filterInexistingAssociation(words) # прореживаем - почему-то оригинальная программа может выдать базу с ассосиацией-ссылкой на несуществущее слово
		
        return words
				