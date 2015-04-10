# -*- coding: utf-8 -*-
import xml.etree.ElementTree as et
import re
import os
import enchant
from enchant.checker import SpellChecker
from datetime import datetime
datadir = "/Users/Simon/UNI_VII/bigdata/nzz/test/"
emptydir = "/Users/Simon/UNI_VII/bigdata/nzz/stringset/"
metadir = "/Users/Simon/UNI_VII/bigdata/nzz/metafiles/"

stringset = ['maschin', 'industri', 'automat', 'techni','mechani','motor']

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
import csv
t1 = datetime.now().strftime('%d-%m')
t2 = datetime.now().strftime('%H:%M')
metafilename = 'metafile_' + t1 + '_' + str(t2) + '.csv'
metapath = os.path.join(metadir, metafilename)       

for folder in folderlist:
    
    #create lists with relevant information for xml file
    clist = []
    ddis = []
    error_ratio = []
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
        
        Nmasch = 0
        tree = et.parse(filepath)
        root = tree.getroot()
        content = root.find('TX') 
        
        
        #loop through xml file's p tags
        for child in content.findall('P'): 
            ddid = child.get('ddis-id')
            text = unicode(child.text)
                
            if any(x in text.lower() for x in stringset):

                clist.append(text)
                cfile.append(file)
                cid.append(ddid)
        
        #auf file ebene
        tend = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
        
        #write file info for adjusting parameters
        Lfiles.append(file)
        Lfolder.append(folder)        
        
    #auf folder ebene
    #define new xml structure
    data = et.Element("data") 
    data.set('month',month) 
    for i in range(0,len(clist)):
        p = et.SubElement(data, "p")
        p.text = clist[i]
        p.attrib['file'] = cfile[i]
        #p.attrib['ddis-id'] = cid[i]
        
    
    #write new xml tree    
    tree = et.ElementTree(data)
    tree.write(newfilepath)
    
    print newfilename + ' ' + tend

print 'fertig'