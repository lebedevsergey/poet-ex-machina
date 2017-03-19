# Copyright 2016 Sergey Lebedev
# Licensed under the Apache License, Version 2.0

import click

class KeyboardWork:
    ENTER_KEY = b'\r'
    EXT_KEY_PREFIX = b'\xe0'
    ARROW_LEFT_KEY = b'K'    
    ARROW_RIGHT_KEY = b'M'    
    ESC_KEY = b'\x1b'
        
    ARROW_LEFT_KEY_UNICODE = '\u004B'
    ARROW_RIGHT_KEY_UNICODE = '\u004D'
    ENTER_KEY_UNICODE = '\u000B'
    ESC_KEY_UNICODE = '\u001B'
    
    CTRL_C = b'\x03'
    CTRL_D = b'\x04'
        
    # gets pressed key 
    @staticmethod
    def getch():
        mainKeyCode = click.getchar()
        if mainKeyCode == KeyboardWork.EXT_KEY_PREFIX:        
            extendedKeyCode = click.getchar()
            return mainKeyCode, extendedKeyCode
        extendedKeyCode = None        
        return (mainKeyCode, extendedKeyCode)
        
    @staticmethod
    def isBreakKeyPressed(keyInfo):
        if keyInfo[0] == KeyboardWork.ESC_KEY or keyInfo[0] == KeyboardWork.ESC_KEY_UNICODE or keyInfo[0] == KeyboardWork.CTRL_C or keyInfo[0] == KeyboardWork.CTRL_D:
            return True
        return False
    
    @staticmethod
    def isEnterPressed(keyInfo):
        if keyInfo[0] == KeyboardWork.ENTER_KEY or keyInfo[0] == KeyboardWork.ENTER_KEY_UNICODE:
            return True
        return False
        
    @staticmethod
    def isArrowRightPressed(keyInfo):        
        if (keyInfo[0] == KeyboardWork.EXT_KEY_PREFIX and keyInfo[1] == KeyboardWork.ARROW_RIGHT_KEY) or keyInfo[0] == KeyboardWork.ARROW_RIGHT_KEY_UNICODE:
            return True
        return False    
    
    @staticmethod
    def isArrowLeftPressed(keyInfo):
        if (keyInfo[0] == KeyboardWork.EXT_KEY_PREFIX and keyInfo[1] == KeyboardWork.ARROW_LEFT_KEY) or keyInfo[0] == KeyboardWork.ARROW_LEFT_KEY_UNICODE:
            return True
        return False    