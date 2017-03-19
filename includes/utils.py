# -*- coding: utf-8 -*-

# Copyright 2016 Sergey Lebedev
# Licensed under the Apache License, Version 2.0

class Utils:
    ASSOC_STOP_SYMS = frozenset(u'.?!()')
    CYRILLIC_LETTERS = frozenset(u'абвгдеёжзйиклмнопртсуфхчцшщыьъэюя')
    VOWELS = frozenset(u'аеёиыоуяэю')
    CONS = frozenset(u'бвгджзйклмнпрстфхцчшщ')
    DEAF = frozenset(u'кпстф')	
    VOICED = frozenset(u'бвгджзлмнрхцчшщ')
    SIGN = frozenset(u'ъь')
    OTHER = frozenset(u'ъь')

    CONSONANT_PAIRS = {'б': 'п', 'в': 'ф', 'г': 'к', 'д': 'т', 'ж': 'ш', 'щ': 'ш', 'з': 'с', 'м': 'н', 'ц': 'ч', 'ы': 'и', 'ю': 'у', 'я': 'а', 'э': 'е', 'ё': 'о'}	
    ONE_LETTER_WORDS = frozenset(u'оауияксвж')
		
    @staticmethod
    def highlightAccentedVowel(wordInfo):	
        s = ""
        curSylNum = 0	
        i = 0
        for c in wordInfo['word']:
            if not Utils.isVowel(c):
                s = s + c
                continue
            curSylNum = curSylNum + 1
            if curSylNum == wordInfo['accentSylNum']:
                s = s + c.upper()
            else:
                s = s + c
            i = i + 1
        return s

    @staticmethod	
    def getConsonant(letter):
        if letter in Utils.CONSONANT_PAIRS:
            return Utils.CONSONANT_PAIRS[letter]  
        else: 
            return letter
	
    @staticmethod
    def getConsonantWord(word):	
        consonantWord = ''
        for c in word:
            consonantWord = consonantWord + Utils.getConsonant(c)
        return consonantWord

    @staticmethod
    def isCyrillicLetter(sym):
        if sym.lower() in Utils.CYRILLIC_LETTERS:
            return True
        return False

    @staticmethod
    def isVowel(c):
        if (c.lower() in Utils.VOWELS):
            return True
        return False

    @staticmethod
    def isOther(c):
        if (c.lower() in Utils.OTHER):
            return True
        return False

    @staticmethod
    def isCons(c):
        if (c.lower() in Utils.CONS):
            return True
        return False

    @staticmethod
    def isDeaf(c):
        if (c.lower() in Utils.DEAF):
            return True
        return False

    @staticmethod
    def isVoiced(c):
        if (c.lower() in Utils.VOICED):
            return True
        return False	

    @staticmethod
    def isAssocStopSym(sym):
        if sym in Utils.ASSOC_STOP_SYMS:
            return True
        return False

    @staticmethod
    def isOneLetterWord(sym):
        if sym in Utils.ONE_LETTER_WORDS:
            return True
        return False

    @staticmethod
    def getWordSyllables(word):
        def isNotLastSyllable(wordEnd):
            for sym in wordEnd:
                if Utils.isVowel(sym):
                    return True
            return False 

        syllables = []		
        curSyll = ''
        for i, curSym in enumerate(word):
            curSyll = curSyll + curSym            
            # 	          // Проверки на признаки конца слогов            
            if curSym == 'й' and i > 0 and i < len(word)-1 and isNotLastSyllable(word[i:]):
                isSyllReady = True      # буква равна 'й' и она не первая и не последняя и это не последний слог
            elif i < len(word)-1 and Utils.isVowel(curSym) and Utils.isVowel(word[i + 1]):
                isSyllReady = True      # текущая гласная и следующая тоже гласная
            elif i < len(word) - 2 and Utils.isVowel(curSym) and Utils.isCons(word[i + 1]) and Utils.isVowel(word[i + 2]):
                isSyllReady = True      # текущая гласная, следующая согласная, а после неё гласная
            elif i < len(word) - 2 and Utils.isVowel(curSym) and Utils.isDeaf(word[i + 1]) and Utils.isCons(word[i + 2]) and isNotLastSyllable(word[(i + 1):]):
                isSyllReady = True      #  текущая гласная, следующая глухая согласная, а после согласная и это не последний слог                            
            elif i < len(word) - 2 and Utils.isVowel(curSym) and Utils.isVoiced(word[i + 1]) and Utils.isCons(word[i + 2]) and isNotLastSyllable(word[(i + 1):]):                
                isSyllReady = True      # текущая гласная, следующая глухая согласная, а после согласна� и это не последний слог (новые правила)
            elif i < len(word) - 1 and Utils.isOther(curSym) and not Utils.isVowel(word[i + 1]) and isNotLastSyllable(word[0:i]):
                isSyllReady = True       # текущая другая, а следующая не гласная если это первый слог 
            # текущая звонкая или шипящая согласная, перед ней гласная, следующая не гласная и не другая, и это не последний слог
            # 			if i > 0 and i < len(word) - 1 and Utils.isVoiced(curSym) and Utils.isVowel(word[i - 1]) and not (Utils.isVowel(word[i + 1]) or Utils.isOther(word[i + 1])) and isNotLastSyllable(word[(i+1):]):    
            # 				syllables.append(curSlog)
            # 				curSlog = '' 
            # 				continue            
            else:
                isSyllReady = False
            
            if isSyllReady:
                syllables.append(curSyll)
                curSyll = ''                 

        syllables.append(curSyll)
        return syllables			