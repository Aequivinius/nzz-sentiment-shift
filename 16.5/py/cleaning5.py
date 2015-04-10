# -*- coding: utf-8 -*-
import xml.etree.ElementTree as et
import re
import enchant
from enchant.checker import SpellChecker

filename = "/Users/Simon/UNI VII/bigdata/nzz/NZZ_1910_1920-with-uuid/1910-01/JM20121222000301997.xml"
# filename = "/Users/tabris/Downloads/NZZ_1910_1920-with-uuid/1910-08/JM20121222000281742.xml"

tree = et.parse(filename)
root = tree.getroot()
content = root.find('TX')
clist = []
craw = []
letter_ratio = []
error_ratio = []
lengths = []

#loop through xml file's p tags
for child in content.findall('P'): 

    craw.append(unicode(child.text))
    
    #try to put content int0 string
    # NICO: use the unicode class, which offers pretty much all the functions of the 
    # string class, but does not save them as 8-bit strings
    try: 
        text = unicode(child.text)
    except:
        clist.append('shit_encoding')
        continue
        
    #check string length
    txlen = len(text)
    lengths.append(txlen)
    if txlen < 1000:
        clist.append('length')
        continue
        
    #check for string size to amount of letters ratio  
    Nchar = 0
    for char in text:
        # NICO: if you prefix a string with u, it will turn it into a unicode string
        if char.isalpha() == True or char == u" ":
            Nchar += 1
    lr = Nchar/ float(txlen)
    letter_ratio.append(lr)     
    if lr < 0.7:
        clist.append('letter_ratio')
        continue
    
    #remove all special characters
    text = re.sub('[^A-Za-z0-9.,!?\s\\xf6\\xfc\\xe4\\xdf]', '', text)

    
    #spell checking
    chkr = SpellChecker("de_CH",text)
    Nerr = 0
    for err in chkr:
        Nerr += 1
        repl = ''
        repl = err.suggest()
        try:
            err.replace(repl[0])
        except:
            err.replace('Error')

        text = err.get_text()
    
    #check error ratio
    Nwords = text.count(' ')
    er = Nerr/float(Nwords)
    error_ratio.append(er)
    if er > 0.7:
        clist.append('error_ratio')
        continue
    
    #finally write processed p's to list
    clist.append(text)

#compare processing        
for i in range(1,len(clist)):
    print "before", craw[i]
    print "after  ", clist[i]
    print ""