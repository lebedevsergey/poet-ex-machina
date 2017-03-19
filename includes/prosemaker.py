# -*- coding: utf-8 -*-

# Copyright 2016 Sergey Lebedev
# Licensed under the Apache License, Version 2.0

import random


import includes.wordbasework as wordbasework

class ProseMaker:	
    MAX_PROSE_WORDS_NUM = 30
	
    words = {}
	
    def __init__(self, words):
        self.words = words		
	
    def makeProse(self):		
        wordKeys = list(self.words.keys())
        curWordIndex = random.randint(0, len(wordKeys)-1)
        curWord = self.words[wordKeys[curWordIndex]]

        n = 0
        s = ''
        while n < self.MAX_PROSE_WORDS_NUM:
            s = curWord['word'] + ' ' + s
            assocWords = wordbasework.WordBaseWork.getAssoc(curWord, self.words)

            if len(assocWords) < 1:
                break
            if len(assocWords) == 1:
                curWord = assocWords[0]
            else:			
                curWord = assocWords[random.randint(0, len(assocWords)-1)]
            n = n + 1

        return s