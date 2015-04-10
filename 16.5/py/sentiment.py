# -*- coding: utf-8 -*-
import os
import xml.etree.ElementTree as et

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
    for word in text.split(" "):
        counter += 1
        if word in senti_WS:
            value += float(senti_WS[word])
    
    return value / counter

# let's go!
#path = "/Users/Simon/UNI_VII/bigdata/nzz/evaluation/"
#files = os.listdir(path)

#try:
    #files.remove('.DS_Store')
#except:
    #something = 0
    
## 
    
#with open(os.path.join(path,"evaluation"),'w') as w:
    #for currentfile in files:
        #print currentfile
        #currentpath = os.path.join(path, currentfile)
        #tree = et.parse(currentpath)
        #root = tree.getroot()
        
        #ps = 0
        #sentimentsum = 0    
       
        #for child in root.findall('p'):   
            #text = unicode(child.text)
            
            #ps += 1
            #sentimentsum += sentiment(text)
        
        #average = sentimentsum / ps
        #w.write(currentfile[:7] + "," + str(average) + "\n")