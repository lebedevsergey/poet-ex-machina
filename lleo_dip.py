# -*- coding: utf-8 -*-

# Python version of Leonid Kaganov's composing verses program
# Original program written in Assembly in 1996
# 
# Copyright 2016 Sergey Lebedev
# Licensed under the Apache License, Version 2.0

import sys, os, argparse
if sys.version_info[0] < 3:
    exec('print "! Please run me with Python version 3 !"')
    exit()

import includes.versemaker as versemaker
import includes.prosemaker as prosemaker
import includes.accentsandsyllables as accentsandsyllables
import includes.wordbasework as wordbasework
import includes.keyboard_work as keyboard_work
import includes.cmdlinestuff as cmdlinestuff


if len(sys.argv) > 1 and '--oldschool' in sys.argv:    
    cmdlinestuff.usageOldMsg()

parser = argparse.ArgumentParser()
parser.add_argument("mode", help="режим запуска программы")
parser.add_argument("basename", help="имя базы слов")
parser.add_argument("thirdArg", nargs='?', help="")

try:
    args = parser.parse_args()
except SystemExit:
    cmdlinestuff.usage()	

if args.mode == 'c':
    if not args.thirdArg:
        cmdlinestuff.usage()
    words = wordbasework.WordBaseWork.loadWordBase(args.basename)        
    template = versemaker.VerseMaker.loadVerseTemplate(args.thirdArg)
    v = versemaker.VerseMaker(words, template)    
#     v.setNoOneSyllableEndsMode(True)
#     v.debugMode = True

    f = open('result.txt', 'w')    
    while True:        
        s = '***' + "\n" + v.makeVerse_N(2) + "\n"
        print(s)
        f.write(s)        
        if keyboard_work.KeyboardWork.isBreakKeyPressed(keyboard_work.KeyboardWork.getch()):
            break
    f.close()
                        
elif args.mode == 'p':
    words = wordbasework.WordBaseWork.loadWordBase(args.basename)
    p = prosemaker.ProseMaker(words)
    f = open('result.txt', 'w')
    while True:        
        s = p.makeProse() + "\n"
        print(s)
        f.write(s)             
        if keyboard_work.KeyboardWork.isBreakKeyPressed(keyboard_work.KeyboardWork.getch()):
            break
    f.close()
                
elif args.mode == 'b':
    print('Загружаем текст в базу...')
    with open(args.thirdArg, mode='r', encoding='utf-8') as f:
        text = f.read()    
            
    b = wordbasework.WordBaseWork()        
    if os.path.exists(args.basename):
        oldWords = wordbasework.WordBaseWork.loadWordBase(args.basename)
        if oldWords:        
            b.words = oldWords
    words = b.refillBase(text)
    print('Расстановка ударений...')    
    words = (accentsandsyllables.AccentsAndSyllables()).setAccentsAndSyllablesDict_N(words)    
    
    wordbasework.WordBaseWork.saveWordBase(args.basename, words)
        
elif args.mode == 'u':
    print('Расстановка ударений...')
    if not args.thirdArg:
        cmdlinestuff.usage()
    words = wordbasework.WordBaseWork.loadWordBase(args.basename)
    accents = accentsandsyllables.AccentsAndSyllables()
    if os.path.exists(args.thirdArg):
        accents.loadSyllablesBase(args.thirdArg)        
    c = accents.setAccentsAndSyllablesManual_N(words)
    wordbasework.WordBaseWork.saveWordBase(args.basename, words) 
    accents.saveSyllablesBase(args.thirdArg)
