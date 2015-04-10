# -*- coding: utf-8 -*-
import enchant
import re
from enchant.checker import SpellChecker

def spellcheck(text):
    #remove all special characters apart from characterset below    
    text = re.sub('[^A-Za-z0-9.,!?\s\\xf6\\xfc\\xe4\\xdf]', '', text)
    
    #spell checking
    chkr = SpellChecker("de_CH",text)
    lasterror = ''
    lastlasterror = ''
    Nerr = 0
    for err in chkr:
        repl = ''
        if lastlasterror == err.word:
            continue
        if lasterror == err.word:
            continue
        lastlasterror = lasterror
        lasterror = err.word
        Nerr += 1
        repl = err.suggest()
        try:
            err.replace(repl[0])
        except:
            err.replace(u"spellchecker_fail")
        
    text = chkr.get_text()
    return text