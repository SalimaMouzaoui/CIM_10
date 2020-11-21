import nltk
import os 
import cleaner
import excel

from nltk.classify import NaiveBayesClassifier

#Listing diagnosis text Files 
def listDocuments(dirPath):
    listDocs = []
    for (dirpath, dirnames, filenames) in os.walk(dirPath):
        listDocs.extend(filenames)
        break
    print (listDocs)  
    return listDocs


def train(train_data):   
    classifier = NaiveBayesClassifier.train(train_data)
    
    return classifier



listDocs = listDocuments('CRH')
train_data = []
codes = excel.getCIM('Diagnostics.xlsx')

for file in listDocs:
    
    words = cleaner.clean("Clean/"+file)
   # print (codes)
    t = (words,codes[file[:-4]])
    train_data.append(t)
    #print (train_data)

cl = train (train_data)
words = ['tumeur']
test = dict([(word, True) for word in words])

print(cl.classify(test))


#for label in dist.samples():
 #   print (label,dist.prob(label))


