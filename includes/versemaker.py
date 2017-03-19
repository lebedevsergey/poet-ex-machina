# -*- coding: utf-8 -*-

# Copyright 2016 Sergey Lebedev
# Licensed under the Apache License, Version 2.0

import locale, random, re, sys
import includes.rhymesandritms as rhymes
import includes.utils as utils
import includes.wordbasework as wordbasework

#locale.setlocale(locale.LC_ALL, '')
#code = locale.getpreferredencoding()

class VerseMaker:	
    noOneSyllableEnds = False               # ensures that verse will not end with one-syllable words
	
    debugMode = False
    debugWordFoundBaseCount = 0 
    debugWordFoundAssocCount = 0
	
    SEARCH_BASE = 0	
    SEARCH_ASSOC = 2
		
    words = {}
    verseTemplate = {}	

    def __init__(self, words, verseTemplate):
        self.words = words
        self.verseTemplate = verseTemplate

    # make versesNum verses 
    def makeVerse_N(self, versesNum):
						
        self.__clearUsedAsRhymeFlags()
        self.__clearUsedInLineFlags()
			
        verseN = ''		
        for i in range(1, versesNum + 1):			
            verseN = verseN + self.makeVerse() + "\n"			

        if self.debugMode:
            print('debugWordFoundBaseCount: ', self.debugWordFoundBaseCount) 
            print('debugWordFoundAssocCount: ', self.debugWordFoundAssocCount)
            print()
		
        return verseN

    # make one verse
    def makeVerse(self):
        rhymesBase = {}
        verseLines = [None] * len(self.verseTemplate)
		
        self.debugWordFoundBaseCount = 0 
        self.debugWordFoundAssocCount = 0	
			
        curLineIndex = len(self.verseTemplate)-1					
        while curLineIndex >= 0:		
            if verseLines[curLineIndex]:                                                #; строка уже написана?
                curLineIndex = curLineIndex - 1
                continue
			
            verseLine = self.__create_STRING(self.verseTemplate[curLineIndex], rhymesBase)			
            if (verseLine == None):						
                rhymeType = self.verseTemplate[curLineIndex]['rhymeType']
                rhymesBase.pop(rhymeType, None)                                         #;стереть такую рифму							
                self.__erase_STRING_with_RHYME(rhymeType, curLineIndex, verseLines) 	#;стереть все строки с этой рифмой															
				
                curLineIndex = len(self.verseTemplate)-1
                continue
	
            verseLines[curLineIndex] = verseLine
            curLineIndex = curLineIndex - 1
			
        verse = ''
        for s in verseLines:
            verse = verse + s + "\n"		
			
        return verse

    @staticmethod
    def loadVerseTemplate(fileName):
        f = open(fileName, 'r')
        text = f.read()
        f.close()
		
        s = re.split("\n", text)				
		
        verseTemplate = []	
        for i, s1 in enumerate(s):
            s2 = s1.replace('\t', ' ')
            s2 = s2.replace('\n', ' ')
            s2 = s2.replace(chr(0x9), ' ')
            s2 = s2.strip()			
            if not s2:
                continue			
			
            rhymeParams = re.split(' ', s2)			
			
            rhymeParams = list(filter(None, rhymeParams))		
            verseTemplate.append({'rhymeType': rhymeParams[1], 'pattern': rhymeParams[0]})	
        return verseTemplate
    
    def setNoOneSyllableEndsMode(self, mode):
        self.noOneSyllableEnds = mode

    def __create_STRING(self, lineTemplate, rhymesBase):
		
        self.__clearUsedInLineFlags()
        E_stack = []		
        searchWordsMode = self.SEARCH_ASSOC		
		
        for i, word in self.words.items():		
            word['usedInLine'] = False		
		
        state = {'curWord': None,
            'prevWord': None, 
            'FIELD': [],
            'searchWordsMode': searchWordsMode, 
            'curTemplateSymlIndex': len(lineTemplate['pattern']) - 1
            }
		
        curRhymeType = lineTemplate['rhymeType']
        if curRhymeType in rhymesBase:
            rhymedWord = rhymesBase[curRhymeType]
            useFreeRhyme = False
        else:
            rhymedWord = None
            useFreeRhyme = True
		
        while True:
            if len(E_stack) == 0:
                isEndWord = True
            else: 
                isEndWord = False
			
            if state['searchWordsMode'] == self.SEARCH_BASE or isEndWord:
                checkedWord = self.__searchAllBase(isEndWord)
                wordFoundMode = 'SEARCH_BASE'
                self.debugWordFoundBaseCount = self.debugWordFoundBaseCount + 1 
            else:
                checkedWord = self.__GET_RND_FIELD_WORD(state['FIELD'], isEndWord)
                wordFoundMode = 'SEARCH_ASSOC'
                self.debugWordFoundAssocCount = self.debugWordFoundAssocCount + 1
									
            if checkedWord == None:						
                if not isEndWord: 								#;13) Если слово не оконечное ■ к 16 db 13,10,'ОШИБКА ПОИСКА  С Л О В А - после /',0
                    state = E_stack.pop()							#; Извлечь из стека Е предыдущий шаг, слово отбросить, а все остальное установить как было, в т.ч. прежнюю группу поиска
                    continue
                else:
                    if state['searchWordsMode'] == self.SEARCH_ASSOC:						
                        self.__clearUsedInLineFlags()
                        state['searchWordsMode'] = self.SEARCH_BASE 					
                        continue
                    if state['searchWordsMode'] == self.SEARCH_BASE:                            # если ■сфера поиска■ = вся база
                        if not useFreeRhyme:
                            return None
                        else:									# Если и рифма была свободная, то						
                            sys.exit('■ТВОРЧЕСКИЙ КРИЗИС■, конец')
	
            if state['prevWord'] and checkedWord['word'] == state['prevWord']['word']:
                continue
                                                                                                #;*6) Проверить совпадение ритма (такт и максимальное количество слогов		
            if not rhymes.RhymesAndRitms.RITM_li(checkedWord, state['prevWord'], lineTemplate['pattern'], state['curTemplateSymlIndex']):
                continue			
            if self.noOneSyllableEnds and checkedWord['sylNum'] < 2:
                continue
            if isEndWord and (not useFreeRhyme) and rhymedWord and (not rhymes.RhymesAndRitms.isRhyme(checkedWord, rhymedWord)):	#не рифмуется
                continue			

            if checkedWord and self.debugMode: 
                print (wordFoundMode + ' ', checkedWord)				                    
            state['curWord'] = checkedWord
            E_stack.append(state.copy())                                                        #;*7) Погрузить в стек Е найденное слово,
					                
            state['FIELD'] = wordbasework.WordBaseWork.getAssoc(checkedWord, self.words)        #;*8) Ассоциации найденного слова ;занести в сферу поиска		
            if state['FIELD']:
                state['searchWordsMode'] = self.SEARCH_ASSOC
            else:
                searchWordsMode = self.SEARCH_BASE
						
            if searchWordsMode == self.SEARCH_BASE:
                state['FIELD'] = []
				
            state['prevWord'] = checkedWord		
                #;9)  Если строка не заполнена полностью - продолжаем		
            state['curTemplateSymlIndex'] = state['curTemplateSymlIndex'] - checkedWord['sylNum']					
            if state['curTemplateSymlIndex'] < 0:
                break
            state['curWord'] = None
		
        s = ''		
        while True:                                                                             #;*9) Вынуть из стека Е все этапы, запоминая ; слова в буфере готовых строк	
            if not E_stack:
                break
            state = E_stack.pop()		
            s = s + ' ' + utils.Utils.highlightAccentedVowel(state['curWord'])
		
        rhymesBase[curRhymeType] = state['curWord']                                             #;*11) Записать оконечное слово в базу рифм, ;заместо предыдущего (если оно было)
            #поставить флаг что слово использовано		
        state['curWord']['usedAsRhyme'] = True                                                  # в след строке это же слово можно использовать		
		
        return s
		
    def __searchAllBase(self, isEndWord):	
        wordKeys = list(self.words.keys())
        startWordIndex = random.randint(0, len(wordKeys)-1)		
        i = startWordIndex	
        while True:     
            word = self.words[wordKeys[i]]
					
            if not word['usedInLine']:
                if not isEndWord:
                    word['usedInLine'] = True                                                   #; помечаем как использованный
                    return word
                elif not word['usedAsRhyme']:
                    word['usedInLine'] = True                                                   #  ; помечаем как использованный
                    return word
				
            i = i + 1					
            if i > len(wordKeys)-1: 					# не вышли за границы базы?
                i = 0 
            if i == startWordIndex: 					#уже по второму кругу пошли? #print ПЕРЕВАЛ			
                return None
			
    def __GET_RND_FIELD_WORD(self, FIELD, isEndWord):
        while True:	
            if len(FIELD) == 0:
                return None
            curWordIndex = random.randint(0, len(FIELD)-1)
            word = FIELD[curWordIndex]
            FIELD.remove(word)	 
            if not isEndWord:                                   # если не оконечное слово, то можно повторяться
                return word
            if not word['word']['usedAsRhyme']:			# ;использован ли уже как рифма?
                return word

    def __erase_STRING_with_RHYME(self, RhymeType, curLineIndex, STROKI):
        verseTemplateLen = len(self.verseTemplate)		
        for i in range(curLineIndex, verseTemplateLen):			
            if self.verseTemplate[i]['rhymeType'] == RhymeType:			
                STROKI[i] = None
				
    def __clearUsedAsRhymeFlags(self):
        for i, word in self.words.items():			
            word['usedAsRhyme'] = False
				
    def __clearUsedInLineFlags(self):
        for i, word in self.words.items():			
            word['usedInLine'] = False
	