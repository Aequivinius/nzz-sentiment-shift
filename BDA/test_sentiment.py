# -*- coding: utf-8 -*-
import sentiment
import spellchecker

test_txt = "/Users/tabris/Downloads/BDA/GermanSentimentData/data.txt"
positive_txt = "/Users/tabris/Downloads/BDA/GermanSentimentData/positive-lables.txt"
negative_txt = "/Users/tabris/Downloads/BDA/GermanSentimentData/negative-lables.txt"
corrected_txt = "/Users/tabris/Downloads/BDA/GermanSentimentData/corrected.txt"

def reference_list():
    reference_list = []
    with open(test_txt,'r') as r:
        for line in r:
            reference_list.append(line)
    
    return reference_list

def setup():
    test_list = []
    test_set = {}
    
    with open(test_txt,'r') as r:
        for line in r:
            test_list.append(line)
    
    with open(positive_txt,'r') as p:
        counter = 0
        next(p)
        for line in p:
            average_rating = 0
            ratings = line.split("\t")
            for rating in ratings:
                average_rating += float(rating)
            average_rating = average_rating / len(ratings)
            test_set[test_list[counter]] = average_rating
            counter += 1
    
    with open(negative_txt,'r') as n:
        counter = 0
        next(n)
        for line in n:
            average_rating = 0
            ratings = line.split("\t")
            for rating in ratings:
                average_rating += float(rating)
            average_rating = average_rating / len(ratings)
            
            if test_list[counter] in test_set:                
                test_set[test_list[counter]] -= average_rating
            else:                
                test_set[test_list[counter]] = (0-average_rating)
            counter += 1
    
    return test_set

def test(test_set,dictionary):
    test = {}
    for key in test_set.keys():
        test[key] =  sentiment.sentiment(key,dictionary)
    
    return test

def test_negate(test_set,dictionary):
    test = {}
    for key in test_set.keys():
        test[key] =  sentiment.sentiment_negate(key,dictionary)
    
    return test

def correct(reference_list):
    corrected_reference_list = [0] * len(reference_list)
    for i in range(len(reference_list)):
        print "Spellchecking ",i
        key = spellchecker.spellcheck(reference_list[i])
        corrected_reference_list[i] = key
    print len(corrected_reference_list)
    
    len(corrected_reference_list)
    
    with open("/Users/tabris/Downloads/BDA/GermanSentimentData/corrected.txt",'w') as c:
        for i in range(len(corrected_reference_list)):
            if (corrected_reference_list[i] == ""):
                c.write(" ")
            else:
                c.write(corrected_reference_list[i])    

def corrected(dictionary):
    corrected_reference_list = []
    with open(corrected_txt,'r') as r:
        for line in r:
            corrected_reference_list.append(line) 
    
    corrected_test_set = {}
    for item in corrected_reference_list:
        corrected_test_set[item] = sentiment.sentiment(item,dictionary)
        
    return corrected_reference_list,corrected_test_set

def find_extremes(my_set):
    min_value = 0
    max_value = 0
    
    for value in my_set.values():
        if value > max_value:
            max_value = value
        
        if value < min_value:
            min_value = value
    
    return min_value,max_value

def scale(test_set,factor):
    scaled_test_set = {}
    for key,value in test_set.items():
        scaled_test_set[key] = value * factor
    
    return scaled_test_set

def mse(training_set,training_reference,test_set,test_reference):
    sum = 0
        
    for i in range(len(training_reference)):
        training = training_set[training_reference[i]]
        test = test_set[test_reference[i]]
        error = training - test
        error = error * error
        sum += error
    mse = sum / len(training_set)
    return mse
        