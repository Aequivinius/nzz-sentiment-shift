# -*- coding: utf-8 -*-
import xml.etree.ElementTree as et
import os

path =  "/Users/tabris/Downloads/16.5/kunst/"
folderlist=os.listdir(path)
print folderlist

try:
    folderlist.remove('.DS_Store')
except:
    bla = 1

write_file = os.path.join(path,"evaluation.csv")
print write_file
with open(write_file,'w') as w:
    print "here"
    for file in folderlist:
        filepath=os.path.join(path, file)
        tree = et.parse(filepath)
        root = tree.getroot()
        
        mystring = file[:4]+";"+file[5:7]+";"+str(root.get('senti'))+"\n"
        print mystring
        w.write(mystring)
            