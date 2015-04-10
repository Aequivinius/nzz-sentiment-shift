# -*- coding: utf-8 -*-
import os
import xml.etree.ElementTree as et

negatives = ['nicht','nichts','kein','weniger','keineswegs']

def setup():
    # reading sentiWS
    senti_WS_negative = "/Users/tabris/Downloads/BDA/SentiWS_v1.8c/SentiWS_v1.8c_Negative.txt"
    senti_WS_positive = "/Users/tabris/Downloads/BDA/SentiWS_v1.8c/SentiWS_v1.8c_Positive.txt"
    senti_WS_write = "/Users/tabris/Downloads/BDA/SentiWS_v1.8c/Senti_WS_written"
    
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
    
    return senti_WS
    
    # writing to file, but that's not really needed
    #with open(senti_WS_write,'w') as w:
        #for key,value in senti_WS.iteritems():
            #w.write(key + "," + value + "\n")

def sentiment(text,dictionary):
    counter = 0
    value = 0 
    for word in text.split(" "):
        counter += 1
        if word in dictionary:
            value += float(dictionary[word])
    
    return value / counter

def sentiment2(text,dictionary):
    counter = 0
    value = 0 
    for word in text.split(" "):
        if word in dictionary:
            counter += 1
            value += float(dictionary[word])
    
    return value / counter
    
def sentiment_negate(text,dictionary):
    counter = 0
    value = 0 
    neck_counter = 0
    inverter = False    
    for word in text.split(" "):
        if word in negatives:
            inverter = True
            print neck_counter
            neck_counter += 1
    for word in text.split(" "):
        counter += 1
        if word in dictionary:
            if inverter:
                add = -float(dictionary[word])
            else:
                add = float(dictionary[word])
            value += add
    
    return value / counter    