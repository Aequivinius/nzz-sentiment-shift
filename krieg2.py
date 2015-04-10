# -*- coding: utf-8 -*-
import xml.etree.ElementTree as et
import re
import os
import enchant

# reading sentiWS
senti_WS_negative = "/Users/Simon/UNI_VII/bigdata/nzz/SentiWS_v1.8c/SentiWS_v1.8c_Negative.txt"
senti_WS_positive = "/Users/Simon/UNI_VII/bigdata/nzz/SentiWS_v1.8c/SentiWS_v1.8c_Positive.txt"
senti_WS_write = "/Users/Simon/UNI_VII/bigdata/nzz/SentiWS_v1.8c/Senti_WS_written"

senti_WS = {}
with open(senti_WS_negative,'r') as f:
    for line in f:
        entries = line.split("\t")
        entry = entries[0].split("|")[0]
        senti_WS[entry.strip()] = entries[1]
        if len(entries) > 2:
            for word in entries[2].split(","):
                senti_WS[word.strip()] = entries[1]
    
with open(senti_WS_positive,'r') as f:
    for line in f:
        entries = line.split("\t")
        entry = entries[0].split("|")[0]
        senti_WS[entry.strip()] = entries[1]
        if len(entries) > 2:
            for word in entries[2].split(","):
                senti_WS[word.strip()] = entries[1]

# writing to file, but that's not really needed
#with open(senti_WS_write,'w') as w:
    #for key,value in senti_WS.iteritems():
        #w.write(key + "," + value + "\n")

def sentiment(text):
 
    counter = 0
    value = 0 
    for item in text:
        counter += 1
        if item in senti_WS:
            value += float(senti_WS[item])
    if counter == 0:
        return 0
    return value / counter

from enchant.checker import SpellChecker
from datetime import datetime
datadir = "/Users/Simon/UNI_VII/bigdata/nzz/test2/"
emptydir = "/Users/Simon/UNI_VII/bigdata/nzz/krieg2/"

stringset = ['waffe','krieg','panzer','angriff','armee',u'militär','bombe','heer','kampf','schlacht','luftwaffe','streitkr','wehr']
path =  datadir
folderlist=os.listdir(path)
try:
    folderlist.remove('.DS_Store')
except:
    bla = 1

#create lists with relevant information for meta file
Lfiles = []
Lfolder = []


#write metafile
#import csv
#t1 = datetime.now().strftime('%d-%m')
#t2 = datetime.now().strftime('%H:%M')
#metafilename = 'metafile_' + t1 + '_' + str(t2) + '.csv'
#metapath = os.path.join(metadir, metafilename)       

for folder in folderlist:
    
    #create lists with relevant information for xml file
    clist = []
    ddis = []
    cfile = []
    cid = []
 
    month = str(folder)
    folderpath=os.path.join(path, folder)
    newfilename = month + '.xml'
    newfilepath=os.path.join(emptydir,newfilename)
    if os.path.isfile(newfilepath)== True:
        continue
    filelist=[]
    filelist = os.listdir(folderpath)
    try:
        filelist.remove('.DS_Store')
    except:
        bah = 1
    
    for file in filelist:
        tstart = datetime.now().strftime('%d-%m-%Y %H:%M:%S')

        filepath=os.path.join(folderpath, file)
        
        tree = et.parse(filepath)
        root = tree.getroot()
        content = root.find('TX') 
        
        
        #loop through xml file's p tags
        for child in content.findall('P'): 
            wordlist = []
            ddid = child.get('ddis-id')
            text = unicode(child.text).lower()
            wordlist = text.split(' ')
            try:
                wordlist.remove('')
            except:
                bla = 1
            Nwords = len(wordlist)
            crange = 20
            
            for i in range(0,Nwords):
                found = False
                for z in stringset:
                    if z in wordlist[i]:
                        found = True
                        break
                
                if found:        
                    if i < crange and i-Nwords < crange:
                        start = 0
                        end = Nwords
                        for y in range(start,end):
                            clist.append(wordlist[y])
                    elif i > crange and i-Nwords > crange:
                        start = i-crange
                        end = i+crange
                        for y in range(start,end):
                            clist.append(wordlist[y])
                    elif i > crange and i-Nwords < crange:
                        start = i-crange
                        end = Nwords
                        for y in range(start,end):
                            clist.append(wordlist[y])
          
        #auf file ebene
        
        #write file info
        #Lfiles.append(file)
        #Lfolder.append(folder)  
    counterdict = {}  
    senti = sentiment(clist)
    print senti
    
    for i in range(0,len(clist)):
        if clist[i] in counterdict:
            counterdict[clist[i]] += 1 
        else:
            counterdict[clist[i]] = 1     
            
        
    data = et.Element("data") 
    data.set('senti',str(senti))
    for key, value in counterdict.iteritems():
        p = et.SubElement(data, "p")
        p.text = unicode(value)
        p.attrib['word'] = unicode(key)
    
    #write new xml tree    
    tree = et.ElementTree(data)
    tree.write(newfilepath)
    
    tend = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
    print newfilename + ' ' + tend

print 'fertig'