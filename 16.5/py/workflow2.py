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

#create lists with relevant information for meta file
Lfiles = []
Lfolder = []
Ler_fail = []
Lshit_encoding = []
Llength_error = []
Lletter_ratio = []
Lps = []
Lpsuccess = []

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
    
    for file in filelist:
        print file
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
            if txlen < 1000:
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
            text = re.sub('[^A-Za-z0-9.,!?\s\\xf6\\xfc\\xe4\\xdf]', '', text)
           
            ##spell checking
            #chkr = SpellChecker("de_CH",text)
            #Nerr = 0
            #lasterror = ''
            #for err in chkr:
                #if lasterror == err.word:
                    #continue
                #lasterror = err.word
                #Nerr += 1
                #repl = err.suggest()
                #try:
                    #err.replace(repl[0])
                #except:
                    #repl = [u""]
                    #err.replace(u"spellchecker_fail")
                
            #text = err.get_text() 
            
            #check error ratio
            Nwords = text.count(' ')
            try:
                er = Nerr/float(Nwords)  
            except:
                er = 0 
            if er > 0.7:
                er_fail += 1
                continue

            #write necessary info into lists
            error_ratio.append(er)
            ddis.append(child.get('ddis-id'))
            psuccess += 1
            clist.append(text)
            
        #auf file ebene
        #write file info for adjusting parameters
        Lfiles.append(file)
        Lfolder.append(folder)
        Ler_fail.append(er_fail)
        Lshit_encoding.append(shit_encoding)
        Llength_error.append(length_error)
        Lletter_ratio.append(letter_ratio)
        Lps.append(ps)
        Lpsuccess.append(psuccess)
        
    ##auf folder ebene
    ##define new xml structure
    #data = et.Element("data") 
    #month = et.SubElement(data, month) 
    #for i in range(0,len(clist)):
        #p = et.SubElement(month, "p")
        #p.text = clist[i]
        #p.attrib['ddis-id'] = ddis[i]
        ##p.attrib['error_ratio'] = error_ratio[i]
    
    ##write new xml tree    
    #tree = et.ElementTree(data)
    #tree.write(newfilepath)
    
#write metafile
import csv
from datetime import datetime
t1 = datetime.now().strftime('%d-%m')
t2 = datetime.now().strftime('%H:%M')
metafilename = 'metafile_' + t1 + '_' + str(t2) + '.csv'
metadir = "/Users/Simon/UNI VII/bigdata/nzz/metafiles/"
metapath = os.path.join(metadir, metafilename)
with open(metapath, 'wb') as a:
    a = csv.writer(a, delimiter=";")
    a.writerow(['Lfiles', 'Lfolder', 'Ler_fail', 'Lshit_encoding', 'Llength_error', 'Lletter_ratio','Lpsuccess','Lps'])
    for i in range(0,len(Lfiles)): 
        a.writerow([Lfiles[i], Lfolder[i], Ler_fail[i], Lshit_encoding[i], Llength_error[i], Lletter_ratio[i], Lpsuccess[i], Lps[i]])
    