# -*- coding: utf-8 -*-
import os
import xml.etree.ElementTree as et

folder = "/Users/tabris/Downloads/krieg"
folder_write = "/Users/tabris/Downloads/krieg_corrected"
files = os.listdir(folder)

try:
    files.remove('.DS_Store')
except:
    something = 0

for file in files:
    path = os.path.join(folder,file)
    
    with open(path,'r') as r:
        data = r.read()
        print type(data)
        replacee1 = "<" + file[:7] + ">"
        replacee2 = "</" + file[:7] + ">"
        print replacee1
        print replacee2
        data = data.replace(replacee1,'')
        data = data.replace(replacee2,'')
        
        writee = os.path.join(folder_write,file)
        with open(writee,'w') as w:
            w.write(data)
            
print "done"