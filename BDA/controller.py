import sentiment
import spellchecker
import test_sentiment as ts

# sentiment
senti_WS = sentiment.setup()
# spellchecker.spellcheck(test)
# sentiment.sentiment(test, senti_WS)

# train sentiment
reference_list = ts.reference_list()
train_set = ts.setup()
test_set = ts.test(train_set,senti_WS)
test_negate_set = ts.test_negate(train_set,senti_WS)

print ts.find_extremes(test_negate_set)

# COMPARISON
scaled_train_set = ts.scale(train_set,0.2)
scaled_test_set = ts.scale(test_set,5.52944)
scaled_negate_test_set = ts.scale(test_negate_set,5.52944)

print ts.mse(scaled_train_set,reference_list,scaled_test_set,reference_list)
print ts.mse(scaled_train_set,reference_list,scaled_negate_test_set,reference_list)

## let's go!
#path = "/Users/tabris/Downloads/krieg_corrected"
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