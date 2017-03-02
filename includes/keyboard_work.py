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
    
    CTRL_C_KEY = b'\x03'
        
    # gets pressed key 
    @staticmethod
    def getch():
        mainKeyCode = click.getchar()
        if mainKeyCode == KeyboardWork.EXT_KEY_PREFIX:        
            extendedKeyCode = click.getchar()
            return mainKeyCode, extendedKeyCode
        extendedKeyCode = None
        return mainKeyCode, extendedKeyCode
    
    # gets pressed key 
    @staticmethod
    def isBreakKeyPressed(key, extKey):
        if key == KeyboardWork.ESC_KEY or key == KeyboardWork.CTRL_C_KEY or key == KeyboardWork.ESC_KEY_UNICODE:
            return True
        return False
