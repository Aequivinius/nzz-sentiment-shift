# -*- coding: utf-8 -*-
filename = "/Users/Simon/UNI VII/bigdata/nzz/NZZ_1910_1920-with-uuid/1910-01/JM20121222000301997.xml"
import xml.etree.ElementTree as et
import re
tree = et.parse(filename)
root = tree.getroot()
content = root.find('TX')
clist = []
craw = []
letter_ratio = []

#loop through xml file's p tags
for child in content.findall('P'): 

    #creat list with raw data for comparison (only during development)
    craw.append(child.text)
    
    #try to put content int string
    try:
        text = str(child.text)
    except:
        clist.append('shit_encoding')
        continue
        
    #check string length
    txlen = len(text)
    if txlen < 40:
        clist.append('low_txlen')
        continue
        
    #check string size to the amount of letters ratio   
    Nchar = 0
    for char in text:
        if char.isalpha() == True or char == " ":
            Nchar += 1
    lr = Nchar/ float(txlen)
    letter_ratio.append(lr)     
    if lr > 0.5:
        clist.append(text)
    else:
        clist.append('letter_ratio')