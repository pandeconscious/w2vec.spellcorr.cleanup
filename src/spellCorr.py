'''
Created on 06-Nov-2016

@author: harshit
'''

import numpy as np
import sklearn.neighbors as sn
import time
from sklearn.neighbors import ball_tree

dimW2Vec = None
numNeighbors = 1000
startEndCharMultiplicant = 1

def getCharVecs(fileName):
    dic = {}
    fvecs = open(fileName)
    for line in fvecs.readlines():
        line = line.strip().split()
        dic[line[0]] = np.array([float(i) for i in line[1:]])
    fvecs.close()
    global dimW2Vec
    dimW2Vec =  dic['a'].shape[0]
    return dic

def getDicWordVecs(charVecs, dicFile):
    dicW2Vec = {}
    dicVec2W = {}
    f = open(dicFile)
    for w in f.readlines():
        w = w.strip()
        
        vec = getVec(charVecs, w)
        
        """
        vec = np.zeros(dimW2Vec)
        numChars = len(w)
        ind = 0
        for c in w:
            if c in charVecs:
                if ind == 0 or ind == numChars-1:
                    vec = np.add(vec, startEndCharMultiplicant*charVecs[c])
                else:
                    vec = np.add(vec, charVecs[c])
            ind += 1
        """
        
        dicW2Vec[w] = vec
        tupleVec = tuple(vec)
        if tupleVec in dicVec2W:
            dicVec2W[tupleVec].append(w)
        else:
            dicVec2W[tupleVec] = [w]
            
        
    f.close()
    return (dicW2Vec, dicVec2W)

def getSpellPairs(fileName):
    dic = {}
    f = open(fileName)
    for line in f.readlines():
        pair = line.strip().split(',')
        dic[pair[0]] = pair[1]
    f.close()
    return dic

def getVec(charVecs, word):
    vec = np.zeros(dimW2Vec)
    """
    for c in word:
        if c in charVecs:
            vec = np.add(vec, charVecs[c])
    """
   
    numChars = len(word)   
    ind = 0
    for c in word:
        if c in charVecs:
            if ind == 0 or ind == numChars-1:
                vec = np.add(vec, startEndCharMultiplicant*charVecs[c])
            else:
                vec = np.add(vec, charVecs[c])
        ind += 1
    return vec

if __name__ == "__main__":
    charVecs = getCharVecs('../data/charVectors.txt')
    dicWord2Vec, dicVec2Word = getDicWordVecs(charVecs, '../data/wordsEnhancedEn.txt')
    
    """
    countAna = []
    for vec, wordlist in dicVec2Word.items():
        countAna.append(len(wordlist))
        if len(wordlist) == 10:
            print wordlist
            
    print "mean num of words per vector: " + str(np.array(countAna).mean())
    print "max num of words per vector: " + str(np.array(countAna).max())
    print "min num of words per vector: " + str(np.array(countAna).min())
    print "median num of words per vector: " + str(np.median(np.array(countAna)))
    
    exit(0)
    """
    
    allDicVecs = np.array(dicVec2Word.keys())
    
    #spellPairs = getSpellPairs('../data/misspeltCorrectPairs.txt')
    spellPairs = getSpellPairs('../data/misspeltCorrectPairsEditDist4.txt')


    #metricArr = ['euclidean', 'braycurtis', 'russellrao', 'cityblock', 'manhattan', 'infinity', 'jaccard', 'seuclidean', 'sokalsneath', 'kulsinski', 'minkowski', 'mahalanobis', 'p', 'l2', 'hamming', 'l1', 'wminkowski', 'pyfunc']
    metricArr = ['euclidean']
    for metr in metricArr:
        errorFile = open('../data/errorPairs.txt', 'w')
        noErrorFile = open('../data/noErrorPairs.txt', 'w')
        
        print "metric: ", metr 
        tree = sn.BallTree(allDicVecs, metric=metr)
        counter = 0
        
        oldtime = time.time()
        
        for incorr, corr in spellPairs.items():
            incorrVec = getVec(charVecs, incorr)
            neigborsInds = tree.query([incorrVec], k = numNeighbors, return_distance = False)
            #print counter
            found = False
            for ind in neigborsInds[0]:
                if corr in dicVec2Word[tuple(allDicVecs[ind])]:
                    counter += 1
                    found = True
                    break
            
            if found == True:
                noErrorFile.write(incorr +","+ corr+"\n")
            else:
                errorFile.write(incorr + ","+ corr+"\n")
        
        newtime = time.time()
        
        errorFile.close()
        noErrorFile.close()
        
        print "percent found: ", (float(counter)*100)/float(len(spellPairs.keys()))
        print "average time: ", (newtime - oldtime)/float(len(spellPairs.keys()))
        print "=====================================================================\n"
     
       
        
    
    
    
    
    