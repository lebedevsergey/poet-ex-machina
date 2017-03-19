# -*- coding: utf-8 -*-

# Copyright 2016 Sergey Lebedev
# Licensed under the Apache License, Version 2.0

import includes.utils as utils

class RhymesAndRitms:

    # new algorithm that works with word syllables
    @staticmethod
    def getRhymedEnd(rhymedWord, rhymedWordAccentedSyllOffset):
        syllables = utils.Utils.getWordSyllables(rhymedWord)
        accentedSyllNum = len(syllables) - rhymedWordAccentedSyllOffset
        s = ''
        for i, syl in reversed(list(enumerate(syllables))):
            if i + 1 != accentedSyllNum:
                s = syl + s
            else:				
                j = len(syl) - 1
                for c in reversed(syl):
                    s = c + s
                    if utils.Utils.isVowel(c):
                        break
                    j = j - 1									
                if len(syllables) == accentedSyllNum and j > 0:
                    s = syl[j-1] + s
                break

        return s

    # old algorithm taken from the original ASm rpogram
    @staticmethod
    def getRhymedEnd_OldAlgorithm(rhymedWord, rhymedWordAccentedSyllOffset):		
        s = ''	
        j = len(rhymedWord) - 1	
        for i in range(0, rhymedWordAccentedSyllOffset + 1):
            while (not utils.Utils.isVowel(rhymedWord[j])) and j >= 0:
                s = rhymedWord[j] + s
                j = j - 1
            while (utils.Utils.isVowel(rhymedWord[j])) and j >= 0:
                s = rhymedWord[j] + s
                j = j - 1
            if rhymedWordAccentedSyllOffset > 0: 	# if not masculine rhyme then add syllable
                while (not utils.Utils.isVowel(rhymedWord[j])) and j >= 0:
                    s = rhymedWord[j] + s
                    j = j - 1
        return s        
        
    @staticmethod	
    def isRhyme(wordInfo, rhymedWordInfo):			
        rhymedWordAccentedSyllOffset = rhymedWordInfo['sylNum'] - rhymedWordInfo['accentSylNum']		
        rhymedEnd1 = RhymesAndRitms.getRhymedEnd(rhymedWordInfo['word'], rhymedWordAccentedSyllOffset)
        wordAccentedSyllOffset = wordInfo['sylNum'] - wordInfo['accentSylNum']
        rhymedEnd2 = RhymesAndRitms.getRhymedEnd(wordInfo['word'], wordAccentedSyllOffset)		
        if not rhymedEnd1 or not rhymedEnd2:
            return False
        # if len(rhymedEnd1) != len(rhymedEnd2) and not (rhymedWordAccentedSyllOffset == 0 and (len(rhymedEnd1) == 1 or len(rhymedEnd2) == 1)):
        if len(rhymedEnd1) != len(rhymedEnd2):
            return False	

        j = len(rhymedEnd2)-1
        for i in range(len(rhymedEnd1)-1, -1, -1):
            if j < 0:
                return False

            c1 = rhymedEnd1[i]		
            c2 = rhymedEnd2[j]
            consonant = utils.Utils.getConsonant(c2)		
            if c1 != c2 and c1 != consonant:			
                return False

            j = j - 1

        return True

    #checks if word meets verse line rhythm
    @staticmethod
    def RITM_li(wordInfo, prevWordInfo, verseLineTemplate, curTemplateSymlIndex):												#;6) Проверить совпадение ритма (такт и максимальное	#;  print db 13,10,'RITM:',0		 													
        sylNum = wordInfo['sylNum']
        if prevWordInfo:
            prevSylNum = prevWordInfo['sylNum']
        else:
            prevSylNum = 0

        if prevSylNum + sylNum <= 2 and prevSylNum > 0:
            return False
        if curTemplateSymlIndex + 1 - sylNum < 0:			#;А влезает ли в строку?
            return False		
        if sylNum == 1:	
            return True

        accentedSyllOffset = sylNum - wordInfo['accentSylNum']	
        if (curTemplateSymlIndex - accentedSyllOffset) < 0:
            return False		
        if verseLineTemplate[curTemplateSymlIndex - accentedSyllOffset] != '+':
            return False	
        return True