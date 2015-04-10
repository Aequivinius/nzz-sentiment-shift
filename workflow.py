# -*- coding: utf-8 -*-
import xml.etree.ElementTree as et
import re
import os
import enchant
from enchant.checker import SpellChecker
datadir = "/Users/Simon/UNI VII/bigdata/nzz/test/"
emptydir = "/Users/Simon/UNI VII/bigdata/nzz/preprocessed/"

path =  datadir
folderlist=os.listdir(path)
folderlist.remove('.DS_Store')

for folder in folderlist:
    clist = []
    cid = []
    month = str(folder)
    folderpath=os.path.join(path, folder)
    newfilename = month + '.xml'
    newfilepath=os.path.join(emptydir,newfilename)
    filelist=[]
    filelist = os.listdir(folderpath)
    
    for file in filelist:
        filepath=os.path.join(folderpath, file)
        tree = et.parse(filepath)
        root = tree.getroot()
        content = root.find('TX') 
        
        #loop through xml file's p tags
        for child in content.findall('P'): 
            #try to put content int0 string
            # NICO: use the unicode class, which offers pretty much all the functions of the 
            # string class, but does not save them as 8-bit strings
            try: 
                text = unicode(child.text)
            except:
                continue
                
            #check string length
            txlen = len(text)
            if txlen < 200:
                continue

            #write processed p's to list
            clist.append(text)
        #auf file ebene
    #auf folder ebene
    data = et.Element("data") 
    month = et.SubElement(data, month) 
    for i in range(0,len(clist)):
        p = et.SubElement(month, "p")
        p.text = clist[i]   
        
    tree = et.ElementTree(data)
    tree.write(newfilepath)