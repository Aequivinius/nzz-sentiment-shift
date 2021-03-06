# -*- coding: utf-8 -*-
import xml.etree.ElementTree as et
import re
import os
import enchant
from enchant.checker import SpellChecker
from datetime import datetime
datadir = "/Users/Simon/UNI VII/bigdata/nzz/test/"
emptydir = "/Users/Simon/UNI VII/bigdata/nzz/preprocessed/"
metadir = "/Users/Simon/UNI VII/bigdata/nzz/metafiles/"

path =  datadir
folderlist=os.listdir(path)
folderlist.remove('.DS_Store')

#create lists with relevant information for meta file
Lfiles = []
Lfolder = []
Ler_fail = []
Lshit_encoding = []
Llength_error = []
Lletter_ratio = []
Lps = []
Lpsuccess = []
Ltstart = []
Ltend = []

for folder in folderlist:
    
    #create lists with relevant information for xml file
    clist = []
    ddis = []
    error_ratio = []
 
    month = str(folder)
    folderpath=os.path.join(path, folder)
    newfilename = month + '.xml'
    newfilepath=os.path.join(emptydir,newfilename)
    filelist=[]
    filelist = os.listdir(folderpath)
    filelist.remove('.DS_Store')
    
    for file in filelist:
        tstart = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
        print file + tstart
        shit_encoding = 0
        length_error = 0
        letter_ratio = 0
        er_fail = 0
        ps = 0
        psuccess = 0
        
        filepath=os.path.join(folderpath, file)
        tree = et.parse(filepath)
        root = tree.getroot()
        content = root.find('TX') 
        
        #loop through xml file's p tags
        for child in content.findall('P'):      
            ps += 1
            try: 
                text = unicode(child.text)
            except:
                shit_encoding += 1
                continue
                
            #check string length
            txlen = len(text)
            if txlen < 500:
                length_error += 1
                continue
               
            #check for string size to amount of letters ratio  
            Nchar = 0
            for char in text:
                if char.isalpha() == True or char == u" ":
                    Nchar += 1
            lr = Nchar/ float(txlen)   
            if lr < 0.7:
                letter_ratio += 1
                continue
            
            #remove all special characters apart from characterset below    
            text = re.sub('[^A-Za-z0-9.,!?\s\\xf6\\xfc\\xe4\\xdf\\u00DF]', '', text)
           
            #spell checking
            chkr = SpellChecker("de_CH",text)
            lasterror = ''
            lasterror2 = ''
            lasterror3 = ''
            Nerr = 0
            for err in chkr:
                repl = ''
                print err.word
                if lasterror == err.word or lasterror2 == err.word or lasterror3 == err.word:
                    continue
                lasterror3 = lasterror2
                lasterror2 = lasterror
                lasterror = err.word
                Nerr += 1
                repl = err.suggest()
                try:
                    if repl[0] == err.word:
                        continue
                    err.replace(repl[0])
                except:
                    continue
                    err.replace(u"spellchecker_fail")
                    
                if len(err.word) > len(repl[0]):
                    l = err.word[len(repl[0]):].lower()
                    r = chkr.suggest(err.word[len(repl[0]):])
                            
                    if (len(r) > 0) and (l == r[0].lower()):
                        err.replace(u"wort_das_dem_spellchecker_aerger_macht")
                                
                    if len(err.word) == 2 and len(repl[0]) == 2:
                        err.replace(u"wort_das_dem_spellchecker_aerger_macht")                    
                
            text = err.get_text()   
            
            #check error ratio
            Nwords = text.count(' ')
            try:
                er = Nerr/float(Nwords)  
            except:
                er = 0 
            if er > 0.7:
                er_fail += 1
                continue
            psuccess += 1

            #write necessary info into lists
            error_ratio.append(er)
            ddis.append(child.get('ddis-id'))
            clist.append(text)
            
        #auf file ebene
        tend = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
        
        
        #write file info for adjusting parameters
        Lfiles.append(file)
        Lfolder.append(folder)
        Ler_fail.append(er_fail)
        Lshit_encoding.append(shit_encoding)
        Llength_error.append(length_error)
        Lletter_ratio.append(letter_ratio)
        Lps.append(ps)
        Lpsuccess.append(psuccess)
        Ltstart.append(tstart)
        Ltend.append(tend)
        
    #auf folder ebene
    #define new xml structure
    data = et.Element("data") 
    month = et.SubElement(data, month) 
    for i in range(0,len(clist)):
        p = et.SubElement(month, "p")
        p.text = clist[i]
        p.attrib['ddis-id'] = ddis[i]
        p.attrib['error_ratio'] = error_ratio[i]
    
    #write new xml tree    
    tree = et.ElementTree(data)
    tree.write(newfilepath)
    
#write metafile
import csv
t1 = datetime.now().strftime('%d-%m')
t2 = datetime.now().strftime('%H:%M')
metafilename = 'metafile_' + t1 + '_' + str(t2) + '.csv'
metapath = os.path.join(metadir, metafilename)
with open(metapath, 'wb') as a:
    a = csv.writer(a, delimiter=";")
    a.writerow(['Lfiles', 'Lfolder', 'Ler_fail', 'Lshit_encoding', 'Llength_error', 'Lletter_ratio','Lpsuccess','Lps','Ltstart','Ltend'])
    for i in range(0,len(Lfiles)): 
        a.writerow([Lfiles[i], Lfolder[i], Ler_fail[i], Lshit_encoding[i], Llength_error[i], Lletter_ratio[i], Lpsuccess[i], Lps[i], Ltstart[i], Ltend[i]])
    